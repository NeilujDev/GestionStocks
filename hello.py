# Test basique de l'environnement
print("Env OK")

# Test visuel Tkinter
import tkinter as tk

root = tk.Tk()
root.title("Test Tkinter")
tk.Label(root, text="Tkinter fonctionne.").pack(padx=12, pady=12)
root.after(1200, root.destroy)  # ferme la fenêtre après ~1,2s
root.mainloop()
