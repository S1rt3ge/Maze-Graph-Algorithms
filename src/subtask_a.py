"""Subtask A: shortest path from S to G by number of moves (BFS).

Owner: Oleksii Burianov.

Every legal move has cost 1, so a breadth-first search layer-by-layer gives the
minimum number of moves. We record each visited cell's predecessor in a parent
map and walk it backwards from G to reconstruct the path.

Complexity:
  time  - O(V + E)
  space - O(V)   (parent map + BFS frontier)
"""

from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .graph import Graph, Vertex


def solve(graph: "Graph") -> dict:
    """Return shortest-path info from S to G under unit-cost moves.

    Returned dict:
        moves      : int | None         - minimum number of moves, or None if G is unreachable
        path       : list[(row, col)]   - S to G inclusive (empty if unreachable)
        mode       : str                - "4" or "8" (movement mode used)
        reachable  : bool
    """
    start = graph.start
    goal = graph.goal
    adj = graph.adj

    parent: dict["Vertex", "Vertex | None"] = {start: None}
    queue: deque["Vertex"] = deque([start])

    while queue:
        v = queue.popleft()
        if v == goal:
            break
        for n in adj[v]:
            if n not in parent:
                parent[n] = v
                queue.append(n)

    if goal not in parent:
        return {
            "moves": None,
            "path": [],
            "mode": str(graph.mode),
            "reachable": False,
        }

    path: list["Vertex"] = []
    cur: "Vertex | None" = goal
    while cur is not None:
        path.append(cur)
        cur = parent[cur]
    path.reverse()

    return {
        "moves": len(path) - 1,
        "path": path,
        "mode": str(graph.mode),
        "reachable": True,
    }
