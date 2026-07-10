"""Canvas that draws the graph and its traversal states."""

from __future__ import annotations

import math
import tkinter as tk

from config import CANVAS, COMPONENTS, EDGE, NODE, TEXT


class GraphCanvas(tk.Canvas):
    def __init__(self, parent: tk.Misc) -> None:
        super().__init__(parent, bg=CANVAS, highlightthickness=0)
        self.matrix: list[list[int]] = []
        self.states: list[str] = []
        self.labels: list[int | None] = []
        self.highlight: tuple[int, int] | None = None
        self.bind("<Configure>", lambda _event: self.draw())

    def set_graph(self, matrix: list[list[int]], states: list[str], labels: list[int | None], highlight: tuple[int, int] | None = None) -> None:
        self.matrix, self.states, self.labels, self.highlight = matrix, states, labels, highlight
        self.draw()

    def draw(self) -> None:
        self.delete("all")
        if not self.matrix:
            return
        width, height = max(self.winfo_width(), 400), max(self.winfo_height(), 330)
        n = len(self.matrix)
        radius = min(width, height) * .32
        cx, cy = width / 2, height / 2
        points = [(cx + radius * math.cos(-math.pi / 2 + 2 * math.pi * i / n), cy + radius * math.sin(-math.pi / 2 + 2 * math.pi * i / n)) for i in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if self.matrix[i][j]:
                    active = self.highlight and {i, j} == set(self.highlight)
                    self.create_line(*points[i], *points[j], fill="#54ddef" if active else EDGE, width=5 if active else 3)
        for i, (x, y) in enumerate(points):
            state = self.states[i] if i < len(self.states) else "unseen"
            colors = {"unseen": (NODE, "#80a5d2"), "frontier": ("#7443bf", "#dfc5ff"), "current": ("#078daa", "#baf6ff"), "done": ("#087357", "#82e9bd")}
            fill, outline = colors[state]
            if state == "done" and self.labels[i] is not None:
                fill = COMPONENTS[self.labels[i] % len(COMPONENTS)]
            r = max(18, min(27, 220 / n))
            self.create_oval(x-r, y-r, x+r, y+r, fill=fill, outline=outline, width=3)
            self.create_text(x, y, text=chr(65 + i) if i < 26 else str(i), fill=TEXT, font=("Segoe UI", 11, "bold"))
