import tkinter as tk
from tkinter import ttk
from ui_strings import *
from repo.database import init_schema


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("800x500")
        self._build_ui()

    def _build_ui(self):
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=12, pady=12)
        ttk.Label(frame, text="Interface initiale prête.").pack()


if __name__ == "__main__":
    init_schema()  # crée stock.db + tables si besoin
    App().mainloop()
