"""
Final Group Project: Maze Graph Algorithms
RTU DIP321 — Algoritmi un programmesanas metodes, Spring 2026.

Team:
  - Oleksii Burianov   (231ADB220)
  - Kirill Pochinchik  (231ADB132)
  - Boris Arutinov     (231ADB216)

Language: Python 3.10+

Run:
    python -m src.main <maze_file> [--task A|B|C|D|E|all]
                                   [--mode 4|8]
                                   [--cost enter|leave|combined]

Examples:
    python -m src.main maze_10x10_A.txt --task all
    python -m src.main maze_10x10_A.txt --task A --mode 4
    python -m src.main maze_10x10_A.txt --task B --cost combined --mode 8
"""

from __future__ import annotations

import argparse
from pathlib import Path

from . import export, graph, maze
from . import subtask_a, subtask_b, subtask_c, subtask_d, subtask_e


def _run(task: str, grid, g, *, mode: int, cost: str):
    if task == "A":
        return subtask_a.solve(g)
    if task == "B":
        return subtask_b.solve(g, cost_model=cost)
    if task == "C":
        return subtask_c.solve(grid)
    if task == "D":
        return subtask_d.solve(grid, mode=mode)
    if task == "E":
        return subtask_e.solve(g)
    raise ValueError(f"Unknown task: {task}")


def _highlight_from(result) -> list | None:
    """Pick something for the SVG to colour from a subtask result, if any."""
    if not isinstance(result, dict):
        return None
    return (
        result.get("path")
        or result.get("positive_flow_edges")
        or result.get("tree_edges")
        or None
    )


def _export(g, base: Path, fmt: str, *, highlight=None) -> None:
    """Write the chosen export format(s) using `base` as the file stem."""
    if fmt in ("graphml", "all"):
        export.to_graphml(g, base.with_suffix(".graphml"))
    if fmt in ("json", "all"):
        export.to_json(g, base.with_suffix(".json"))
    if fmt in ("csv", "all"):
        export.to_csv(g, base.with_suffix(".csv"))
    if fmt in ("svg", "all"):
        export.to_svg(g, base.with_suffix(".svg"), highlight=highlight)
    print(f"[export] wrote {fmt} for '{base}'")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Maze Graph Algorithms (RTU DIP321)")
    parser.add_argument("maze_file", type=Path, help="Path to maze .txt file")
    parser.add_argument(
        "--task", choices=["A", "B", "C", "D", "E", "all"], default="all",
        help="Which subtask to run",
    )
    parser.add_argument(
        "--mode", choices=["4", "8"], default="4",
        help="Movement mode (4- or 8-directional)",
    )
    parser.add_argument(
        "--cost", choices=["enter", "leave", "combined"], default="enter",
        help="Cost model for Subtask B",
    )
    parser.add_argument(
        "--export", choices=["graphml", "json", "csv", "svg", "all"], default=None,
        help="Also export the graph in this format (extension)",
    )
    parser.add_argument(
        "--export-out", type=Path, default=None,
        help="Output base path for --export (default: the maze file stem)",
    )
    args = parser.parse_args(argv)

    grid = maze.load(args.maze_file)
    g = graph.build(grid, mode=int(args.mode))

    tasks = ["A", "B", "C", "D", "E"] if args.task == "all" else [args.task]
    last_result = None
    for t in tasks:
        print(f"=== Subtask {t} ===")
        try:
            last_result = _run(t, grid, g, mode=int(args.mode), cost=args.cost)
            print(last_result)
        except NotImplementedError as exc:
            print(f"[not implemented] {exc}")
        print()

    if args.export:
        base = args.export_out or Path(args.maze_file).with_suffix("")
        # only highlight when a single task ran, so the overlay is unambiguous
        highlight = _highlight_from(last_result) if args.task != "all" else None
        _export(g, base, args.export, highlight=highlight)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
