"""Subtask E: minimum spanning tree (Kruskal with Union-Find).

Owner: Kirill Pochinchik.

Undirected graph:
  - vertices: all non-wall cells
  - edges: between neighbouring non-wall cells (per movement mode)
  - weight(u, v) = value(u) + value(v); value(S) = value(G) = 0

Restrict MST to the connected component containing S. Also report whether
G is reachable from S.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .graph import Graph


def solve(graph: "Graph") -> dict:
    """Return:
      {
        'mst_total_weight': int,
        'component_vertices': int,
        'tree_edges_count': int,
        'tree_edges': [...],
        'mode': str,
        'goal_reachable': bool,
      }

    TODO: gather edges within S's component, sort by weight, run Kruskal
          with a Union-Find (Disjoint-Set Union).
    """
    raise NotImplementedError("Subtask E — see GitHub issue 'Subtask E: MST'")
