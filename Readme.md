# Finding Connected Components Using Adjacency Matrix

### Algorithm Design & Time Complexity Analysis — Mini Project

This project implements and analyzes two classical graph traversal algorithms — **Depth-First Search (DFS)** and **Breadth-First Search (BFS)** — to solve the **connected components problem** on an undirected graph represented as an **adjacency matrix**.

The primary goal of this project is not just to produce correct output, but to **formally derive, empirically verify, and compare the time and space complexity** of both algorithms.

---

## Table of Contents

1. [Problem Statement](#problem-statement)
2. [Objectives](#objectives)
3. [Weekly Work Plan](#weekly-work-plan)
4. [Project Structure](#project-structure)
5. [Algorithm Design](#algorithm-design)
6. [Time Complexity — Formal Derivation](#time-complexity--formal-derivation)
7. [Time Complexity — Practical Explanation](#time-complexity--practical-explanation)
8. [Space Complexity](#space-complexity)
9. [DFS vs BFS Comparison](#dfs-vs-bfs-comparison)
10. [Adjacency Matrix vs Adjacency List](#adjacency-matrix-vs-adjacency-list)
11. [Empirical Verification (Benchmark)](#empirical-verification-benchmark)
12. [How to Run](#how-to-run)
13. [Test Cases](#test-cases)
14. [Conclusion](#conclusion)

---

## Problem Statement

> Given an undirected graph represented as an adjacency matrix, identify all **connected components** — subsets of vertices where every vertex is reachable from every other vertex within the same subset — and report the total number of components along with the component label for each vertex.

```
Example graph:           Components found:
  0 — 1     3 — 4           {0, 1, 2}  → Component 0
      |                     {3, 4}     → Component 1
      2                     {5}        → Component 2 (isolated vertex)
              5
```

---

## Objectives

- Accept an adjacency matrix as input and validate it
- Implement a **DFS-based** algorithm to find connected components
- Implement a **BFS-based** algorithm for comparison
- Output the component label of each vertex and the total component count
- **Formally analyze** the time complexity of both algorithms (Big-O derivation)
- **Empirically benchmark** runtime growth to confirm the theoretical analysis
- Test on multiple graph types: connected, disconnected, isolated vertices

---

## Weekly Work Plan

A suggested 6-week breakdown for this mini project, mapping each objective to a concrete weekly deliverable. Adjust the pace to fit your actual submission deadline.

### Week 1 — Problem Understanding & Setup

- Study the definition of connected components and how adjacency matrices represent undirected graphs
- Set up the project repository, folder structure, and VS Code environment
- Write `graph.py` (the shared model: matrix, `visited[]`, `component[]`)
- Write `validator.py` and confirm it correctly rejects bad input (non-square, asymmetric, non-binary)
- **Deliverable:** working `Graph` class + validator with passing unit tests

### Week 2 — DFS Implementation

- Implement the recursive DFS traversal (`dfs.py`)
- Manually trace DFS on paper for a small graph (3–5 vertices) to confirm understanding before coding
- Test DFS against all three graph types: connected, disconnected, isolated vertices
- **Deliverable:** `find_components_dfs()` working and unit-tested

### Week 3 — BFS Implementation

- Implement the queue-based BFS traversal (`bfs.py`)
- Verify DFS and BFS produce identical component counts and groupings on the same input
- Write `labeler.py` to format and display output (vertex → component ID)
- **Deliverable:** `find_components_bfs()` working, output formatting complete

### Week 4 — Time Complexity Analysis (Theory)

- Derive the Big-O time complexity of DFS and BFS step-by-step (outer loop × row-scan cost)
- Derive the space complexity (visited/component arrays, recursion stack, queue)
- Compare adjacency matrix O(V²) against adjacency list O(V+E) conceptually
- Write up the formal derivation and practical explanation in the README
- **Deliverable:** complete written complexity analysis (this README's analysis sections)

### Week 5 — Empirical Verification & Benchmarking

- Implement `benchmark.py` to generate random graphs of increasing size and time both algorithms
- Run the benchmark across doubling input sizes (e.g. 10 → 320) and record the runtime ratios
- Confirm the measured ratio approaches the theoretical 4x-per-doubling signature of O(V²)
- **Deliverable:** benchmark module + recorded results table proving the theoretical analysis

### Week 6 — Testing, Polish & Submission

- Write/finish remaining unit and integration tests (`tests/`)
- Test edge cases: single vertex, two vertices, fully disconnected graph, large random graph
- Finalize README, architecture doc, and code comments
- Prepare any presentation slides or report summarizing the findings
- **Deliverable:** final GitHub repository, all tests passing, project ready to present/submit

---

## Project Structure

```
connected-components/
│
├── src/
│   ├── graph.py          # Graph model: matrix, visited[], component[]
│   ├── validator.py      # Validates matrix (square, binary, symmetric)
│   ├── dfs.py             # DFS-based component finder + complexity notes
│   ├── bfs.py             # BFS-based component finder + complexity notes
│   ├── labeler.py         # Formats and prints output
│   ├── complexity.py      # Theoretical Big-O comparison + timing
│   ├── benchmark.py        # Empirical growth-rate benchmark (proves O(V²))
│   └── main.py             # Entry point / interactive menu
│
├── tests/
│   ├── test_dfs.py
│   ├── test_bfs.py
│   ├── test_validator.py
│   ├── test_benchmark.py
│   └── test_cases.py       # Integration tests: connected/disconnected/isolated
│
├── data/                    # Sample adjacency matrices
├── docs/architecture.md     # Architecture diagram & design notes
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Algorithm Design

### DFS-based Component Finder

```python
def dfs(graph, v, comp_id):
    graph.visited[v] = True
    graph.component[v] = comp_id
    for u in range(graph.V):                 # scan full row
        if graph.matrix[v][u] == 1 and not graph.visited[u]:
            dfs(graph, u, comp_id)            # recurse

def find_components_dfs(graph):
    comp_id = 0
    for v in range(graph.V):                  # outer loop: V times
        if not graph.visited[v]:
            dfs(graph, v, comp_id)
            comp_id += 1
    return comp_id, graph.component
```

DFS picks an unvisited vertex, explores as far as possible along each branch before backtracking, and labels every vertex it touches with the same component ID. When DFS exhausts all reachable vertices, one full component has been found.

### BFS-based Component Finder

```python
def find_components_bfs(graph):
    comp_id = 0
    for v in range(graph.V):                  # outer loop: V times
        if not graph.visited[v]:
            queue = deque([v])
            graph.visited[v] = True
            while queue:
                node = queue.popleft()
                for u in range(graph.V):       # scan full row
                    if graph.matrix[node][u] == 1 and not graph.visited[u]:
                        graph.visited[u] = True
                        queue.append(u)
            comp_id += 1
    return comp_id, graph.component
```

BFS uses a queue instead of recursion, exploring all immediate neighbors before moving to the next level. The structural difference (queue vs. stack) changes the _order_ of traversal but not the _final_ result — both correctly partition the graph into connected components.

---

## Time Complexity — Formal Derivation

Let **V** = number of vertices, **E** = number of edges.

### Step-by-step derivation for DFS (and identically for BFS) on an adjacency matrix

**Step 1 — Outer loop cost.**
The outer loop in `find_components_dfs` iterates over every vertex once:

```
for v in range(V):     → runs exactly V times
```

This contributes a factor of **V**.

**Step 2 — Cost per DFS/BFS call.**
Each time DFS (or BFS) visits a vertex `v`, it must scan the entire row `matrix[v]` to discover neighbors:

```
for u in range(V):     → runs exactly V times per vertex visited
```

Since the matrix stores an entry for _every possible pair_ of vertices (whether or not an edge exists), determining the neighbors of one vertex always costs **O(V)** — regardless of how many actual edges that vertex has.

**Step 3 — Total work across all vertices.**
Across the whole traversal (DFS or BFS), **every vertex is visited exactly once** (guarded by the `visited[]` array), and each visit costs O(V) to scan its row.

```
Total operations = (number of vertices visited) × (cost per vertex)
                  = V × O(V)
                  = O(V²)
```

**Step 4 — Formal Big-O bound.**
Let `T(V)` be the running time. From Steps 1–3:

```
T(V) = V × c·V + d   (c = cost of one row-scan step, d = lower-order setup terms)
     = c·V² + d
```

By the definition of Big-O, `T(V) ∈ O(V²)` since there exist constants `c′ > 0` and `V₀` such that `T(V) ≤ c′·V²` for all `V ≥ V₀` (take `c′ = c + 1`, since the lower-order term `d` is dominated by `V²` for sufficiently large V).

```
∴  T_DFS(V) = O(V²)        T_BFS(V) = O(V²)
```

**Note on E:** with an adjacency matrix, the cost is **independent of E** — a graph with 1 edge and a graph with V(V-1)/2 edges both cost O(V²) to traverse, because the matrix representation forces a full row scan regardless of actual edge count. This is the key formal distinction from the adjacency-list representation (see below).

---

## Time Complexity — Practical Explanation

In plain terms: imagine a classroom seating chart of V students where the chart records, for every pair of students, whether they're friends (1) or not (0). To find out who vertex `v`'s friends are, you have to read v's _entire row_ — there's no shortcut, because the chart doesn't group friends together; it just lists yes/no for everyone.

- Visiting **one** vertex costs you a full row read → V checks.
- You do this for **every** vertex (V of them).
- Total work: V vertices × V checks each = **V² checks**.

This holds true whether the graph is densely connected or has almost no edges — the matrix forces you to check every cell either way. That's why **both DFS and BFS cost O(V²)** when using an adjacency matrix, even though their _traversal order_ (depth-first vs. breadth-first) is different.

---

## Space Complexity

| Component           | Space           | Why                                                     |
| ------------------- | --------------- | ------------------------------------------------------- |
| Adjacency matrix    | **O(V²)**       | Stores an entry for every pair of vertices, used or not |
| `visited[]` array   | O(V)            | One boolean per vertex                                  |
| `component[]` array | O(V)            | One label per vertex                                    |
| DFS call stack      | O(V) worst case | A straight-line graph (path) recurses V levels deep     |
| BFS queue           | O(V) worst case | A star graph enqueues up to V−1 neighbors at once       |

**Total space complexity: O(V²)** — dominated by the matrix itself, not by the traversal algorithm.

---

## DFS vs BFS Comparison

| Aspect                   | DFS                                             | BFS                                                             |
| ------------------------ | ----------------------------------------------- | --------------------------------------------------------------- |
| Data structure           | Recursive call stack                            | Explicit queue                                                  |
| Traversal order          | Goes deep before wide                           | Goes wide (level by level) before deep                          |
| Time complexity (matrix) | O(V²)                                           | O(V²)                                                           |
| Space complexity         | O(V)                                            | O(V)                                                            |
| Component count result   | Identical to BFS                                | Identical to DFS                                                |
| Best suited for          | Deep/narrow graphs, simpler code via recursion  | Shortest-path-style exploration, avoiding deep recursion limits |
| Risk                     | Stack overflow on very large V (deep recursion) | Slightly higher constant-factor overhead from queue operations  |

**Key takeaway:** for the specific task of _counting connected components_, DFS and BFS are asymptotically identical — O(V²) time, O(V) auxiliary space — and always produce the same component count and grouping. The choice between them is a matter of implementation style and constraints (e.g., recursion depth limits), not asymptotic performance.

---

## Adjacency Matrix vs Adjacency List

| Representation                      | Time (component search) | Space    | Best for                                      |
| ----------------------------------- | ----------------------- | -------- | --------------------------------------------- |
| **Adjacency Matrix** (this project) | O(V²)                   | O(V²)    | Dense graphs, frequent edge-existence queries |
| Adjacency List                      | O(V + E)                | O(V + E) | Sparse graphs, large V with few edges         |

This is the most important comparison in the analysis: **the matrix representation is the bottleneck, not the algorithm.** If E ≪ V², an adjacency list would let both DFS and BFS run in O(V + E) instead of O(V²) — a substantial improvement for sparse graphs. This project intentionally uses a matrix to study its specific complexity profile, as outlined in the objectives.

---

## Empirical Verification (Benchmark)

A formal Big-O derivation predicts behavior — `benchmark.py` **measures actual runtime** across increasing graph sizes to confirm the prediction holds.

**Method:** generate random graphs of size V = 10, 20, 40, 80, 160, 320 (each doubling the last), time DFS/BFS on each, and compute the ratio between consecutive runtimes.

```
If T(V) = O(V²), then doubling V should ~quadruple the runtime:
   T(2V) / T(V)  ≈  (2V)² / V²  =  4
```

### Sample output

```
                    EMPIRICAL GROWTH-RATE BENCHMARK
────────────────────────────────────────────────────────────────────────
  V       DFS (ms)    DFS ratio   BFS (ms)    BFS ratio
  ------  ---------   ---------   ---------   ---------
  20      0.0155      —           0.0146      —
  40      0.0447      2.88x       0.0462      3.16x
  80      0.1663      3.72x       0.1617      3.50x
  160     0.6541      3.93x       0.6270      3.88x
────────────────────────────────────────────────────────────────────────
  Expected ratio for O(V²) when V doubles: ~4.00x
```

The ratio converges toward **4.00x** as V grows — small graphs show noise from constant-factor overhead, but the trend clearly approaches the theoretical prediction, empirically confirming **O(V²)** for both algorithms.

Run it yourself:

```bash
python -m src.benchmark
```

or select option `[6]` from the interactive menu in `main.py`.

---

## How to Run

### Prerequisites

- Python 3.8+
- No external dependencies (standard library only)

### Setup

```bash
git clone https://github.com/sunitishrestha/algorithm.git
cd algorithm
python -m src.main
```

### Interactive menu

```
  [1] Enter matrix manually
  [2] Load sample: Connected graph
  [3] Load sample: Disconnected graph
  [4] Load sample: Isolated vertices
  [5] Show Big-O reference table
  [6] Run empirical growth-rate benchmark
  [0] Exit
```

### Run tests

```bash
python -m pytest tests/ -v
```

---

## Test Cases

| Test case          | Description                             | Expected components         |
| ------------------ | --------------------------------------- | --------------------------- |
| Connected graph    | Every vertex reachable from every other | 1                           |
| Disconnected graph | Multiple separate subgraphs             | matches number of subgraphs |
| Isolated vertices  | No edges at all                         | V (one per vertex)          |
| Single vertex      | 1×1 matrix                              | 1                           |
| Two vertices       | Connected / disconnected pair           | 1 / 2                       |

39 unit and integration tests cover correctness of DFS, BFS, the validator, the benchmark, and agreement between DFS and BFS results across all graph types.

---

## Conclusion

Both DFS and BFS solve the connected-components problem correctly and share the same asymptotic complexity — **O(V²) time, O(V) auxiliary space** — when implemented over an adjacency matrix. The formal derivation shows this stems directly from the O(V) cost of a row scan repeated across all V vertices, independent of edge count E. The empirical benchmark confirms this prediction, with measured runtime ratios converging toward the theoretical 4x-per-doubling signature of quadratic growth. The primary lesson of this project is that **the data structure (matrix vs. list), not the traversal strategy (DFS vs. BFS), is what determines the time complexity ceiling** for this problem.

---

## Future Improvements

- [ ] Add adjacency-list implementation to empirically compare O(V²) vs O(V+E)
- [ ] Plot benchmark results with `matplotlib` (log-log growth curve)
- [ ] Union-Find (Disjoint Set Union) as a third algorithmic approach for comparison
- [ ] File-based input from `data/*.txt`

---
