"""This module can reshape a criteria file from a long format to a wider one."""

import importlib.resources as pkg_resources
from os import PathLike

import polars as pl

from asbg.utils.logger import get_logger


class ReshapeToWide:
    """Reshapes a criteria file in a long format to a wide one.

    Args:
        src: The path of the criteria file in a long format. Defaults to None.
        dst: The path where to save the reshaped file. Defaults to None.
        index: The column(s) to use as the index of the DataFrame in long format.
            Defaults to ["licence", "genre", "participation"].
        group_by: The list of column(s) to use to group by the DataFrame in long format.
            Defaults to ["critere", "sous_critere"].
        value: The value column in the DataFrame in long format. Defaults to "score".
    """

    def __init__(
        self,
        src: str | PathLike | None = None,
        dst: str | PathLike | None = None,
        index: tuple[str] = ("licence", "genre", "participation"),
        group_by: tuple[str] = ("critere", "sous_critere"),
        value: str = "score",
    ) -> None:
        self.logger = get_logger(__name__)
        self.src = src
        self.dst = dst
        self.index = index
        self.group_by = group_by
        self.value = value

    def reshape(self) -> pl.DataFrame:
        """Reshapes a criteria file in a long format to a wide one."""
        criteria = self.load_criteria()
        criteria = self.from_long_to_wide(criteria)
        self.save(criteria)

        return criteria

    def load_criteria(self) -> pl.DataFrame:
        """Loads the criteria file in a long format."""
        if self.src is None:
            ressource = pkg_resources.files("asbg.teams.data").joinpath("example-criteria.csv")
            with pkg_resources.as_file(ressource) as filename:
                self.src = filename

        self.logger.debug(f"Loading the criteria data from `{self.src}`...")

        return pl.read_csv(self.src, separator=";")

    def from_long_to_wide(self, df: pl.DataFrame) -> pl.DataFrame:
        """Reshapes the given DataFrame from long to wide.

        Args:
            df: The DataFrame to reshape.

        Returns:
            The reshaped DataFrame in a wide format.
        """
        self.logger.info("Formating the criteria to a wide format...")
        mapping = self.map_columns(df)
        df_wide = df.pivot(self.group_by, index=self.index, values=self.value)
        return df_wide.rename(mapping)

    def map_columns(self, df: pl.DataFrame) -> pl.DataFrame:
        """Creates a mapping of the column names to rename them properly after the reshaping.

        Args:
            df: The DataFrame from which to create the mapping.

        Returns:
            The mapping between the column names.
        """
        mapping = list(df.select(self.group_by).unique().iter_rows())
        return {f'{{"{row[0]}","{row[1]}"}}': row[1] for row in mapping}

    def save(self, df: pl.DataFrame) -> None:
        """Saves the reshaped DataFrame.

        Args:
            df: The DataFrame in wide format to save.
        """
        ressource = pkg_resources.files("asbg.teams.data").joinpath("example-criteria-wide.csv")

        with pkg_resources.as_file(ressource) as filename:
            self.logger.debug(f"Writing the example file to `{filename}`")
            df.write_csv(filename, separator=";")
