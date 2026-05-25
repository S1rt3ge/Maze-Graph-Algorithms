# Final Group Project Report: Maze Graph Algorithms

**Course:** RTU DIP321 - Algoritmi un programmesanas metodes
**Semester:** Spring 2026
**Maze under test:** `maze_10x10_A.txt`
**Language:** Python 3.10+ (standard library only)

## 1. Team and division of work

| Name              | Student ID | Contribution                                                                                          |
|-------------------|------------|-------------------------------------------------------------------------------------------------------|
| Oleksii Burianov  | 231ADB220  | Maze parser, graph builder, **Subtask A** (BFS), **Subtask C** (movement-mode comparison), report     |
| Kirill Pochinchik | 231ADB132  | **Subtask B** (Dijkstra) with three cost models, **Subtask E** (Kruskal MST + Union-Find)             |
| Boris Arutinov    | 231ADB216  | **Subtask D** (Edmonds-Karp max flow), **extension**: graph exports to GraphML / JSON / CSV / SVG     |

Each subtask was tracked as a GitHub issue and implemented on its own branch.
The repository lives at <https://github.com/S1rt3ge/Maze-Graph-Algorithms>.

## 2. How the maze is represented

The maze is loaded by `src/maze.py` into a 2-D list of single-character cells.
While loading, we validate four invariants:

1. The file is non-empty.
2. All rows have the same width.
3. Every cell is one of `S`, `G`, `X`, `0`-`9`.
4. There is exactly one `S` and exactly one `G`.

A helper `value_of(ch)` maps a cell character to its numeric value: `S` and
`G` return `0`, digits `'0'`-`'9'` return their integer value, and walls
(`X`) are not passable so calling `value_of('X')` raises.

## 3. How the graph is represented

`src/graph.py` exposes a `Graph` dataclass:

```python
@dataclass
class Graph:
    grid:  list[list[str]]                # original maze
    mode:  int                            # 4 or 8
    adj:   dict[Vertex, list[Vertex]]     # adjacency list keyed by (row, col)
    start: Vertex                         # location of 'S'
    goal:  Vertex                         # location of 'G'
```

- **Vertices** are every non-wall cell, identified by `(row, col)`.
- **Edges** are between cells reachable by one move. Two movement modes are
  supported:
  - `mode = 4`: up, down, left, right
  - `mode = 8`: the four cardinals plus the four diagonals
- The adjacency list is symmetric, so the same structure also serves as the
  residual-graph adjacency for Subtask D (max flow).

For the required `maze_10x10_A.txt` this gives **76 vertices**, with
**97 undirected edges** under 4-dir and **171 undirected edges** under 8-dir.

## 4. Subtasks

### Subtask A: shortest path by number of moves (Oleksii)

**Approach.** Plain breadth-first search from `S`. Each visited cell records
its predecessor in a `parent` dictionary. Because every legal move has unit
cost, BFS layer-by-layer reaches `G` in the minimum number of edges. The
search stops as soon as `G` is popped from the queue, and the path is
reconstructed by walking `parent` backwards from `G` to `S`.

**Complexity.** Time `O(V + E)`. Space `O(V)` (parent map + BFS queue).

**Results on the test maze.**

| Mode | Minimum moves |
|------|---------------|
| 4-dir | 18           |
| 8-dir | 11           |

### Subtask B: minimum-cost path (Kirill)

**Approach.** Dijkstra with a binary min-heap (`heapq`). All cell values are
non-negative (`0`-`9`), which is exactly when Dijkstra is guaranteed to
work. We keep a `dist` map and a `parent` map; the algorithm settles `G`
and reconstructs the path the same way as Subtask A. Stale heap entries
(left over from an earlier relaxation of the same vertex) are skipped with
the usual `cost > dist[u]` check.

Three cost models are supported per the spec:

- `enter`:    `cost(u -> v) = value(v)`
- `leave`:    `cost(u -> v) = value(u)`
- `combined`: `cost(u -> v) = value(u) + value(v)`

For every model, `value(S) = value(G) = 0`.

**Complexity.** Time `O((V + E) log V)`. Space `O(V)`.

**Results on the test maze.**

