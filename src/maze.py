"""Maze parsing and grid utilities.

Owner: Oleksii Burianov (foundation).
"""

from __future__ import annotations

from pathlib import Path

VALID_CHARS = set("SGX0123456789")


def load(path: str | Path) -> list[list[str]]:
    """Read a maze text file and return it as a 2D grid of characters.

    Validates:
      - all rows have the same length
      - exactly one 'S' and one 'G'
      - every cell is in {'S', 'G', 'X', '0'..'9'}
    """
    text = Path(path).read_text(encoding="utf-8")
    lines = [line.rstrip("\n\r") for line in text.splitlines()]
    # Drop trailing empty lines
    while lines and lines[-1] == "":
        lines.pop()

    if not lines:
        raise ValueError("Maze file is empty.")

    grid = [list(row) for row in lines]

    row_len = len(grid[0])
    for i, row in enumerate(grid):
        if len(row) != row_len:
            raise ValueError(
                f"Row {i} has length {len(row)}, expected {row_len}."
            )
        for j, ch in enumerate(row):
            if ch not in VALID_CHARS:
                raise ValueError(
                    f"Invalid character {ch!r} at ({i}, {j})."
                )

    s_count = sum(row.count("S") for row in grid)
    g_count = sum(row.count("G") for row in grid)
    if s_count != 1:
        raise ValueError(f"Expected exactly one 'S', found {s_count}.")
    if g_count != 1:
        raise ValueError(f"Expected exactly one 'G', found {g_count}.")

    return grid


def find(grid: list[list[str]], ch: str) -> tuple[int, int]:
    """Return (row, col) of the unique cell containing `ch`."""
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == ch:
                return (r, c)
    raise ValueError(f"Character {ch!r} not found in grid.")


def value_of(ch: str) -> int:
    """Return the numeric value of a cell character.

    S and G have value 0. Digits return their digit value. Walls have no value.
    """
    if ch in ("S", "G"):
        return 0
    if ch.isdigit():
        return int(ch)
    raise ValueError(f"Cell {ch!r} has no numeric value (it is a wall or unknown).")
