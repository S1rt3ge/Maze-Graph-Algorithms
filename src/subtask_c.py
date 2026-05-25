"""Subtask C: compare 4-directional and 8-directional movement.

Owner: Oleksii Burianov.

Runs Subtask A (BFS by number of moves) under both movement modes and reports
how the result changes. Subtask B (cheapest path) is not required here but is
discussed in the explanation text so the report can answer the spec's three
questions in full.

Complexity (same as Subtask A, but executed twice):
  time  - O(V + E)
  space - O(V)
"""

from __future__ import annotations

from . import graph, subtask_a


def solve(grid: list[list[str]]) -> dict:
    """Return BFS results for both movement modes and a comparison summary.

    Returned dict:
        mode_4     : dict   - subtask_a.solve(graph.build(grid, 4))
        mode_8     : dict   - subtask_a.solve(graph.build(grid, 8))
        comparison : str    - human-readable summary answering the spec's questions
    """
    g4 = graph.build(grid, mode=4)
    g8 = graph.build(grid, mode=8)
    res4 = subtask_a.solve(g4)
    res8 = subtask_a.solve(g8)

    lines: list[str] = [
        f"4-dir shortest: moves={res4['moves']} reachable={res4['reachable']}",
        f"8-dir shortest: moves={res8['moves']} reachable={res8['reachable']}",
    ]

    if res4["reachable"] and res8["reachable"]:
        diff = res4["moves"] - res8["moves"]
        if diff > 0:
            lines.append(
                f"Diagonals shorten the path by {diff} moves: "
                "they create direct edges across wall corners, "
                "skipping the detours 4-dir movement is forced to take."
            )
        elif diff == 0:
            lines.append(
                "Both modes find paths of the same length. "
                "Diagonals exist but do not unlock a shorter route on this maze."
            )
        else:
            lines.append(
                f"Unexpected: 4-dir is {-diff} moves shorter. "
                "This should not happen because 8-dir is a strict superset "
                "of 4-dir moves; check the graph construction."
            )
    elif res4["reachable"] and not res8["reachable"]:
        lines.append(
            "G is reachable in 4-dir but not in 8-dir. "
            "This should not happen: every 4-dir edge also exists in 8-dir."
        )
    elif res8["reachable"] and not res4["reachable"]:
        lines.append(
            "G is reachable only with diagonals. Wall placement creates a "
            "thin barrier that 4-dir movement cannot cross."
        )
    else:
        lines.append("G is unreachable under both movement modes.")

    lines.append(
        "Fewest-moves and lowest-cost paths can differ: BFS treats every move "
        "as equal, while Dijkstra (Subtask B) sums cell values, so a longer "
        "route through cheap cells can beat a short route through expensive ones."
    )

    return {
        "mode_4": res4,
        "mode_8": res8,
        "comparison": "\n".join(lines),
    }
