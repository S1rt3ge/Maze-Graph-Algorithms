# Maze Graph Algorithms

Final group project for **RTU DIP321 — Algoritmi un programmēšanas metodes**, Spring 2026.

Read a maze from a text file, build a graph from it, and solve five classic graph
problems (shortest path, min-cost path, 4-vs-8-direction comparison, max flow, MST).

## Team

| Name              | Student ID | Responsibility                                                                          |
|-------------------|------------|-----------------------------------------------------------------------------------------|
| Oleksii Burianov  | 231ADB220  | Maze parser + graph builder, **Subtask A** (BFS), **Subtask C** (4-dir vs 8-dir)        |
| Kirill Pochinchik | 231ADB132  | **Subtask B** (Dijkstra, min-cost path), **Subtask E** (MST)                            |
| Boris Arutinov   | 231ADB216  | **Subtask D** (max flow G→S, Edmonds-Karp), extension: export (GraphML/JSON/SVG/CSV)    |

## Requirements

Python 3.10+. The core subtasks use only the standard library.

## Run

```bash
python -m src.main maze_10x10_A.txt --task all
python -m src.main maze_10x10_A.txt --task A --mode 4
python -m src.main maze_10x10_A.txt --task B --cost combined --mode 8
python -m src.main maze_10x10_A.txt --task D --mode 4
```

`--mode` selects 4- or 8-directional movement.
`--cost` selects the cost model for Subtask B (`enter`, `leave`, `combined`).

## Maze format

| Symbol  | Meaning                              |
|---------|--------------------------------------|
| `S`     | start cell (value = 0)               |
| `G`     | goal cell (value = 0)                |
| `X`     | wall / blocked                       |
| `0`–`9` | passable cell with the given value   |

All rows must have the same length. Exactly one `S` and one `G`.

## Subtasks

- **A** — Shortest path S→G by number of moves (BFS).
- **B** — Minimum-cost path S→G under a chosen cost model (Dijkstra).
- **C** — Compare 4-directional and 8-directional movement on A/B and discuss.
- **D** — Maximum flow from G to S, with `capacity(u, v) = value(v)` and
  capacity into both S and G fixed at 100.
- **E** — Minimum spanning tree of the undirected graph
  (`weight(u, v) = value(u) + value(v)`), restricted to the connected component
  containing S.

Implementation files live in `src/`.

## Workflow

Each subtask is tracked as a GitHub issue. Branch per issue, PR into `main`.
