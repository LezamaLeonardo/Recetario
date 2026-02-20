import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ===== ARCHIVO JSON =====
ruta_json = "recetas.json"
recetas = []

if os.path.exists(ruta_json):
    try:
        with open(ruta_json, "r", encoding="utf-8") as archivo:
            recetas = json.load(archivo)
    except:
        pass

# ===== VENTANA PRINCIPAL =====
ventana = tk.Tk()
ventana.title("Recetario de Cocina")
ventana.geometry("900x550")
ventana.resizable(False, False)

# ===== FRAME SUPERIOR =====
frame_superior = tk.Frame(ventana)
frame_superior.pack(fill=tk.X, padx=20, pady=15)

tk.Label(frame_superior, text="Buscar:").grid(row=0, column=0, padx=5)
entrada_busqueda = tk.Entry(frame_superior, width=30)
entrada_busqueda.grid(row=0, column=1, padx=5)

tk.Label(frame_superior, text="Categoría:").grid(row=0, column=2, padx=20)
combo_categoria = ttk.Combobox(
    frame_superior,
    values=["Todas", "Desayuno", "Comida", "Cena", "Postre"],
    state="readonly",
    width=20
)
combo_categoria.set("Todas")
combo_categoria.grid(row=0, column=3, padx=5)

# ===== FRAME CENTRAL =====
frame_central = tk.Frame(ventana)
frame_central.pack(fill=tk.BOTH, expand=True, padx=20)

# ===== TABLA =====
frame_tabla = tk.Frame(frame_central)
frame_tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

tabla = ttk.Treeview(
    frame_tabla,
    columns=("nombre", "categoria", "tiempo"),
    show="headings",
    height=18
)

tabla.heading("nombre", text="Nombre")
tabla.heading("categoria", text="Categoría")
tabla.heading("tiempo", text="Tiempo (min)")

tabla.column("nombre", width=300)
tabla.column("categoria", width=150)
tabla.column("tiempo", width=120, anchor="center")

scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tabla.yview)
tabla.configure(yscrollcommand=scrollbar.set)

tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# ===== FUNCIONES LAMBDA =====
actualizar_tabla = lambda: (
    tabla.delete(*tabla.get_children()),
    [tabla.insert("", tk.END, values=(r["nombre"], r["categoria"], r["tiempo"])) for r in recetas]
)

buscar = lambda e=None: (
    tabla.delete(*tabla.get_children()),
    [tabla.insert("", tk.END, values=(r["nombre"], r["categoria"], r["tiempo"]))
     for r in recetas
     if (entrada_busqueda.get().lower() == "" 
         or entrada_busqueda.get().lower() in r["nombre"].lower() 
         or entrada_busqueda.get().lower() in r.get("ingredientes", "").lower())
     and (combo_categoria.get() == "Todas" 
          or r["categoria"] == combo_categoria.get())]
)

entrada_busqueda.bind("<KeyRelease>", buscar)
combo_categoria.bind("<<ComboboxSelected>>", buscar)

# ===== AGREGAR RECETA =====
agregar = lambda: (
    (v_agregar := tk.Toplevel(ventana),
     v_agregar.title("Agregar Receta"),
     v_agregar.geometry("400x450")),

    tk.Label(v_agregar, text="Nombre:").pack(pady=5),
    (e_nombre := tk.Entry(v_agregar, width=40), e_nombre.pack(pady=5)),

    tk.Label(v_agregar, text="Categoría:").pack(pady=5),
    (c_cat := ttk.Combobox(
        v_agregar,
        values=["Desayuno", "Comida", "Cena", "Postre"],
        state="readonly",
        width=38
    ), c_cat.pack(pady=5)),

    tk.Label(v_agregar, text="Tiempo (min):").pack(pady=5),
    (e_tiempo := tk.Entry(v_agregar, width=40), e_tiempo.pack(pady=5)),

    tk.Label(v_agregar, text="Ingredientes:").pack(pady=5),
    (t_ing := tk.Text(v_agregar, height=5, width=40), t_ing.pack(pady=5)),

    tk.Button(
        v_agregar,
        text="Guardar",
        bg="green",
        fg="white",
        width=20,
        command=lambda: (
            messagebox.showerror("Error", "Completa todos los campos")
            if (e_nombre.get() == "" or c_cat.get() == "" or e_tiempo.get() == "" or t_ing.get("1.0", tk.END).strip() == "")
            else (
                recetas.append({
                    "nombre": e_nombre.get(),
                    "categoria": c_cat.get(),
                    "tiempo": e_tiempo.get(),
                    "ingredientes": t_ing.get("1.0", tk.END).strip()
                }),
                open(ruta_json, "w", encoding="utf-8").write(json.dumps(recetas, indent=4, ensure_ascii=False)),
                actualizar_tabla(),
                buscar(),
                messagebox.showinfo("Éxito", "Receta guardada"),
                v_agregar.destroy()
            )
        )
    ).pack(pady=10),

    tk.Button(v_agregar, text="Cancelar", command=v_agregar.destroy, width=20).pack(pady=5)
)

# ===== VER RECETA =====
ver = lambda: (
    messagebox.showerror("Error", "Selecciona una receta")
    if not tabla.selection()
    else (
        nombre_sel := tabla.item(tabla.selection()[0])["values"][0],
        messagebox.showinfo(
            "Detalles",
            "\n".join([
                f"Nombre: {r['nombre']}\n"
                f"Categoría: {r['categoria']}\n"
                f"Tiempo: {r['tiempo']} min\n\n"
                f"Ingredientes:\n{r['ingredientes']}"
                for r in recetas if r["nombre"] == nombre_sel
            ])
        )
    )[-1]
)

# ===== ELIMINAR RECETA =====
eliminar = lambda: (
    messagebox.showerror("Error", "Selecciona una receta")
    if not tabla.selection()
    else (
        nombre_sel := tabla.item(tabla.selection()[0])["values"][0],
        messagebox.askyesno("Confirmar", f"¿Eliminar '{nombre_sel}'?")
        and (
            recetas.pop(next(i for i, r in enumerate(recetas) if r["nombre"] == nombre_sel)),
            open(ruta_json, "w", encoding="utf-8").write(json.dumps(recetas, indent=4, ensure_ascii=False)),
            actualizar_tabla(),
            buscar(),
            messagebox.showinfo("Éxito", "Receta eliminada")
        )
    )[-1]
)

# ===== BOTONES =====
frame_botones = tk.Frame(frame_central)
frame_botones.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

tk.Button(frame_botones, text="Agregar Receta", bg="green", fg="white", command=agregar).pack(pady=10, fill=tk.X)
tk.Button(frame_botones, text="Ver Receta", command=ver).pack(pady=10, fill=tk.X)
tk.Button(frame_botones, text="Eliminar", bg="red", fg="white", command=eliminar).pack(pady=10, fill=tk.X)

# ===== INICIAR =====
actualizar_tabla()
ventana.mainloop()
