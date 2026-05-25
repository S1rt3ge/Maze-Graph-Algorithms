"""Subtask E: minimum spanning tree (Kruskal with Union-Find).

Owner: Kirill Pochinchik.

Undirected graph:
  - vertices: all non-wall cells
  - edges: between neighbouring non-wall cells (per movement mode)
  - weight(u, v) = value(u) + value(v); value(S) = value(G) = 0

Restricted to the connected component containing S.

Approach
--------
1. BFS/DFS from S over graph.adj to find all vertices in S's component.
2. Collect undirected edges inside that component (each pair once).
3. Sort edges by weight (ascending).
4. Kruskal: iterate edges, use Union-Find (path compression + union-by-rank)
   to skip edges that would form a cycle.
5. Accept edge when its endpoints are in different sets; stop after |V|-1 edges.

Cycle avoidance : Union-Find — two vertices are in the same tree iff
                  find(u) == find(v); merging via union-by-rank keeps trees flat.
Edge selection  : sort ascending by weight → always pick the globally
                  cheapest remaining edge that doesn't create a cycle.

Time complexity : O(E log E)  — sort dominates
Space complexity: O(V + E)
"""

from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING

from . import maze as maze_utils

if TYPE_CHECKING:
    from .graph import Graph


# ---------------------------------------------------------------------------
# Union-Find (Disjoint-Set Union) with path compression + union-by-rank
# ---------------------------------------------------------------------------

class _DSU:
    def __init__(self, vertices: list[tuple]) -> None:
        self._parent: dict[tuple, tuple] = {v: v for v in vertices}
        self._rank: dict[tuple, int] = {v: 0 for v in vertices}

    def find(self, x: tuple) -> tuple:
        while self._parent[x] != x:
            # Path compression (halving)
            self._parent[x] = self._parent[self._parent[x]]
            x = self._parent[x]
        return x

    def union(self, x: tuple, y: tuple) -> bool:
        """Merge sets of x and y. Returns True if they were different sets."""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        # Union by rank
        if self._rank[rx] < self._rank[ry]:
            rx, ry = ry, rx
        self._parent[ry] = rx
        if self._rank[rx] == self._rank[ry]:
            self._rank[rx] += 1
        return True


# ---------------------------------------------------------------------------
# Main solver
# ---------------------------------------------------------------------------

def solve(graph: "Graph") -> dict:
    """Return MST result dict for the connected component containing S."""
    src = graph.start
    dst = graph.goal

    # --- Step 1: BFS to find S's connected component ---
    component: set[tuple] = set()
    queue: deque[tuple] = deque([src])
    component.add(src)
    while queue:
        u = queue.popleft()
        for v in graph.adj.get(u, []):
            if v not in component:
                component.add(v)
                queue.append(v)

    goal_reachable = dst in component

    # --- Step 2: Collect undirected edges (each edge once) ---
    seen_edges: set[frozenset] = set()
    edges: list[tuple[int, tuple, tuple]] = []  # (weight, u, v)

    for u in component:
        val_u = maze_utils.value_of(graph.grid[u[0]][u[1]])
        for v in graph.adj.get(u, []):
            if v not in component:
                continue
            key = frozenset((u, v))
            if key in seen_edges:
                continue
            seen_edges.add(key)
            val_v = maze_utils.value_of(graph.grid[v[0]][v[1]])
            weight = val_u + val_v
            edges.append((weight, u, v))

    # --- Step 3: Sort by weight ---
    edges.sort(key=lambda e: e[0])

    # --- Step 4 & 5: Kruskal ---
    dsu = _DSU(list(component))
    tree_edges: list[tuple[tuple, tuple, int]] = []
    total_weight = 0
    target = len(component) - 1  # MST has |V|-1 edges

    for weight, u, v in edges:
        if len(tree_edges) == target:
            break
        if dsu.union(u, v):
            tree_edges.append((u, v, weight))
            total_weight += weight

    return {
        "mst_total_weight": total_weight,
        "component_vertices": len(component),
        "tree_edges_count": len(tree_edges),
        "tree_edges": tree_edges,
        "mode": str(graph.mode),
        "goal_reachable": goal_reachable,
    }