| Mode  | Model     | Minimum cost |
|-------|-----------|--------------|
| 4-dir | enter     | 26           |
| 4-dir | leave     | 26           |
| 4-dir | combined  | 52           |
| 8-dir | enter     | 18           |
| 8-dir | leave     | 18           |
| 8-dir | combined  | 36           |

For this maze `enter` and `leave` happen to give the same total, because
the cheapest route uses cells with the same value distribution either way
the cost is read. The `combined` model is exactly the sum of the two, as
expected by the formulas above.

### Subtask C: 4-dir vs 8-dir comparison (Oleksii)

**Approach.** Build the graph in both modes, run Subtask A on each, and
synthesise a short discussion comparing the results.

**Complexity.** Same as Subtask A, executed twice: time `O(V + E)`,
space `O(V)`.

**Discussion (the three required questions).**

1. **Does diagonal movement change the shortest path?** Yes. On this maze
   the minimum number of moves drops from **18 to 11**. Diagonals create
   direct edges across the corners of the wall blocks (for example
   `(2,0) -> (3,1) -> (4,2)` short-cuts what is a four-step staircase in
   4-dir), so anywhere a corridor turns through a corner an 8-dir path can
   save one step.
2. **Does diagonal movement change the cheapest path?** Yes. With diagonals
   Dijkstra picks an entirely different route through the upper rows: the
   4-dir `enter` cost is 26 but the 8-dir `enter` cost is 18. A diagonal
   traverses different cells whose values may be higher or lower than the
   cells of the 4-dir detour; for this maze they happen to be cheaper.
3. **Can the fewest-moves path differ from the lowest-cost path?** Yes.
   BFS treats every move as equal, while Dijkstra sums cell values. On the
   test maze the 4-dir BFS path costs 51 in the `enter` model, but
   Dijkstra finds a path costing only 26 by taking a longer route through
   cheaper cells.

### Subtask D: maximum flow G -> S (Boris)

**Approach.** Edmonds-Karp = Ford-Fulkerson with BFS for augmenting paths.

- Source = `G`, sink = `S`.
- `capacity(u, v) = value(v)` for normal cells; edges entering `S` or `G`
  have capacity `100` (the spec override, so the source/sink are not blocked
  by their value of 0).
- A single dict `residual[(u, v)]` is initialised from the capacity table.
  Pushing `f` units along `u -> v` does
  `residual[(u,v)] -= f; residual[(v,u)] += f`. Because the maze adjacency
  is symmetric both directions are already keys, so this one dict represents
  both forward capacity and back-flow potential.
- BFS finds a shortest residual path, we compute the bottleneck along it,
  and we augment until no path remains.

**Complexity.** Time `O(V * E^2)` (Edmonds-Karp bound). Space `O(V + E)`.

**Results on the test maze.**

| Mode  | Max flow |
|-------|----------|
| 4-dir | 1        |
| 8-dir | 4        |

The 4-dir answer surprised us at first. The two edges out of `G` each have
capacity 1, so the upper bound is 2. The real bottleneck is topological:
rows 0-2 are split by walls in column 5 into two disjoint quadrants, and
only **two** cells connect the upper half to the lower half: `(3,1)` and
`(3,9)`. The `(3,9)` route leads to the upper-right quadrant
`(0,6)..(0,9)`, which is itself *not* connected to `S = (0,0)` because
the row-0 wall at `(0,5)` blocks it. So every unit of flow has to pass
through `(3,1) -> (2,1)`, whose capacity is `value((2,1)) = 1`. That
single edge is the global min cut, so by max-flow / min-cut max flow = 1.

With diagonals (8-dir) the wall corners stop separating the components and
four parallel augmenting paths become available.

### Subtask E: minimum spanning tree (Kirill)

**Approach.** Kruskal with a Disjoint-Set Union (Union-Find), using path
halving in `find` and union-by-rank in `union`.

Steps:
1. BFS from `S` to find every vertex in `S`'s connected component.
2. Collect every undirected edge inside that component, using a `frozenset`
   key so each pair is added only once.
3. Sort the edges by weight (`weight(u, v) = value(u) + value(v)`,
   `value(S) = value(G) = 0`).
