# ui_widgets.py - Кастомные виджеты для интерфейса

import tkinter as tk
from tkinter import ttk

class RoundedFrame(tk.Frame):
    def __init__(self, parent, bg="#1a1a1a", radius=16, **kwargs):
        super().__init__(parent, bg=parent["bg"], **kwargs)
        self.radius = radius
        self.bg_color = bg
        self.canvas = tk.Canvas(self, bg=parent["bg"], highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.inner_frame = tk.Frame(self.canvas, bg=bg)
        self.inner_frame.pack(fill="both", expand=True, padx=1, pady=1)
        self.canvas.bind("<Configure>", self._on_configure)

    def _on_configure(self, event):
        self.canvas.delete("all")
        w, h = event.width, event.height
        r = self.radius
        points = [
            r, 0, w - r,