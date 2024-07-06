import random

import pytest

from asbg.teams.utils.generate_players_rankings import Player, clip, generate_players_rankings


@pytest.mark.parametrize(
    "n, lower_bound, upper_bound, expected",
    [
        (2008, 2000, 2010, 2008),
        (2, 0, 2, 2),
        (3, 0, 2, 2),
        (3, 2, 2, 2),
        (2, 2, 2, 2),
        (-1, 4, 5, 4),
    ],
)
def test_clip(n: int, lower_bound: int, upper_bound: int, expected: int) -> None:
    """Tests that we correctly clip a number between a lower and an upper bound.

    Args:
        n: The number to clip.
        lower_bound: The lower bound to use when clipping.
        upper_bound: The upper bound to use when clipping.
        expected: The expected result.
    """
    assert clip(n, lower_bound, upper_bound) == expected


def test_clip_with_invalid_bounds() -> None:
    """Tests that we correctly raise a ValueError with invalid bounds.."""
    with pytest.raises(ValueError):
        clip(94, 20, 8)


def test_generate_players_rankings() -> None:
    """Tests that we correctly generate random players."""
    random.seed(2008)
    players = generate_players_rankings(n=4, save=False)

    expected = [
        Player(licence=0, nom="ERM", prenom="dby", simple="D8", double="D8", mixte="D8"),
        Player(licence=1, nom="ZZE", prenom="kyo", simple="NC", double="P11", mixte="P11"),
        Player(licence=2, nom="RLS", prenom="rzf", simple="P12", double="P11", mixte="P12"),
        Player(licence=3, nom="SZR", prenom="wtt", simple="D8", double="P10", mixte="D8"),
    ]

    assert players == expected
