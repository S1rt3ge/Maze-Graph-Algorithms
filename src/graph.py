"""Graph construction from a maze grid.

Owner: Oleksii Burianov (foundation).

A `Graph` is an adjacency representation over non-wall cells.
Each vertex is a (row, col) tuple. Movement mode controls which neighbours
are connected (4-directional or 8-directional).
"""

from __future__ import annotations

from dataclasses import dataclass, field

Vertex = tuple[int, int]


@dataclass
class Graph:
    grid: list[list[str]]
    mode: int  # 4 or 8
    adj: dict[Vertex, list[Vertex]] = field(default_factory=dict)
    start: Vertex = (0, 0)
    goal: Vertex = (0, 0)


def build(grid: list[list[str]], mode: int = 4) -> Graph:
    """Construct an adjacency-list graph for the given maze grid.

    TODO:
      - locate S and G
      - for every non-wall cell, generate neighbours under the chosen mode
      - skip neighbours that are walls or outside the grid
    """
    raise NotImplementedError("graph.build — see issue: foundation (parser + graph)")
