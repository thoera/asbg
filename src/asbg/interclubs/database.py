import importlib.resources as pkg_resources
import sqlite3

import pandas as pd

from asbg.utils.logger import get_logger


def connect() -> sqlite3.Connection:
    """Establishes a connection to the database.

    Returns:
        A Connection object to the database.
    """
    with pkg_resources.as_file(pkg_resources.files("asbg.data")) as dir:
        DATABASE_FILE = dir / "data.db"

    return sqlite3.connect(DATABASE_FILE)


def fetch_results(con: sqlite3.Connection) -> pd.DataFrame:
    """Fetches the results of the Interclubs from the database.

    Args:
        con: A Connection object to the database.

    Returns:
        The results of the Interclubs fetched from the database.
    """
    logger = get_logger()
    logger.debug("Connecting to the database `data.db`")

    query = """
        SELECT
            result.team_id,
            team.competition,
            result.discipline,
            result.wins,
            result.losses
        FROM result
        INNER JOIN team ON result.team_id = team.team_id
    """

    with con:
        res = con.execute(query)
        rows = res.fetchall()

    cols = ["team_id", "competition", "discipline", "wins", "losses"]

    return pd.DataFrame(data=rows, columns=cols)
