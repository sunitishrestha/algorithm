Connected Components Lab

A Python desktop mini project for finding connected components in an **undirected graph** using an adjacency matrix. It provides an animated visual comparison of DFS and BFS.

## Features

- Editable adjacency matrix with green `1` cells for connected edges and dark `0` cells for no edge.
- DFS and BFS animation with Run, Step, Reset, and speed controls.
- **Run DFS → BFS** button: completes DFS first, then automatically starts BFS.
- Clear live badge: `RUNNING DFS`, `RUNNING BFS`, or complete status.
- Component count, vertices, edges, visited vertices, and current traversal event.
- User-defined adjacency matrices from 1 to 12 vertices.
- Matrix-size control for adding or reducing vertices.
- Example graphs: mixed components, fully connected, isolated vertices, and three components.
- Input-specific complexity information.

## Requirements

- Python 3.10 or newer
- Tkinter (included with the normal Windows Python installer)
- Visual Studio Code with the Microsoft **Python** extension, recommended

No third-party Python packages are needed.

## Run in VS Code

1. Open the `connected-components-python-project` folder in VS Code.
2. Select a Python interpreter if VS Code asks.
3. Press `F5` and select **Run Connected Components Lab**.

Or use the VS Code terminal:

```powershell
python main.py
```

The app starts maximized. You can restore or resize it; the matrix section has a vertical scrollbar so all rows remain available.

## Project files

```text
connected-components-python-project/
├── main.py             # Main dashboard, controls, results, and animation loop
├── algorithms.py       # DFS and BFS event generation
├── graph_model.py      # Matrix data, validation, presets, and resizing
├── graph_canvas.py     # Canvas graph drawing and traversal colors
├── matrix_dialog.py    # User matrix import dialog
├── config.py           # Shared colors and visual settings
├── README.md           # Project guide
└── .vscode/
    └── launch.json     # VS Code F5 configuration
```

## How to use

1. Choose an example graph, click matrix cells, change the matrix size, or click **Import user matrix**.
2. Choose **DFS** or **BFS**.
3. Click **Run** for automatic animation, or **Step** to move one traversal event at a time.
4. Click **Run DFS → BFS** to animate DFS completely and then animate BFS automatically.
5. Watch the graph, status badge, current event, component labels, and complexity panel.

## User adjacency-matrix input

Click **Import user matrix** and enter one row on each line. Values must be `0` or `1`, separated by spaces.

Example with two components: `A-B-C` and `D` isolated.

```text
0 1 0 0
1 0 1 0
0 1 0 0
0 0 0 0
```

Input rules:

- The matrix must be square: rows = columns.
- Use only `0` and `1`.
- Every diagonal value must be `0`.
- The matrix must be symmetric because the graph is undirected. For example, if `A-B` is `1`, then `B-A` must also be `1`.

## Complexity

With an adjacency matrix containing `V` vertices:

| Algorithm | Time complexity | Extra space |
| --------- | --------------: | ----------: |
| DFS       |         `O(V²)` |      `O(V)` |
| BFS       |         `O(V²)` |      `O(V)` |

Both algorithms scan adjacency-matrix rows, so each can inspect up to `V × V` cells. The UI calculates this number for the current matrix, and also shows the number of undirected edges `E` and matrix edge entries `2E`.
