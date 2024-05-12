"""This module formats the results to feed to the dashboard."""

import pandas as pd


DISCIPLINES = ["SH", "SD", "DH", "DD", "DX"]


class FormatResults:
    """Formats the results of the Interclubs to feed to the dashboard."""

    @staticmethod
    def filter_results(results: pd.DataFrame, competition: str) -> pd.DataFrame:
        """Filters the results to only keep those of the given competition.

        Args:
            results: The results of the Interclubs.
            competition: The competition for which to filter the results.

        Returns:
            The filtered results for the given competition.
        """
        return results.loc[results["competition"] == competition, :]

    def aggregate_results(self, results: pd.DataFrame) -> pd.DataFrame:
        """Aggregates the results to show them intelligibly.

        Args:
            results: The results to aggregate.

        Returns:
            The aggregated results.
        """
        results = results.loc[:, ["discipline", "wins", "losses"]].groupby("discipline").sum()

        results["win_percentage"] = results["wins"] / results.sum(axis="columns")

        results = results.reindex(DISCIPLINES)

        return self._remove_disciplines_not_played(results)

    @staticmethod
    def _remove_disciplines_not_played(results: pd.DataFrame) -> pd.DataFrame:
        """Removes from the results the disciplines which have not been played.

        Args:
            results: The results from which to remove the disciplines.

        Returns:
            The results without the disciplines which have not been played.
        """
        return results.loc[results.sum(axis=1) > 0, :]
