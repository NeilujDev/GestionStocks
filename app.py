import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from ui_strings import *
from repo.database import init_schema
from repo.article_repository import create_article, list_articles
from repo.movement_repository import get_stock, create_movement


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("900x560")
        self._build_menu()
        self._build_articles_table()
        self.refresh_articles()

    # Menus
    def _build_menu(self):
        menubar = tk.Menu(self)

        m_articles = tk.Menu(menubar, tearoff=0)
        m_articles.add_command(
            label="Ajouter un article", command=self.add_article_dialog
        )
        menubar.add_cascade(label="Articles", menu=m_articles)

        m_moves = tk.Menu(menubar, tearoff=0)
        m_moves.add_command(
            label="Entrée (IN)", command=lambda: self.add_movement("IN")
        )
        m_moves.add_command(
            label="Sortie (OUT)", command=lambda: self.add_movement("OUT")
        )
        menubar.add_cascade(label="Mouvements", menu=m_moves)

        self.config(menu=menubar)

    # Tableau
    def _build_articles_table(self):
        frame = ttk.Frame(self)
        frame.pack(fill="both", expand=True, padx=12, pady=12)

        columns = ("id", "name", "stock")
        self.tree = ttk.Treeview(
            frame, columns=columns, show="headings", selectmode="browse"
        )
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("stock", text="Stock")
        self.tree.column("id", width=80, anchor="center")
        self.tree.column("name", width=520, anchor="w")
        self.tree.column("stock", width=120, anchor="e")

        vsb = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.status = tk.StringVar(value="Prêt.")
        ttk.Label(self, textvariable=self.status, anchor="w").pack(
            fill="x", padx=12, pady=(0, 8)
        )

    def refresh_articles(self):
        for iid in self.tree.get_children():
            self.tree.delete(iid)

        items = list_articles()
        for a in items:
            stock = get_stock(a.id)
            self.tree.insert("", "end", values=(a.id, a.name, stock))

        self.status.set(f"{len(items)} article(s).")

    # Dialogues
    def add_article_dialog(self):
        name = simpledialog.askstring(APP_TITLE, "Nom de l'article :")
        if not name:
            return
        try:
            create_article(name.strip())
            self.status.set(f"Article créé: {name.strip()}")
            self.refresh_articles()
        except Exception as e:
            messagebox.showerror(MSG_ERROR, str(e))

    def _selected_article_id(self) -> int | None:
        sel = self.tree.selection()
        if not sel:
            return None
        values = self.tree.item(sel[0], "values")
        return int(values[0])

    def add_movement(self, kind: str):
        article_id = self._selected_article_id()
        if not article_id:
            messagebox.showinfo(
                MSG_INFO, "Sélectionne d'abord un article dans la liste."
            )
            return
        qty = simpledialog.askinteger(APP_TITLE, f"Quantité pour {kind} :", minvalue=1)
        if not qty:
            return
        try:
            create_movement(article_id, kind, qty)
            self.status.set(f"Mouvement {kind} de {qty} enregistré.")
            self.refresh_articles()
        except Exception as e:
            messagebox.showerror(MSG_ERROR, str(e))


if __name__ == "__main__":
    init_schema()
    App().mainloop()
