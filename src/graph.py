"""Graph construction from a maze grid.

Owner: Oleksii Burianov (foundation).

A `Graph` is an adjacency list over the non-wall cells of the maze. Each vertex
is a `(row, col)` tuple. The movement mode chooses which neighbours are
connected: 4 cardinal directions, or 4 cardinal + 4 diagonals.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import maze

Vertex = tuple[int, int]

DIRS_4: tuple[tuple[int, int], ...] = (
    (-1, 0),  # up
    (1, 0),   # down
    (0, -1),  # left
    (0, 1),   # right
)

DIRS_8: tuple[tuple[int, int], ...] = DIRS_4 + (
    (-1, -1),  # up-left
    (-1, 1),   # up-right
    (1, -1),   # down-left
    (1, 1),    # down-right
)


@dataclass
class Graph:
    grid: list[list[str]]
    mode: int
    adj: dict[Vertex, list[Vertex]] = field(default_factory=dict)
    start: Vertex = (0, 0)
    goal: Vertex = (0, 0)


def build(grid: list[list[str]], mode: int = 4) -> Graph:
    """Build an adjacency-list graph for the maze.

    Vertices: every non-wall cell.
    Edges: between adjacent non-wall cells under the chosen movement mode.
    """
    if mode not in (4, 8):
        raise ValueError(f"mode must be 4 or 8, got {mode}")

    dirs = DIRS_4 if mode == 4 else DIRS_8
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    adj: dict[Vertex, list[Vertex]] = {}
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "X":
                continue
            neighbours: list[Vertex] = []
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "X":
                    neighbours.append((nr, nc))
            adj[(r, c)] = neighbours

    return Graph(
        grid=grid,
        mode=mode,
        adj=adj,
        start=maze.find(grid, "S"),
        goal=maze.find(grid, "G"),
    )
