"""Dialog for importing any user-provided adjacency matrix."""

import tkinter as tk
from tkinter import ttk


class MatrixDialog(tk.Toplevel):
    def __init__(self, parent: tk.Misc, apply_callback) -> None:
        super().__init__(parent)
        self.title("Import adjacency matrix")
        self.configure(bg="#112440")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()
        tk.Label(self, text="Paste any square, symmetric 0/1 adjacency matrix.", bg="#112440", fg="#eef5ff", font=("Segoe UI", 11)).pack(padx=18, pady=(16, 6))
        tk.Label(self, text="One row per line. Maximum 12 vertices.", bg="#112440", fg="#a7b8d5").pack(padx=18, anchor="w")
        self.text = tk.Text(self, width=45, height=12, bg="#09182c", fg="#eef5ff", insertbackground="white", font=("Consolas", 10))
        self.text.pack(padx=18, pady=10)
        ttk.Button(self, text="Use this matrix", command=lambda: apply_callback(self, self.text.get("1.0", "end"))).pack(pady=(0, 16))
