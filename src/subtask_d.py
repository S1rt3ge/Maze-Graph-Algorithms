"""Subtask D: maximum flow from G to S (Edmonds-Karp).

Owner: Boris Arutinov.

Directed flow network:
  - source = G, sink = S
  - capacity(u, v) = value(v)
  - capacity into S = 100, capacity into G = 100 (special override)

Edges are created in both directions between neighbouring non-wall cells
according to the movement mode (each direction gets its own capacity).
"""

from __future__ import annotations


def solve(grid: list[list[str]], mode: int = 4) -> dict:
    """Return {'max_flow': int, 'positive_flow_edges': [...], 'mode': str}.

    TODO: build capacity table, run Edmonds-Karp (BFS augmenting paths),
          collect edges with positive flow at the end.
    """
    raise NotImplementedError("Subtask D — see GitHub issue 'Subtask D: max flow'")
