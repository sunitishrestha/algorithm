"""Graph data, presets, and adjacency-matrix validation."""

from __future__ import annotations


PRESETS = {
    "Mixed components": [[0, 1], [1, 2], [2, 0], [3, 4], [5, 6]],
    "Fully connected": [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6]],
    "Isolated vertices": [[0, 1], [3, 4]],
    "Three components": [[0, 1], [1, 2], [3, 4]],
}


class GraphModel:
    def __init__(self, vertices: int = 7) -> None:
        self.matrix = [[0] * vertices for _ in range(vertices)]
        self.load_preset("Mixed components")

    @property
    def vertices(self) -> int:
        return len(self.matrix)

    @property
    def edge_count(self) -> int:
        return sum(self.matrix[i][j] for i in range(self.vertices) for j in range(i + 1, self.vertices))

    def toggle(self, i: int, j: int) -> None:
        if i == j:
            return
        value = 1 - self.matrix[i][j]
        self.matrix[i][j] = self.matrix[j][i] = value

    def clear(self) -> None:
        self.matrix = [[0] * self.vertices for _ in range(self.vertices)]

    def resize(self, vertices: int) -> None:
        """Resize the matrix, preserving edges shared by the old/new sizes."""
        if not 1 <= vertices <= 12:
            raise ValueError("Choose between 1 and 12 vertices.")
        resized = [[0] * vertices for _ in range(vertices)]
        shared = min(vertices, self.vertices)
        for i in range(shared):
            for j in range(shared):
                resized[i][j] = self.matrix[i][j]
        self.matrix = resized

    def load_preset(self, name: str) -> None:
        edges = PRESETS[name]
        self.matrix = [[0] * 7 for _ in range(7)]
        for left, right in edges:
            self.matrix[left][right] = self.matrix[right][left] = 1

    def set_matrix_from_text(self, text: str) -> None:
        try:
            rows = [[int(value) for value in line.split()] for line in text.strip().splitlines() if line.strip()]
        except ValueError as error:
            raise ValueError("Use only 0 and 1, separated by spaces.") from error
        if not rows:
            raise ValueError("Enter at least one matrix row.")
        size = len(rows)
        if size > 12:
            raise ValueError("Use at most 12 vertices so the graph remains readable.")
        if any(len(row) != size for row in rows):
            raise ValueError("The matrix must be square.")
        for i in range(size):
            if rows[i][i] != 0:
                raise ValueError("Diagonal values must be 0.")
            for j in range(size):
                if rows[i][j] not in (0, 1) or rows[i][j] != rows[j][i]:
                    raise ValueError("Use a symmetric 0/1 matrix for an undirected graph.")
        self.matrix = rows
