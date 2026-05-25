"""Graph construction from a maze grid.

Owner: Oleksii Burianov (foundation).

A `Graph` is an adjacency representation over non-wall cells.
Each vertex is a (row, col) tuple. Movement mode controls which neighbours
are connected (4-directional or 8-directional).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from . import maze as maze_utils

Vertex = tuple[int, int]

_DIRS_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
_DIRS_8 = [(-1, 0), (1, 0), (0, -1), (0, 1),
           (-1, -1), (-1, 1), (1, -1), (1, 1)]


@dataclass
class Graph:
    grid: list[list[str]]
    mode: int  # 4 or 8
    adj: dict[Vertex, list[Vertex]] = field(default_factory=dict)
    start: Vertex = (0, 0)
    goal: Vertex = (0, 0)


def build(grid: list[list[str]], mode: int = 4) -> Graph:
    """Construct an adjacency-list graph for the given maze grid."""
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    start = maze_utils.find(grid, "S")
    goal = maze_utils.find(grid, "G")

    dirs = _DIRS_8 if mode == 8 else _DIRS_4

    adj: dict[Vertex, list[Vertex]] = {}
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "X":
                continue
            v: Vertex = (r, c)
            neighbours: list[Vertex] = []
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "X":
                    neighbours.append((nr, nc))
            adj[v] = neighbours

    return Graph(grid=grid, mode=mode, adj=adj, start=start, goal=goal)
