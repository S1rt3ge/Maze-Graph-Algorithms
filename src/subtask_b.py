"""Subtask B: minimum-cost path from S to G (Dijkstra).

Owner: Kirill Pochinchik.

Cost models:
  - 'enter'    : cost(u, v) = value(v)
  - 'leave'    : cost(u, v) = value(u)
  - 'combined' : cost(u, v) = value(u) + value(v)

value(S) = value(G) = 0 for all models.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .graph import Graph


def solve(graph: "Graph", cost_model: str = "enter") -> dict:
    """Return {'cost': int, 'path': [(r, c), ...], 'cost_model': str, 'mode': str}.

    TODO: Dijkstra with a min-heap; reconstruct path via parent map.
    """
    raise NotImplementedError("Subtask B — see GitHub issue 'Subtask B: Dijkstra'")
