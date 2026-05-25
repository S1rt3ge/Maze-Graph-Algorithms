"""Generate the official output.txt for the required test maze.

Runs every subtask in both movement modes (and Subtask B in all three cost
models) and writes a clean, human-readable text report.

Run from the project root:

    python scripts/generate_output.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make `src` importable when running this file directly.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import export, graph, maze
from src import subtask_a, subtask_b, subtask_c, subtask_d, subtask_e

MAZE = ROOT / "maze_10x10_A.txt"
OUT = ROOT / "output.txt"
RULE = "=" * 72


def fmt_path(path: list[tuple[int, int]]) -> str:
    return "->".join(f"({r},{c})" for r, c in path)


def section(title: str) -> str:
    return f"\n{RULE}\n{title}\n{RULE}\n"


def render_a(grid, mode: int) -> str:
    g = graph.build(grid, mode=mode)
    r = subtask_a.solve(g)
    out = [
        f"  --- {mode}-directional ---",
        f"  movement = {mode}-directional",
        f"  reachable = {r['reachable']}",
        f"  minimum_moves = {r['moves']}",
        f"  path = {fmt_path(r['path'])}",
        "",
    ]
    return "\n".join(out)


def render_b(grid, mode: int, cost_model: str) -> str:
    g = graph.build(grid, mode=mode)
    r = subtask_b.solve(g, cost_model=cost_model)
    out = [
        f"  --- {mode}-directional, cost_model = {cost_model} ---",
        f"  movement = {mode}-directional",
        f"  cost_model = {cost_model}",
        f"  minimum_cost = {r['cost']}",
        f"  path = {fmt_path(r['path'])}",
        "",
    ]
    return "\n".join(out)


def render_c(grid) -> str:
    r = subtask_c.solve(grid)
    out = [
        f"  4-dir minimum_moves = {r['mode_4']['moves']}  path_length = {len(r['mode_4']['path'])}",
        f"  8-dir minimum_moves = {r['mode_8']['moves']}  path_length = {len(r['mode_8']['path'])}",
        "",
        "  Discussion:",
    ]
    for line in r["comparison"].splitlines():
        out.append(f"    {line}")
    out.append("")
    return "\n".join(out)


def render_d(grid, mode: int) -> str:
    r = subtask_d.solve(grid, mode=mode)
    out = [
        f"  --- {mode}-directional ---",
        f"  movement = {mode}-directional",
        f"  max_flow_G_to_S = {r['max_flow']}",
        f"  positive_flow_edges ({len(r['positive_flow_edges'])}):",
    ]
    for u, v, flow, cap in r["positive_flow_edges"]:
        out.append(f"    ({u[0]},{u[1]})->({v[0]},{v[1]}): {flow}/{cap}")
    out.append("")
    return "\n".join(out)


def render_e(grid, mode: int) -> str:
    g = graph.build(grid, mode=mode)
    r = subtask_e.solve(g)
    out = [
        f"  --- {mode}-directional ---",
        f"  movement = {mode}-directional",
        f"  goal_reachable = {r['goal_reachable']}",
        f"  component_vertices = {r['component_vertices']}",
        f"  tree_edges_count = {r['tree_edges_count']}",
        f"  mst_total_weight = {r['mst_total_weight']}",
        f"  tree_edges:",
    ]
    for u, v, w in r["tree_edges"]:
        out.append(f"    ({u[0]},{u[1]}) -- ({v[0]},{v[1]})  weight={w}")
    out.append("")
    return "\n".join(out)


def main() -> None:
    grid = maze.load(MAZE)
    g4 = graph.build(grid, mode=4)

    parts: list[str] = []
    parts.append(f"Maze: {MAZE.name}")
    parts.append(f"Grid: {len(grid)} x {len(grid[0])}")
    parts.append(f"S = {g4.start}  G = {g4.goal}")
    parts.append(f"Non-wall cells (vertices): {len(g4.adj)}")

    parts.append(section("Subtask A: Shortest path by number of moves (BFS)"))
    parts.append(render_a(grid, 4))
    parts.append(render_a(grid, 8))

    parts.append(section("Subtask B: Minimum-cost path (Dijkstra)"))
    for mode in (4, 8):
        for cm in ("enter", "leave", "combined"):
            parts.append(render_b(grid, mode, cm))

    parts.append(section("Subtask C: Movement mode comparison"))
    parts.append(render_c(grid))

    parts.append(section("Subtask D: Maximum flow G->S (Edmonds-Karp)"))
    parts.append(render_d(grid, 4))
    parts.append(render_d(grid, 8))

    parts.append(section("Subtask E: MST (Kruskal + Union-Find)"))
    parts.append(render_e(grid, 4))
    parts.append(render_e(grid, 8))

    parts.append(section("Extension: graph exports"))
    base = ROOT / "exports" / MAZE.stem
    base.parent.mkdir(exist_ok=True)
    for fmt, fn in (
        ("graphml", export.to_graphml),
        ("json",    export.to_json),
        ("csv",     export.to_csv),
    ):
        out_path = base.with_suffix(f".{fmt}")
        fn(g4, out_path)
        parts.append(f"  wrote {out_path.relative_to(ROOT)}")
    # SVG with the BFS path highlighted (Subtask A result, 4-dir).
    svg_path = base.with_suffix(".svg")
    bfs = subtask_a.solve(g4)
    export.to_svg(g4, svg_path, highlight=bfs["path"])
    parts.append(f"  wrote {svg_path.relative_to(ROOT)} (with Subtask A path highlighted)")
    parts.append("")

    OUT.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
