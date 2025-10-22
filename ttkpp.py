import json
import os
from tkinter import ttk

class ttkpp:
    def __init__(self, theme_name="default", root=None):
        self.theme_name = theme_name
        self.themes = self.load_themes()
        self.theme = self.themes.get(self.theme_name, self.themes["default"])

        self.root = root
        self.apply_theme()

    def load_themes(self):
        path = os.path.join(os.path.dirname(__file__), "themes", "theme.json")
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def apply_theme(self):
        if self.root:
            self.root.configure(bg=self.theme["bg"])
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "TButton",
            background=self.theme["button_bg"],
            foreground=self.theme["button_fg"],
            font=("Arial", 12),
            padding=8,
            borderwidth=0
        )

        style.map(
            "TButton",
            background=[("active", self.theme["accent"])]
        )
