# 🔗 Finding Connected Components Using Adjacency Matrix

> **Mini Project — Algorithm Design & Time Complexity Analysis**  
> Graph Traversal with DFS & BFS | Undirected Graphs

---

## 📌 What Is This Project About?

This project focuses on **identifying connected components in an undirected graph** using an **adjacency matrix** representation. A connected component is a **sub-set of vertices where each vertex is reachable from any other vertex within the same subset**.

We implement and compare two classic graph traversal algorithms:

- **DFS (Depth-First Search)** — primary algorithm for finding components
- **BFS (Breadth-First Search)** — implemented for comparison

---

## 🎯 Objectives

```
Program accepts adjacency matrix as input
          ↓
Implement DFS-based algorithm to find connected components
          ↓
Implement BFS algorithm (for comparison)
          ↓
Output component labels for each vertex & total number of components
          ↓
Analyze time complexity for each algorithm
          ↓
Test multiple graph examples (connected, disconnected, isolated vertices)
```

---

## 🧠 Core Concept

| Term                    | Definition                                                               |
| ----------------------- | ------------------------------------------------------------------------ |
| **Graph**               | A set of vertices (nodes) connected by edges                             |
| **Undirected Graph**    | Edges have no direction; if A→B exists, B→A also exists                  |
| **Adjacency Matrix**    | An N×N matrix where `matrix[i][j] = 1` means edge between vertex i and j |
| **Connected Component** | A maximal set of vertices all reachable from each other                  |
| **DFS**                 | Explore as deep as possible before backtracking                          |
| **BFS**                 | Explore level by level using a queue                                     |

---

## 🏗️ Project Architecture

```
connected-components/
│
├── README.md                     ← You are here
├── main.py                       ← Entry point: takes input, runs both algorithms
│
├── graph/
│   ├── __init__.py
│   ├── adjacency_matrix.py       ← Graph representation & input handling
│   └── graph_utils.py            ← Helper: print matrix, display components
│
├── algorithms/
│   ├── __init__.py
│   ├── dfs.py                    ← DFS-based connected component finder
│   └── bfs.py                    ← BFS-based connected component finder
│
├── analysis/
│   ├── time_complexity.py        ← Measures actual runtime for both algorithms
│   └── complexity_notes.md       ← Theoretical complexity analysis writeup
│
└── tests/
    ├── test_connected.py         ← Fully connected graph test
    ├── test_disconnected.py      ← Graph with multiple components
    └── test_isolated.py          ← Graph with isolated (solo) vertices
```

---

## ⚙️ How It Works

### Step 1 — Input: Adjacency Matrix

```
Enter number of vertices: 5

Enter adjacency matrix (row by row):
0 1 1 0 0
1 0 1 0 0
1 1 0 0 0
0 0 0 0 1
0 0 0 1 0
```

This represents:

- Vertices 0, 1, 2 are all connected → **Component 1**
- Vertices 3, 4 are connected to each other → **Component 2**

---

### Step 2 — DFS Algorithm (Primary)

```python
def dfs(matrix, vertex, visited, component_id, labels):
    visited[vertex] = True
    labels[vertex] = component_id
    for neighbor in range(len(matrix)):
        if matrix[vertex][neighbor] == 1 and not visited[neighbor]:
            dfs(matrix, neighbor, visited, component_id, labels)

def find_components_dfs(matrix):
    n = len(matrix)
    visited = [False] * n
    labels = [-1] * n
    component_id = 0
    for v in range(n):
        if not visited[v]:
            dfs(matrix, v, visited, component_id, labels)
            component_id += 1
    return labels, component_id
```

---

### Step 3 — BFS Algorithm (For Comparison)

```python
from collections import deque

def bfs(matrix, start, visited, component_id, labels):
    queue = deque([start])
    visited[start] = True
    while queue:
        vertex = queue.popleft()
        labels[vertex] = component_id
        for neighbor in range(len(matrix)):
            if matrix[vertex][neighbor] == 1 and not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)

def find_components_bfs(matrix):
    n = len(matrix)
    visited = [False] * n
    labels = [-1] * n
    component_id = 0
    for v in range(n):
        if not visited[v]:
            bfs(matrix, v, visited, component_id, labels)
            component_id += 1
    return labels, component_id
```

---

### Step 4 — Output

```
=== DFS Result ===
Vertex 0 → Component 1
Vertex 1 → Component 1
Vertex 2 → Component 1
Vertex 3 → Component 2
Vertex 4 → Component 2

Total Connected Components: 2

=== BFS Result ===
(Same output as DFS — both algorithms find identical components)
```

---

## ⏱️ Time Complexity Analysis

| Algorithm | Time Complexity | Space Complexity | Why?                                                        |
| --------- | --------------- | ---------------- | ----------------------------------------------------------- |
| **DFS**   | O(V²)           | O(V)             | Each vertex scans the full row of N neighbors in the matrix |
| **BFS**   | O(V²)           | O(V)             | Same — every vertex inspects all N columns for neighbors    |

> **Note:** If we used an **adjacency list** instead, both would be O(V + E). The matrix forces O(V²) because we always scan every possible neighbor, even if no edge exists.

### Breakdown

```
Outer loop:           runs V times (one per unvisited vertex)
Inner DFS/BFS loop:   for each vertex, scans all V neighbors in the row
Total:                V × V = O(V²)

Space:
  visited array:      O(V)
  labels array:       O(V)
  call stack (DFS):   O(V) worst case (linear graph / deep recursion)
  queue (BFS):        O(V) worst case (star graph, all neighbors at once)
```

---

## 🧪 Test Cases to Cover

### Test 1: Fully Connected Graph

```
All vertices can reach each other → 1 component
Example (3 vertices):
  0 1 1
  1 0 1
  1 1 0
Expected: Component count = 1
```

### Test 2: Disconnected Graph

```
Two separate groups of vertices → 2 or more components
Example (4 vertices, 2 groups):
  0 1 0 0
  1 0 0 0
  0 0 0 1
  0 0 1 0
Expected: Component count = 2
```

### Test 3: Isolated Vertices

```
Some vertices have no edges at all → each is its own component
Example (3 vertices, no edges):
  0 0 0
  0 0 0
  0 0 0
Expected: Component count = 3
```

### Test 4: Mixed (Realistic Graph)

```
Some connected groups + some isolated vertices
Expected: Count = number of groups + number of isolated vertices
```

---

## 🚀 How to Run

```bash
# Clone the project
git clone https://github.com/your-username/connected-components.git
cd connected-components

# Run main program
python main.py

# Run specific tests
python tests/test_connected.py
python tests/test_disconnected.py
python tests/test_isolated.py

# Run time complexity comparison
python analysis/time_complexity.py
```

---

## 📊 What to Submit / Present

- [ ] Working code with both DFS and BFS implementations
- [ ] At least 3 test cases (connected, disconnected, isolated)
- [ ] Printed output showing component labels for each vertex
- [ ] Time complexity table comparing DFS vs BFS
- [ ] Brief explanation of **why adjacency matrix gives O(V²)**
- [ ] Optional: Graph visualization showing color-coded components

---

## 💡 Key Takeaways

1. **Both DFS and BFS** correctly find all connected components — the result is the same
2. **DFS** is simpler to implement recursively; watch out for **stack overflow** on very large graphs
3. **BFS** is safer for large graphs (no recursion depth limit)
4. **Adjacency matrix** is convenient but wastes space and time on sparse graphs — O(V²) always
5. **Adjacency list** would be more efficient for real-world sparse graphs — O(V + E)

---
