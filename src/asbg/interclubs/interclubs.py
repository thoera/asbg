"""This module parses the results of the Interclubs from https://icbad.ffbad.org."""

import re
from typing import NamedTuple

import requests
from bs4 import BeautifulSoup, element

from asbg.interclubs.database import connect
from asbg.utils.logger import get_logger


class Team(NamedTuple):
    team_id: str
    competition: str
    division: str
    group: str
    year: str


class Disciplines(NamedTuple):
    SH: str | None = None
    SD: str | None = None
    DH: str | None = None
    DD: str | None = None
    DX: str | None = None


class Results(NamedTuple):
    wins: int
    losses: int


class Interclubs:
    """Fetches, parses and saves the results of the Interclubs into a database."""

    def __init__(self) -> None:
        self.name = "Association Sportive des Badistes Givrés"
        self.logger = get_logger(__name__)

    def parse(self) -> None:
        """Fetches, parses and saves the results of the Interclubs into a database.

        Two tables will be created and populated: a "team" table and a "result" table.

        The format of the "team" table is the following:

        ```
        | team_id |   competition |   division |   group |   year |
        | ------- | ------------- | ---------- | ------- | ------ |
        |  <id_1> | <competition> | <division> | <group> | <year> |
        |  <id_2> | <competition> | <division> | <group> | <year> |
        |     ... |           ... |        ... |     ... |    ... |
        ```

        Where `team_id` is the primary key.

        The format of the "result" table is the following:

        ```
        | team_id |     discipline |   wins |   losses |
        | ------- | -------------- | ------ | -------- |
        |  <id_1> | <discipline_1> | <wins> | <losses> |
        |  <id_1> | <discipline_2> | <wins> | <losses> |
        |     ... |            ... |    ... |      ... |
        ```

        Where (`team_id`, `discipline`) is the primary key.

        "REPLACE" statements are used when loading the data into the database
        to allow running the parsing several times (to take into account new results
        during the year for instance).
        See https://www.sqlite.org/lang_conflict.html
        """
        self.logger.info("Parsing the results of the Interclubs")
        teams = self._get_teams()

        results = {}

        for team in teams:
            team_results = self._get_team_results(team)
            results[team] = team_results

        self._save(results)

    def _get_teams(self) -> list[Team]:
        """Gets the teams competing in the Interclubs.

        Returns:
            A list of the teams competing in the Interclubs.
        """
        url = "https://icbad.ffbad.org/instance/ASBG75"
        request = requests.get(url)
        soup = BeautifulSoup(markup=request.text, features="html.parser")

        year = soup.find_all("a", {"href": "https://icbad.ffbad.org"})[1].text

        team_details = soup.find_all("h2")

        regex = re.compile(rf"{self.name}.*")

        teams = []

        for team in team_details:
            competition, division, group = team.text.split(" - ")

            for sibling in team.next_siblings:
                # If we find a "h2" header, it means that we reached a new team.
                if sibling.name == "h2":
                    break

                try:
                    match = sibling.find_all("td", class_="nom-equipe", string=regex)
                    if match:
                        team_id = parse_team_id(match[0])
                        teams.append(Team(team_id, competition, division, group, year))
                except AttributeError:
                    pass

        return teams

    def _get_team_results(self, team: Team) -> Disciplines[Results]:
        """Gets the results in the Interclubs for a given team.

        Args:
            team: A Team object for which to get the results.

        Returns:
            The results in the Interclubs for the given team.
        """
        self.logger.debug(f"Getting the results for the team: {team.team_id}")

        url = f"https://icbad.ffbad.org/equipe/{team.team_id}"
        request = requests.get(url)
        soup = BeautifulSoup(markup=request.text, features="html.parser")

        disciplines = {}

        for discipline in Disciplines._fields:
            h4 = soup.find(name="h4", string=discipline)

            # The header will be empty if the discipline does not exist.
            # For instance, there is no "Men double" in a all women team.
            if h4 is None:
                continue

            for sibling in h4.next_siblings:
                if "victoire" in sibling.text:
                    wins = sibling.text.strip().split(" ")[0]
                if "défaite" in sibling.text:
                    losses = sibling.text.strip().split(" ")[0]

            disciplines[discipline] = Results(int(wins), int(losses))

        results = Disciplines(**disciplines)
        self.logger.debug(f"Team results: {results}")

        return results

    def _save(self, results: dict[Team, Disciplines[Results]]) -> None:
        """Saves the results into a SQLite database.

        This method will create the database if it does not already exists.

        Args:
            results: The results to save into the database.
        """
        self.logger.debug("Connecting to (and creating if needed) the database `data.db`")

        con = connect()

        self.logger.debug("Creating the table `team` if it does not exist")
        query = """
            CREATE TABLE IF NOT EXISTS
            team(team_id PRIMARY KEY, competition, division, 'group', year)
        """

        with con:
            con.execute(query)

        self.logger.debug("Populating the table `team`")

        rows_teams = []

        for team in results:
            rows_teams.append(
                (team.team_id, team.competition, team.division, team.group, team.year)
            )

        with con:
            con.executemany("REPLACE INTO team VALUES(?, ?, ?, ?, ?)", rows_teams)

        self.logger.debug("Creating the table `result` if it does not exist")
        query = """
            CREATE TABLE IF NOT EXISTS
            result(team_id, discipline, wins, losses, PRIMARY KEY(team_id, discipline))
        """

        with con:
            con.execute(query)

        self.logger.debug("Populating the table `result`")

        rows_results = []

        for team, team_results in results.items():
            for discipline, wins_losses in team_results._asdict().items():
                if wins_losses is not None:
                    rows_results.append((team.team_id, discipline, *wins_losses))
                else:
                    rows_results.append((team.team_id, discipline, None, None))

        with con:
            con.executemany("REPLACE INTO result VALUES(?, ?, ?, ?)", rows_results)


def parse_team_id(text: element.Tag) -> str:
    """Parses the team id from the given tag element.

    Args:
        text: The tag element from which to parse the team id.

    Returns:
        The team id parsed from the tag element.
    """
    return text.select_one("a").get("href").split("/")[-1]
