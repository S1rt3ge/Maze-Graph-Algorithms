"""Extension: export the maze graph and subtask results to common formats.

Owner: Boris Arutinov.

Target formats:
  - GraphML (.graphml)
  - JSON    (.json)
  - SVG     (.svg)   — visualisation of the maze + path / flow / MST
  - CSV     (.csv)   — vertex list + edge list

Any external libraries used must be listed in the report.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .graph import Graph


def to_graphml(graph: "Graph", path: str | Path) -> None:
    raise NotImplementedError("export.to_graphml — see GitHub issue 'Extension: export'")


def to_json(graph: "Graph", path: str | Path) -> None:
    raise NotImplementedError("export.to_json — see GitHub issue 'Extension: export'")


def to_svg(graph: "Graph", path: str | Path, *, highlight=None) -> None:
    raise NotImplementedError("export.to_svg — see GitHub issue 'Extension: export'")


def to_csv(graph: "Graph", path: str | Path) -> None:
    raise NotImplementedError("export.to_csv — see GitHub issue 'Extension: export'")
