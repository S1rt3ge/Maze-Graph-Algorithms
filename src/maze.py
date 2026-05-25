"""Maze parsing and grid utilities.

Owner: Oleksii Burianov (foundation).
"""

from __future__ import annotations

from pathlib import Path


def load(path: str | Path) -> list[list[str]]:
    """Read a maze text file and return it as a 2D grid of characters.

    TODO:
      - validate that all rows have the same length
      - validate exactly one 'S' and one 'G'
      - validate every cell is in {'S', 'G', 'X', '0'..'9'}
    """
    raise NotImplementedError("maze.load — see issue: foundation (parser + graph)")


def find(grid: list[list[str]], ch: str) -> tuple[int, int]:
    """Return (row, col) of the unique cell containing `ch`."""
    raise NotImplementedError("maze.find — see issue: foundation (parser + graph)")


def value_of(ch: str) -> int:
    """Return the numeric value of a cell character.

    S and G have value 0. Digits return their digit value. Walls have no value.
    """
    raise NotImplementedError("maze.value_of — see issue: foundation (parser + graph)")
