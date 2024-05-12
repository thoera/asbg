import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal

from asbg.interclubs.results import FormatResults


def test_filter_results() -> None:
    """Tests that we correctly filter the results."""
    res = FormatResults()

    results = pd.DataFrame(
        data={
            "team_id": [1, 1, 2, 2, 3, 3, 3],
            "competition": ["foo", "foo", "bar", "bar", "lili", "lili", "lili"],
            "discipline": ["SH", "DH", "SD", "DD", "DH", "DD", "DX"],
            "wins": [3, 2, 4, 2, 0, 3, 5],
            "losses": [3, 2, 6, 2, 0, 2, 0],
        }
    )

    computed = res.filter_results(results, competition="lili")

    expected = pd.DataFrame(
        data={
            "team_id": [3, 3, 3],
            "competition": ["lili", "lili", "lili"],
            "discipline": ["DH", "DD", "DX"],
            "wins": [0, 3, 5],
            "losses": [0, 2, 0],
        }
    )
    expected.index = [4, 5, 6]

    assert_frame_equal(computed, expected)


def test_aggregate_results() -> None:
    """Tests that we correctly aggregate the results.

    Args:
        results: The results to aggregate.
    """
    res = FormatResults()

    results = pd.DataFrame(
        data={
            "team_id": [3, 3, 3],
            "competition": ["lili", "lili", "lili"],
            "discipline": ["DH", "DD", "DX"],
            "wins": [0, 3, 5],
            "losses": [0, 2, 0],
        }
    )

    computed = res.aggregate_results(results)

    expected = pd.DataFrame(
        data={
            "discipline": ["DD", "DX"],
            "wins": [3, 5],
            "losses": [2, 0],
            "win_percentage": [0.6, 1],
        }
    ).set_index("discipline")

    assert_frame_equal(computed, expected, check_dtype=False)


def test_remove_disciplines_not_played() -> None:
    """Tests that we correctly removes the disciplines which have not been played.

    Args:
        results: The results from which to remove the disciplines.
    """
    res = FormatResults()

    results = pd.DataFrame(
        data={
            "discipline": ["SH", "SD", "DH", "DD", "DX"],
            "wins": [np.nan, np.nan, 0, 3, 5],
            "losses": [np.nan, np.nan, 0, 2, 0],
            "win_percentage": [np.nan, np.nan, np.nan, 0.6, 1],
        }
    ).set_index("discipline")

    computed = res._remove_disciplines_not_played(results)

    expected = pd.DataFrame(
        data={
            "discipline": ["DD", "DX"],
            "wins": [3, 5],
            "losses": [2, 0],
            "win_percentage": [0.6, 1],
        }
    ).set_index("discipline")

    assert_frame_equal(computed, expected, check_dtype=False)
