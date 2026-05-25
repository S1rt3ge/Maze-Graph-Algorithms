"""Subtask D: maximum flow from G to S (Edmonds-Karp).

Owner: Boris Arutinov.

Directed flow network:
  - source = G, sink = S
  - capacity(u, v) = value(v) for an edge into a normal cell v
  - capacity into S = 100 and capacity into G = 100 (spec override, so the
    sink/source are not blocked by their value of 0)

Vertices are non-wall cells. Between two neighbouring non-wall cells we add a
directed edge in each direction, each with its own capacity. The neighbour
relation is symmetric, so the maze adjacency list already lists both directions
and doubles as the residual-graph adjacency.

Complexity:
  time  - O(V * E^2)   (Edmonds-Karp: at most O(V*E) augmentations, each a BFS)
  space - O(V + E)     (capacity / residual tables + BFS structures)
"""

from __future__ import annotations

from collections import deque

from . import graph, maze

CAP_OVERRIDE = 100  # forced capacity for edges entering S or G


def solve(grid: list[list[str]], mode: int = 4) -> dict:
    """Return {'max_flow': int, 'positive_flow_edges': [...], 'mode': str}.

    positive_flow_edges holds ((r1, c1), (r2, c2), flow, capacity) for every
    edge carrying net positive flow.
    """
    g = graph.build(grid, mode=mode)
    adj = g.adj
    source = g.goal   # flow runs G -> S
    sink = g.start

    # capacity[(u, v)]: an edge into v costs value(v), except edges entering
    # S or G, which the spec fixes at 100.
    capacity: dict[tuple, int] = {}
    for u, neighbours in adj.items():
        for v in neighbours:
            head = grid[v[0]][v[1]]
            capacity[(u, v)] = CAP_OVERRIDE if head in ("S", "G") else maze.value_of(head)

    # residual starts as a copy of capacity; reverse edges already exist as keys
    # because the grid adjacency is symmetric, so pushing flow back is well defined.
    residual = dict(capacity)

    max_flow = 0
    while True:
        # BFS for a shortest augmenting path (in edges) with spare capacity.
        parent: dict[tuple, tuple | None] = {source: None}
        queue = deque([source])
        while queue:
            u = queue.popleft()
            if u == sink:
                break
            for v in adj[u]:
                if v not in parent and residual[(u, v)] > 0:
                    parent[v] = u
                    queue.append(v)

        if sink not in parent:
            break  # no augmenting path left -> current flow is maximum

        # bottleneck = smallest residual capacity along the path
        bottleneck = float("inf")
        v = sink
        while parent[v] is not None:
            u = parent[v]
            bottleneck = min(bottleneck, residual[(u, v)])
            v = u

        # push the bottleneck: subtract forward, add to the reverse edge
        v = sink
        while parent[v] is not None:
            u = parent[v]
            residual[(u, v)] -= bottleneck
            residual[(v, u)] += bottleneck
            v = u

        max_flow += bottleneck

    # net flow on an edge = capacity - remaining residual; report positives.
    positive_flow_edges = []
    for (u, v), cap in capacity.items():
        flow = cap - residual[(u, v)]
        if flow > 0:
            positive_flow_edges.append((u, v, flow, cap))
    positive_flow_edges.sort()

    return {
        "max_flow": max_flow,
        "positive_flow_edges": positive_flow_edges,
        "mode": str(mode),
    }
