"""Extension: export the maze graph (and optional results) to common formats.

Owner: Boris Arutinov.

Formats (all written with the Python standard library only):
  - GraphML (.graphml) via xml.etree.ElementTree
  - JSON    (.json)    via json
  - CSV     (.csv)     via csv  -> writes <stem>_nodes.csv and <stem>_edges.csv
  - SVG     (.svg)     raw XML  -> maze picture with an optional highlight overlay

A vertex id is the string "r,c". Edges are undirected and de-duplicated (each
unordered pair appears once), since the maze adjacency lists both directions.

`highlight` (SVG only) is anything a subtask wants to colour:
  - a path     : list of (r, c)                -> the cells are filled
  - MST edges  : list of ((r, c), (r, c))       -> the edges are drawn
  - flow edges : list of ((r, c), (r, c), ...)  -> the edges are drawn
"""

from __future__ import annotations

import csv
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import TYPE_CHECKING

from . import maze

if TYPE_CHECKING:
    from .graph import Graph, Vertex


def _vid(v: "Vertex") -> str:
    """Vertex id used in every format: 'row,col'."""
    return f"{v[0]},{v[1]}"


def _cell_type(graph: "Graph", v: "Vertex") -> str:
    ch = graph.grid[v[0]][v[1]]
    if ch == "S":
        return "start"
    if ch == "G":
        return "goal"
    return "cell"


def _undirected_edges(graph: "Graph") -> list[tuple["Vertex", "Vertex"]]:
    """Each unordered neighbour pair once, with the smaller endpoint first."""
    seen: set = set()
    edges: list = []
    for u, neighbours in graph.adj.items():
        for v in neighbours:
            key = (u, v) if u <= v else (v, u)
            if key not in seen:
                seen.add(key)
                edges.append(key)
    return edges


def to_json(graph: "Graph", path: str | Path) -> None:
    """Write vertices (with value + type) and undirected edges as JSON."""
    data = {
        "mode": graph.mode,
        "start": list(graph.start),
        "goal": list(graph.goal),
        "vertices": [
            {
                "id": _vid(v),
                "row": v[0],
                "col": v[1],
                "value": maze.value_of(graph.grid[v[0]][v[1]]),
                "type": _cell_type(graph, v),
            }
            for v in graph.adj
        ],
        "edges": [{"source": _vid(u), "target": _vid(v)} for u, v in _undirected_edges(graph)],
    }
    Path(path).write_text(json.dumps(data, indent=2), encoding="utf-8")


def to_csv(graph: "Graph", path: str | Path) -> None:
    """Write two files next to `path`: <stem>_nodes.csv and <stem>_edges.csv."""
    p = Path(path)
    nodes_path = p.with_name(p.stem + "_nodes.csv")
    edges_path = p.with_name(p.stem + "_edges.csv")

    with nodes_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "row", "col", "value", "type"])
        for v in graph.adj:
            w.writerow([_vid(v), v[0], v[1], maze.value_of(graph.grid[v[0]][v[1]]), _cell_type(graph, v)])

    with edges_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["source", "target"])
        for u, v in _undirected_edges(graph):
            w.writerow([_vid(u), _vid(v)])


def to_graphml(graph: "Graph", path: str | Path) -> None:
    """Write a standard GraphML file with 'value' and 'type' node attributes."""
    ns = "http://graphml.graphdrawing.org/xmlns"
    root = ET.Element("graphml", {"xmlns": ns})

    # declare the node attributes ("keys") GraphML readers expect up front
    for key_id, attr_name, attr_type in (("value", "value", "int"), ("type", "type", "string")):
        ET.SubElement(root, "key", {
            "id": key_id, "for": "node", "attr.name": attr_name, "attr.type": attr_type,
        })

    graph_el = ET.SubElement(root, "graph", {"id": "maze", "edgedefault": "undirected"})
    for v in graph.adj:
        node = ET.SubElement(graph_el, "node", {"id": _vid(v)})
        ET.SubElement(node, "data", {"key": "value"}).text = str(maze.value_of(graph.grid[v[0]][v[1]]))
        ET.SubElement(node, "data", {"key": "type"}).text = _cell_type(graph, v)
    for u, v in _undirected_edges(graph):
        ET.SubElement(graph_el, "edge", {"source": _vid(u), "target": _vid(v)})

    ET.indent(root)  # pretty-print (Python 3.9+)
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)


def to_svg(graph: "Graph", path: str | Path, *, highlight=None) -> None:
    """Render the maze as an SVG grid, optionally overlaying a highlight.

    Highlighted *cells* (a path) are filled; highlighted *edges* (MST / flow)
    are drawn as lines between cell centres.
    """
    cell = 40            # pixel size of one maze cell
    rows = len(graph.grid)
    cols = len(graph.grid[0]) if rows else 0

    highlight_cells, highlight_edges = _split_highlight(highlight)

    def center(v: "Vertex") -> tuple[int, int]:
        return (v[1] * cell + cell // 2, v[0] * cell + cell // 2)

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{cols * cell}" '
        f'height="{rows * cell}" font-family="monospace" font-size="14">'
    ]
    for r in range(rows):
        for c in range(cols):
            ch = graph.grid[r][c]
            x, y = c * cell, r * cell
            if ch == "X":
                fill = "#333333"
            elif (r, c) in highlight_cells:
                fill = "#ffd54f"
            elif ch == "S":
                fill = "#66bb6a"
            elif ch == "G":
                fill = "#ef5350"
            else:
                fill = "#ffffff"
            parts.append(
                f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" '
                f'fill="{fill}" stroke="#cccccc"/>'
            )
            if ch != "X":
                parts.append(
                    f'<text x="{x + cell // 2}" y="{y + cell // 2 + 5}" '
                    f'text-anchor="middle">{ch}</text>'
                )

    for u, v in highlight_edges:
        x1, y1 = center(u)
        x2, y2 = center(v)
        parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="#1e88e5" stroke-width="3"/>'
        )

    parts.append("</svg>")
    Path(path).write_text("\n".join(parts), encoding="utf-8")


def _split_highlight(highlight) -> tuple[set, list]:
    """Sort a highlight list into (cells, edges).

    An item is an edge when its first element is itself a coordinate tuple
    (covers ((r,c),(r,c)) MST edges and ((r,c),(r,c),flow,cap) flow edges);
    otherwise it is a plain (r, c) cell.
    """
    cells: set = set()
    edges: list = []
    if not highlight:
        return cells, edges
    for item in highlight:
        if isinstance(item[0], tuple):
            edges.append((item[0], item[1]))
        else:
            cells.add(tuple(item))
    return cells, edges
