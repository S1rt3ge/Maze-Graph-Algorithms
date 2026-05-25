"""Maze parsing and grid utilities.

Owner: Oleksii Burianov (foundation).

The maze is stored as a list of rows, each row being a list of single-character
cells. Allowed cells: 'S' (start), 'G' (goal), 'X' (wall), '0'..'9' (passable
cell with a numeric value).
"""

from __future__ import annotations

from pathlib import Path

<<<<<<< HEAD
VALID_CHARS = set("SGX0123456789")
=======
VALID_CELLS = frozenset("SGX0123456789")
>>>>>>> 765997de98c4f29f1acfeb16815cf336b679b224


def load(path: str | Path) -> list[list[str]]:
    """Read a maze text file and return it as a 2D grid of characters.

<<<<<<< HEAD
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
=======
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
>>>>>>> 765997de98c4f29f1acfeb16815cf336b679b224

    return grid


def find(grid: list[list[str]], ch: str) -> tuple[int, int]:
    """Return (row, col) of the unique cell containing `ch`."""
    for r, row in enumerate(grid):
        for c, cell in enumerate(row):
            if cell == ch:
                return (r, c)
<<<<<<< HEAD
    raise ValueError(f"Character {ch!r} not found in grid.")
=======
    raise ValueError(f"Character {ch!r} not found in grid")
>>>>>>> 765997de98c4f29f1acfeb16815cf336b679b224


def value_of(ch: str) -> int:
    """Numeric value of a cell character.

    'S' and 'G' are treated as 0. Digits return their integer value.
    Walls have no numeric value, so passing 'X' raises.
    """
    if ch in ("S", "G"):
        return 0
    if ch.isdigit():
        return int(ch)
<<<<<<< HEAD
    raise ValueError(f"Cell {ch!r} has no numeric value (it is a wall or unknown).")
=======
    raise ValueError(f"Cell {ch!r} has no numeric value (walls are not passable)")
>>>>>>> 765997de98c4f29f1acfeb16815cf336b679b224