4. Walk the sorted edges and accept one iff `union(u, v)` succeeds (the
   endpoints were in different sets). Stop after `|V| - 1` edges have been
   accepted, since that is exactly the size of any spanning tree.

**Complexity.** Time `O(E log E)` - the sort dominates; Union-Find ops are
effectively `O(alpha(V))`. Space `O(V + E)`.

**Results on the test maze.**

| Mode  | MST weight | Vertices | Edges | Goal reachable |
|-------|------------|----------|-------|----------------|
| 4-dir | 390        | 76       | 75    | yes            |
| 8-dir | 144        | 76       | 75    | yes            |

The 8-dir MST is much lighter because diagonals offer more candidate
edges, so Kruskal can skip the high-value cells almost entirely.

## 5. Extension: graph exports (Boris)

`src/export.py` writes the graph to four documented formats, using **only
the Python standard library**:

| Format   | Module                     | What is written                                              |
|----------|----------------------------|--------------------------------------------------------------|
| GraphML  | `xml.etree.ElementTree`    | XML with `value` and `type` node attributes                  |
| JSON     | `json`                     | `vertices` (with `value`, `type`) + `edges` arrays           |
| CSV      | `csv`                      | Two files: `<stem>_nodes.csv` and `<stem>_edges.csv`         |
| SVG      | raw XML                    | A picture of the maze, cells filled by type                  |

Vertex IDs are the string `"r,c"`. Edges are undirected and de-duplicated.
The SVG renderer accepts an optional `highlight` argument: a list of `(r, c)`
cells (e.g. a path) gets filled in yellow, and a list of edges (such as
`((r,c),(r,c),...)`) gets drawn as blue lines between cell centres, so the
same renderer can visualise paths from A/B, the MST from E, and the
positive flow from D.

The exported artefacts live under `exports/`:
`maze_10x10_A.graphml`, `maze_10x10_A.json`, `maze_10x10_A_nodes.csv`,
`maze_10x10_A_edges.csv`, and `maze_10x10_A.svg` (with the BFS path
highlighted).

## 6. How to reproduce the results

```bash
# run a single subtask
python -m src.main maze_10x10_A.txt --task A --mode 4
python -m src.main maze_10x10_A.txt --task B --cost combined --mode 8
python -m src.main maze_10x10_A.txt --task D --mode 4
python -m src.main maze_10x10_A.txt --task E --mode 8

# run everything and write the official artefacts
python scripts/generate_output.py
```

`scripts/generate_output.py` is what produced the submitted `output.txt`.

## 7. Discussion of results

- BFS and Dijkstra agree on the endpoints of the path but pick different
  middles whenever cell values vary, which is exactly what you'd expect.
- Diagonals help everywhere: they cut roughly a third off the BFS length
  and roughly a third off the Dijkstra cost, and they more than halve the
  MST weight.
- The 4-dir max-flow of 1 is the most counter-intuitive result; it is a
  good example of graph topology dominating local capacities. The min-cut
  explanation in section 4-D shows why.

## 8. Known limitations

- Subtask B uses `cost = -1` to mean "goal unreachable", while Subtask A
  uses `moves = None`. The two are consistent within each subtask but
  differ between them. The test maze never triggers this branch.
- The SVG renderer is deliberately simple: it uses one fixed cell size and
  does no auto-scaling for very large mazes. For inputs near 100x100 the
  resulting file is still readable but quite large.
- We did not write automated tests. Verification was done by running each
  subtask on the required maze, cross-checking with `Subtask C`, and
  tracing the surprising 4-dir max-flow result by hand to confirm
  `max_flow = 1` matches the min cut.

## 9. AI / tool usage disclosure

We used an AI assistant (Claude) interactively during development to help
with:

- bootstrapping the repository skeleton and the GitHub issue layout,
- reviewing pull requests for correctness (in particular, tracing the
  4-dir max-flow result by hand to confirm `max_flow = 1` is correct
  rather than a bug),
- drafting parts of this report and some of the docstrings.

All algorithmic decisions and the algorithm implementations themselves
were owned by the team members listed in section 1. No external library
implementations of BFS, Dijkstra, Edmonds-Karp, or Kruskal were used; every
algorithm in this project is written from scratch on top of the Python
standard library, as required by the spec.
