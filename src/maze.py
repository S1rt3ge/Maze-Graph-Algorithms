"""Maze parsing and grid utilities.

Owner: Oleksii Burianov (foundation).

The maze is stored as a list of rows, each row being a list of single-character
cells. Allowed cells: 'S' (start), 'G' (goal), 'X' (wall), '0'..'9' (passable
cell with a numeric value).
"""

from __future__ import annotations

from pathlib import Path

VALID_CELLS = frozenset("SGX0123456789")


def load(path: str | Path) -> list[list[str]]:
    """Read a maze text file and return it as a 2D grid of characters.

    Validates that:
      - the file is non-empty,
      - every row has the same length,
      - every cell is one of S/G/X/0-9,
      - the maze contains exactly one S and exactly one G.
    """
    text = Path(path).read_text(encoding="utf-8")
    lines = text.splitlines()
    while lines and not lines[-1].strip():
        lines.pop()
    if not lines:
        raise ValueError(f"Maze file is empty: {path}")

    grid = [list(line) for line in lines]
    width = len(grid[0])
    for r, row in enumerate(grid):
        if len(row) != width:
            raise ValueError(
                f"Row {r} has length {len(row)}, expected {width} "
                f"(all rows must be the same length)"
            )

    s_count = 0
    g_count = 0
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch not in VALID_CELLS:
                raise ValueError(
                    f"Invalid cell {ch!r} at ({r},{c}); "
                    f"allowed: S, G, X, 0-9"
                )
            if ch == "S":
                s_count += 1
            elif ch == "G":
                g_count += 1

    if s_count != 1:
        raise ValueError(f"Maze must contain exactly one 'S', found {s_count}")
    if g_count != 1:
        raise ValueError(f"Maze must contain exactly one 'G', found {g_count}")

    return grid


def find(grid: list[list[str]], ch: str) -> tuple[int, int]:
    """Return (row, col) of the unique cell containing `ch`."""
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == ch:
                return (r, c)
    raise ValueError(f"Character {ch!r} not found in grid")


def value_of(ch: str) -> int:
    """Numeric value of a cell character.

    'S' and 'G' are treated as 0. Digits return their integer value.
    Walls have no numeric value, so passing 'X' raises.
    """
    if ch in ("S", "G"):
        return 0
    if ch.isdigit():
        return int(ch)
    raise ValueError(f"Cell {ch!r} has no numeric value (walls are not passable)")
