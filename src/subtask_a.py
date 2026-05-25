"""Subtask A: shortest path from S to G by number of moves (BFS).

Owner: Oleksii Burianov.

Every legal move has cost 1, so BFS layer-by-layer gives the minimum number
of moves and a corresponding path. Reconstruct the path with a `parent` map.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .graph import Graph


def solve(graph: "Graph") -> dict:
    """Return {'moves': int, 'path': [(r, c), ...], 'mode': '4' | '8'}.

    TODO: BFS from graph.start; stop at graph.goal; reconstruct path.
    """
    raise NotImplementedError("Subtask A — see GitHub issue 'Subtask A: BFS'")
