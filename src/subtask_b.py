"""Subtask B: minimum-cost path from S to G (Dijkstra).

Owner: Kirill Pochinchik.

Cost models:
  - 'enter'    : cost(u, v) = value(v)
  - 'leave'    : cost(u, v) = value(u)
  - 'combined' : cost(u, v) = value(u) + value(v)

value(S) = value(G) = 0 for all models.

Approach
--------
Dijkstra with a min-heap (heapq). All edge weights are non-negative (cell
values are 0–9), so Dijkstra is correct and optimal.

Time complexity : O((V + E) log V)
Space complexity: O(V)
"""

from __future__ import annotations

import heapq
from typing import TYPE_CHECKING

from . import maze as maze_utils

if TYPE_CHECKING:
    from .graph import Graph


def _edge_cost(graph: "Graph", u: tuple, v: tuple, cost_model: str) -> int:
    """Return the cost of traversing edge u → v under the chosen model."""
    val_u = maze_utils.value_of(graph.grid[u[0]][u[1]])
    val_v = maze_utils.value_of(graph.grid[v[0]][v[1]])
    if cost_model == "enter":
        return val_v
    if cost_model == "leave":
        return val_u
    # combined
    return val_u + val_v


def solve(graph: "Graph", cost_model: str = "enter") -> dict:
    """Return {'cost': int, 'path': [(r, c), ...], 'cost_model': str, 'mode': str}.

    Dijkstra from graph.start; stops as soon as graph.goal is settled.
    Path is reconstructed via a parent map.
    """
    src = graph.start
    dst = graph.goal

    # dist[v] = best known cost from src to v
    dist: dict[tuple, int] = {src: 0}
    parent: dict[tuple, tuple | None] = {src: None}

    # min-heap entries: (cost, vertex)
    heap: list[tuple[int, tuple]] = [(0, src)]

    while heap:
        cost, u = heapq.heappop(heap)

        # Skip stale heap entries: when we relax a vertex we just push a new
        # (smaller-cost, vertex) pair instead of updating the old one, so the
        # heap can contain several entries for the same vertex. Only the
        # smallest one is real, the rest must be ignored.
        if cost > dist.get(u, float("inf")):
            continue

        # All edge weights are non-negative (cell values are 0..9), so once
        # Dijkstra pops the goal we have its final shortest distance and can
        # stop right away - the rest of the heap can only contain >= costs.
        if u == dst:
            break

        for v in graph.adj.get(u, []):
            new_cost = cost + _edge_cost(graph, u, v, cost_model)
            if new_cost < dist.get(v, float("inf")):
                dist[v] = new_cost
                parent[v] = u
                heapq.heappush(heap, (new_cost, v))

    # Reconstruct path
    if dst not in dist:
        return {
            "cost": -1,
            "path": [],
            "cost_model": cost_model,
            "mode": str(graph.mode),
        }

    path: list[tuple] = []
    node: tuple | None = dst
    while node is not None:
        path.append(node)
        node = parent[node]
    path.reverse()

    return {
        "cost": dist[dst],
        "path": path,
        "cost_model": cost_model,
        "mode": str(graph.mode),
    }
