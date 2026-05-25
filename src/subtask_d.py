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
    source = g.goal   # the spec asks for the flow that can be pushed from G to S
    sink = g.start

    # Build the capacity table. Every (u, v) with v non-wall gets capacity
    # value(v) - the cost of "entering" v. The two exceptions (S, G) get a
    # forced 100 so they are not blocked by their value of 0, otherwise no
    # flow could leave G or arrive at S at all.
    capacity: dict[tuple, int] = {}
    for u, neighbours in adj.items():
        for v in neighbours:
            head = grid[v[0]][v[1]]
            capacity[(u, v)] = CAP_OVERRIDE if head in ("S", "G") else maze.value_of(head)

    # `residual` is the residual graph; it starts as a copy of capacity.
    # When we push f units along u -> v we do:
    #     residual[(u, v)] -= f      (less spare capacity forward)
    #     residual[(v, u)] += f      (we can now "cancel" that flow later
    #                                  by pushing back through v -> u)
    # The neighbour relation is symmetric, so (v, u) is already a key.
    residual = dict(capacity)

    max_flow = 0
    while True:
        # Edmonds-Karp: find the SHORTEST augmenting path (fewest edges) using
        # BFS over residual edges with capacity > 0. Using BFS instead of
        # plain DFS is what gives the O(V * E^2) bound; with DFS the algorithm
        # is still Ford-Fulkerson but the bound depends on integer capacities.
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
            # No path from G to S with spare capacity left. By the max-flow
            # min-cut theorem the current flow is already the maximum.
            break

        # First pass over the path: find the bottleneck = the smallest residual
        # capacity on any edge of the path. That's the largest amount we can
        # push through without overflowing any edge.
        bottleneck = float("inf")
        v = sink
        while parent[v] is not None:
            u = parent[v]
            bottleneck = min(bottleneck, residual[(u, v)])
            v = u

        # Second pass: actually push the bottleneck. Subtract on the forward
        # edge, add on the reverse edge (so future augmenting paths can
        # "undo" this decision if a better route appears).
        v = sink
        while parent[v] is not None:
            u = parent[v]
            residual[(u, v)] -= bottleneck
            residual[(v, u)] += bottleneck
            v = u

        max_flow += bottleneck

    # Reconstruct the actual flow on each forward edge by comparing the
    # original capacity to whatever is left in the residual. Positive
    # difference == net flow we ended up pushing on that edge.
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
