"""Run the Connected Components Lab desktop project."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from algorithms import traversal_events
from config import ACCENT, BG, BORDER, MUTED, PANEL, PURPLE, TEXT
from graph_canvas import GraphCanvas
from graph_model import GraphModel, PRESETS
from matrix_dialog import MatrixDialog


class ConnectedComponentsLab(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Connected Components Lab")
        self.geometry("1420x860")
        self.minsize(1060, 700)
        self.configure(bg=BG)
        # Start maximized on Windows so the complete dashboard is visible.
        # The app still supports restoring and resizing the normal window.
        try:
            self.state("zoomed")
        except tk.TclError:
            pass
        self.model = GraphModel()
        self.algorithm = "DFS"
        self.states: list[str] = []
        self.labels: list[int | None] = []
        self.events: list[dict] = []
        self.index = 0
        self.timer = None
        self._style()
        self._build()
        self.reset()

    def _style(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", background="#193558", foreground=TEXT, bordercolor=BORDER, padding=9, font=("Segoe UI", 11))
        style.map("TButton", background=[("active", "#254a78")])
        style.configure("Accent.TButton", background="#1779d0", foreground="white")
        style.configure("Active.TButton", background=PURPLE, foreground="white")
        style.configure("TCombobox", fieldbackground="#193558", background="#193558", foreground=TEXT, arrowcolor=TEXT)

    def panel(self, parent: tk.Misc) -> tk.Frame:
        return tk.Frame(parent, bg=PANEL, highlightbackground=BORDER, highlightthickness=1, padx=18, pady=18)

    def _build(self) -> None:
        tk.Label(self, text="Connected Components Lab", bg=BG, fg=TEXT, font=("Segoe UI", 31, "bold")).pack(anchor="w", padx=38, pady=(24, 0))
        tk.Label(self, text="Explore how DFS and BFS label every disconnected part of an undirected graph.", bg=BG, fg=MUTED, font=("Segoe UI", 14)).pack(anchor="w", padx=38, pady=(3, 20))
        root = tk.Frame(self, bg=BG)
        root.pack(fill="both", expand=True, padx=34, pady=(0, 30))
        root.grid_columnconfigure(1, weight=1)
        root.grid_rowconfigure(0, weight=1)

        left = self.panel(root); left.grid(row=0, column=0, sticky="nsw", padx=(0, 20))
        center = self.panel(root); center.grid(row=0, column=1, sticky="nsew", padx=(0, 20))
        right = tk.Frame(root, bg=BG); right.grid(row=0, column=2, sticky="nsew")
        self._left(left); self._center(center); self._right(right)

    def _left(self, parent: tk.Frame) -> None:
        tk.Label(parent, text="Graph controls", bg=PANEL, fg=TEXT, font=("Segoe UI", 14, "bold")).pack(anchor="w")
        tk.Label(parent, text="Example graph", bg=PANEL, fg=TEXT, font=("Segoe UI", 11)).pack(anchor="w", pady=(18, 3))
        self.preset = tk.StringVar(value="Mixed components")
        box = ttk.Combobox(parent, textvariable=self.preset, values=list(PRESETS), state="readonly", width=23); box.pack(fill="x"); box.bind("<<ComboboxSelected>>", lambda _e: self.load_preset())
        ttk.Button(parent, text="Import user matrix", command=self.import_matrix).pack(fill="x", pady=(9, 0))
        ttk.Button(parent, text="Clear edges", command=self.clear).pack(fill="x", pady=(7, 0))
        tk.Label(parent, text="Matrix size (vertices)", bg=PANEL, fg=TEXT, font=("Segoe UI", 11)).pack(anchor="w", pady=(14, 3))
        size_row = tk.Frame(parent, bg=PANEL); size_row.pack(fill="x")
        self.size_var = tk.StringVar(value=str(self.model.vertices))
        self.size_box = tk.Spinbox(size_row, from_=1, to=12, textvariable=self.size_var, width=7, bg="#0d1d33", fg=TEXT, buttonbackground="#193558", insertbackground="white", relief="flat", font=("Segoe UI", 11))
        self.size_box.pack(side="left")
        ttk.Button(size_row, text="Apply size", command=self.resize_matrix).pack(side="left", padx=(8, 0))
        tk.Label(parent, text="TRAVERSAL ALGORITHM", bg=PANEL, fg=MUTED, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(25, 8))
        row = tk.Frame(parent, bg=PANEL); row.pack(fill="x")
        self.dfs_btn = ttk.Button(row, text="DFS", command=lambda: self.choose("DFS")); self.dfs_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
        self.bfs_btn = ttk.Button(row, text="BFS", command=lambda: self.choose("BFS")); self.bfs_btn.pack(side="left", fill="x", expand=True, padx=(4, 0))
        tk.Label(parent, text="ANIMATION", bg=PANEL, fg=MUTED, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(25, 8))
        row = tk.Frame(parent, bg=PANEL); row.pack(fill="x")
        ttk.Button(row, text="▶ Run", style="Accent.TButton", command=self.run).pack(side="left", padx=(0, 5))
        ttk.Button(row, text="Step", command=self.step).pack(side="left", padx=5)
        ttk.Button(row, text="Reset", command=self.reset).pack(side="left", padx=5)
        ttk.Button(parent, text="Run DFS → BFS", command=self.run_both).pack(fill="x", pady=(8, 0))
        tk.Label(parent, text="Speed", bg=PANEL, fg=MUTED).pack(anchor="w", pady=(14, 0))
        self.speed = tk.Scale(parent, from_=150, to=1200, orient="horizontal", showvalue=False, bg=PANEL, fg=TEXT, troughcolor="#f2f2f2", highlightthickness=0); self.speed.set(650); self.speed.pack(fill="x")
        tk.Label(parent, text="ADJACENCY MATRIX", bg=PANEL, fg=MUTED, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(13, 7))
        matrix_shell = tk.Frame(parent, bg=PANEL)
        matrix_shell.pack(fill="x")
        self.matrix_view = tk.Canvas(matrix_shell, bg=PANEL, highlightthickness=0, height=245, width=285)
        self.matrix_scroll = tk.Scrollbar(matrix_shell, orient="vertical", command=self.matrix_view.yview)
        self.matrix_view.configure(yscrollcommand=self.matrix_scroll.set)
        self.matrix_view.pack(side="left", fill="both", expand=True)
        self.matrix_scroll.pack(side="right", fill="y")
        self.matrix_frame = tk.Frame(self.matrix_view, bg=PANEL)
        self.matrix_window = self.matrix_view.create_window((0, 0), window=self.matrix_frame, anchor="nw")
        self.matrix_frame.bind("<Configure>", self._resize_matrix_scroll_region)
        self.matrix_view.bind("<MouseWheel>", self._scroll_matrix)
        self.matrix_note = tk.Label(parent, text="Green 1 = connected edge. Dark 0 = no edge. Click a cell to change it.", bg=PANEL, fg=MUTED, wraplength=260, justify="left"); self.matrix_note.pack(anchor="w", pady=(8, 0))

    def _resize_matrix_scroll_region(self, _event=None) -> None:
        """Keep all matrix rows scrollable, including after a size change."""
        self.matrix_view.configure(scrollregion=self.matrix_view.bbox("all"))

    def _scroll_matrix(self, event) -> None:
        self.matrix_view.yview_scroll(int(-event.delta / 120), "units")

    def _center(self, parent: tk.Frame) -> None:
        heading = tk.Frame(parent, bg=PANEL)
        heading.pack(fill="x", pady=(0, 12))
        tk.Label(heading, text="Graph traversal animation", bg=PANEL, fg=TEXT, font=("Segoe UI", 14, "bold")).pack(side="left")
        self.running_badge = tk.Label(heading, text="READY", bg="#193558", fg=MUTED, font=("Segoe UI", 10, "bold"), padx=11, pady=5)
        self.running_badge.pack(side="right")
        self.canvas = GraphCanvas(parent); self.canvas.pack(fill="both", expand=True)
        self.status = tk.Label(parent, text="Ready. Choose DFS or BFS, then run.", bg="#0a1930", fg=MUTED, font=("Segoe UI", 11), anchor="w", padx=14, pady=12); self.status.pack(fill="x", pady=(12, 0))

    def _right(self, parent: tk.Frame) -> None:
        result = self.panel(parent); result.pack(fill="x")
        tk.Label(result, text="Results", bg=PANEL, fg=TEXT, font=("Segoe UI", 14, "bold")).pack(anchor="w")
        self.metrics = {}
        for label in ("Components found", "Vertices", "Edges", "Visited"):
            row = tk.Frame(result, bg=PANEL); row.pack(fill="x", pady=10)
            tk.Label(row, text=label, bg=PANEL, fg=MUTED, font=("Segoe UI", 11)).pack(side="left")
            value = tk.Label(row, text="—", bg=PANEL, fg=TEXT, font=("Segoe UI", 13, "bold")); value.pack(side="right"); self.metrics[label] = value
        event = self.panel(parent); event.pack(fill="x", pady=18)
        tk.Label(event, text="Current event", bg=PANEL, fg=TEXT, font=("Segoe UI", 14, "bold")).pack(anchor="w")
        self.event_text = tk.Label(event, text="Press Run to animate component discovery.", bg=PANEL, fg=MUTED, wraplength=230, justify="left", font=("Segoe UI", 11)); self.event_text.pack(anchor="w", pady=(14, 0))
        legend = self.panel(parent); legend.pack(fill="x")
        tk.Label(legend, text="State legend", bg=PANEL, fg=TEXT, font=("Segoe UI", 14, "bold")).pack(anchor="w")
        for text, color in (("Unvisited", "#183557"), ("Frontier (stack / queue)", "#7443bf"), ("Current vertex", "#078daa"), ("Completed", "#087357")):
            line = tk.Frame(legend, bg=PANEL); line.pack(anchor="w", pady=7)
            tk.Label(line, text="●", bg=PANEL, fg=color, font=("Segoe UI", 14)).pack(side="left")
            tk.Label(line, text=text, bg=PANEL, fg=MUTED, font=("Segoe UI", 11)).pack(side="left", padx=8)
        complexity = self.panel(parent); complexity.pack(fill="x", pady=(18, 0))
        tk.Label(complexity, text="Time complexity", bg=PANEL, fg=TEXT, font=("Segoe UI", 14, "bold")).pack(anchor="w")
        self.complexity_text = tk.Label(complexity, text="", bg=PANEL, fg=MUTED, justify="left", anchor="w", wraplength=230, font=("Segoe UI", 10))
        self.complexity_text.pack(fill="x", pady=(9, 0))

    def render_matrix(self) -> None:
        for child in self.matrix_frame.winfo_children(): child.destroy()
        names = [chr(65+i) for i in range(self.model.vertices)]
        tk.Label(self.matrix_frame, text="", bg=PANEL).grid(row=0, column=0)
        for j, name in enumerate(names): tk.Label(self.matrix_frame, text=name, bg=PANEL, fg=MUTED, width=3).grid(row=0, column=j+1)
        for i, name in enumerate(names):
            tk.Label(self.matrix_frame, text=name, bg=PANEL, fg=MUTED, width=3).grid(row=i+1, column=0)
            for j in range(self.model.vertices):
                if i == j:
                    cell = tk.Label(self.matrix_frame, text="–", width=3, height=1, bg="#32455f", fg="#a7b8d5")
                else:
                    connected = self.model.matrix[i][j] == 1
                    cell = tk.Button(
                        self.matrix_frame,
                        text="1" if connected else "0",
                        width=2,
                        height=1,
                        relief="flat",
                        cursor="hand2",
                        bg="#0b7b59" if connected else "#0d1d33",
                        fg="white" if connected else "#788ba8",
                        activebackground="#16a36f" if connected else "#1a304b",
                        activeforeground="white",
                        command=lambda x=i, y=j: self.toggle(x, y),
                    )
                cell.grid(row=i+1, column=j+1, padx=2, pady=2)
        self.matrix_frame.update_idletasks()
        self._resize_matrix_scroll_region()

    def choose(self, algorithm: str) -> None:
        self.algorithm = algorithm; self.dfs_btn.configure(style="Active.TButton" if algorithm == "DFS" else "TButton"); self.bfs_btn.configure(style="Active.TButton" if algorithm == "BFS" else "TButton"); self.reset()

    def load_preset(self) -> None: self.model.load_preset(self.preset.get()); self.size_var.set(str(self.model.vertices)); self.reset()
    def clear(self) -> None: self.model.clear(); self.reset()
    def toggle(self, i: int, j: int) -> None: self.model.toggle(i, j); self.reset()
    def import_matrix(self) -> None: MatrixDialog(self, self.apply_matrix)
    def apply_matrix(self, dialog, text: str) -> None:
        try: self.model.set_matrix_from_text(text)
        except ValueError as error: messagebox.showerror("Invalid matrix", str(error), parent=dialog); return
        dialog.destroy(); self.size_var.set(str(self.model.vertices)); self.reset()

    def resize_matrix(self) -> None:
        try:
            size = int(self.size_var.get())
            self.model.resize(size)
        except ValueError:
            messagebox.showerror("Invalid size", "Enter a whole number from 1 to 12.", parent=self)
            self.size_var.set(str(self.model.vertices))
            return
        self.reset()

    def reset(self) -> None:
        if self.timer: self.after_cancel(self.timer); self.timer = None
        self.events, self.index = [], 0; self.states = ["unseen"] * self.model.vertices; self.labels = [None] * self.model.vertices
        self.status.configure(text="Ready. Choose DFS or BFS, then run."); self.event_text.configure(text="Press Run to animate component discovery.")
        self.running_badge.configure(text="READY", bg="#193558", fg=MUTED)
        self.render_matrix(); self.refresh()

    def run(self) -> None:
        if not self.events:
            self.events = traversal_events(self.model.matrix, self.algorithm)
            self.running_badge.configure(text=f"RUNNING {self.algorithm}", bg=PURPLE if self.algorithm == "DFS" else "#087e9c", fg="white")
            self.status.configure(text=f"Running {self.algorithm} on the current adjacency matrix...")
        self.step(auto=True)

    def run_both(self) -> None:
        """Animate DFS completely, reset the states, then animate BFS."""
        self.reset()
        self.algorithm = "DFS"
        self.dfs_btn.configure(style="Active.TButton")
        self.bfs_btn.configure(style="TButton")
        self.running_badge.configure(text="RUNNING DFS", bg=PURPLE, fg="white")
        self.status.configure(text="Running DFS first; BFS will start automatically after DFS completes.")
        self.events = traversal_events(self.model.matrix, "DFS")
        self.events.append({"kind": "phase", "algorithm": "BFS"})
        self.events.extend(traversal_events(self.model.matrix, "BFS"))
        self.step(auto=True)

    def step(self, auto: bool = False) -> None:
        if not self.events:
            self.events = traversal_events(self.model.matrix, self.algorithm)
            self.running_badge.configure(text=f"RUNNING {self.algorithm}", bg=PURPLE if self.algorithm == "DFS" else "#087e9c", fg="white")
            self.status.configure(text=f"Stepping through {self.algorithm} on the current adjacency matrix...")
        if self.index >= len(self.events): return
        event = self.events[self.index]; self.index += 1; self.apply_event(event)
        if auto and self.index < len(self.events): self.timer = self.after(max(70, 1350-self.speed.get()), lambda: self.step(auto=True))

    def apply_event(self, event: dict) -> None:
        kind, c = event["kind"], event.get("component")
        highlight = None
        if kind == "phase":
            self.algorithm = event["algorithm"]
            self.states = ["unseen"] * self.model.vertices
            self.labels = [None] * self.model.vertices
            self.dfs_btn.configure(style="TButton")
            self.bfs_btn.configure(style="Active.TButton")
            self.running_badge.configure(text="RUNNING BFS", bg="#087e9c", fg="white")
            self.status.configure(text="DFS complete. BFS animation now begins.")
            self.event_text.configure(text="BFS starts from the first unvisited vertex.")
        elif kind == "component": self.event_text.configure(text=f"Component {c+1} starts at vertex {chr(65+event['vertex'])}.")
        elif kind == "frontier": self.states[event["vertex"]] = "frontier"; self.labels[event["vertex"]] = c; self.event_text.configure(text=f"{chr(65+event['vertex'])} enters the {'stack' if self.algorithm == 'DFS' else 'queue'}.")
        elif kind == "visit": self.states[event["vertex"]] = "current"; self.event_text.configure(text=f"Visiting vertex {chr(65+event['vertex'])}.")
        elif kind == "edge": highlight = (event["source"], event["target"]); self.event_text.configure(text=f"Inspect edge {chr(65+event['source'])} — {chr(65+event['target'])}.")
        elif kind == "done": self.states[event["vertex"]] = "done"
        elif kind == "finished":
            self.event_text.configure(text=f"Done! {event['components']} connected component(s) found.")
            self.running_badge.configure(text=f"{self.algorithm} COMPLETE", bg="#087357", fg="white")
        self.refresh(highlight)

    def refresh(self, highlight=None) -> None:
        self.canvas.set_graph(self.model.matrix, self.states, self.labels, highlight)
        self.metrics["Vertices"].configure(text=str(self.model.vertices)); self.metrics["Edges"].configure(text=str(self.model.edge_count))
        visited = sum(state != "unseen" for state in self.states); self.metrics["Visited"].configure(text=str(visited))
        count = len({x for x in self.labels if x is not None}); self.metrics["Components found"].configure(text=str(count) if count else "—")
        vertices = self.model.vertices
        edges = self.model.edge_count
        self.complexity_text.configure(
            text=(f"Current matrix: V={vertices}, E={edges}\n\n"
                  f"DFS: O(V²) time, O(V) space\n"
                  f"BFS: O(V²) time, O(V) space\n\n"
                  f"This input scans {vertices} × {vertices} = "
                  f"{vertices * vertices} matrix cells per algorithm.\n"
                  f"It contains {2 * edges} directed edge entries (2E).")
        )


if __name__ == "__main__":
    ConnectedComponentsLab().mainloop()
