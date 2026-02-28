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

# ===== ACTUALIZAR Y BUSCAR =====
actualizar_tabla = lambda: (
    tabla.delete(*tabla.get_children()),
    [tabla.insert("", tk.END, values=(r["nombre"], r["categoria"], r["tiempo"])) for r in recetas]
)

buscar = lambda e=None: (
    tabla.delete(*tabla.get_children()),
    [tabla.insert("", tk.END, values=(r["nombre"], r["categoria"], r["tiempo"]))
     for r in recetas
     if (entrada_busqueda.get().lower() == "" 
         or entrada_busqueda.get().lower() in r["nombre"].lower())
     and (combo_categoria.get() == "Todas" 
          or r["categoria"] == combo_categoria.get())]
)

entrada_busqueda.bind("<KeyRelease>", buscar)
combo_categoria.bind("<<ComboboxSelected>>", buscar)

# ===== AGREGAR RECETA =====
agregar = lambda: (
    (v := tk.Toplevel(ventana),
     v.title("Agregar Receta"),
     v.geometry("600x750")),

    ingredientes := [],
    pasos := [],

    tk.Label(v, text="Nombre:").pack(padx=10, pady=5),
    (e_nombre := tk.Entry(v, width=50)).pack(padx=10, pady=5),

    tk.Label(v, text="Categoría:").pack(padx=10, pady=5),
    (c_cat := ttk.Combobox(v, values=["Desayuno","Comida","Cena","Postre"], state="readonly", width=47)).pack(padx=10, pady=5),

    tk.Label(v, text="Tiempo (min):").pack(padx=10, pady=5),
    (e_tiempo := tk.Entry(v, width=50)).pack(padx=10, pady=5),

    tk.Label(v, text="Porciones:").pack(padx=10, pady=5),
    (e_porciones := tk.Entry(v, width=50)).pack(padx=10, pady=5),

    tk.Label(v, text="Descripción:").pack(padx=10, pady=5),
    (t_desc := tk.Text(v, height=3, width=50)).pack(padx=10, pady=5),

    # ----- INGREDIENTES -----
    tk.Label(v, text="Ingredientes:", font=("Arial", 10, "bold")).pack(padx=10, pady=(15,5)),
    frame_ing := tk.Frame(v),
    frame_ing.pack(padx=10, pady=5),

    tk.Label(frame_ing, text="Cantidad").grid(row=0, column=0, padx=5),
    tk.Label(frame_ing, text="Unidad").grid(row=0, column=1, padx=5),
    tk.Label(frame_ing, text="Ingrediente").grid(row=0, column=2, padx=5),

    (e_cant := tk.Entry(frame_ing, width=8)).grid(row=1, column=0, padx=5),
    (e_unidad := tk.Entry(frame_ing, width=10)).grid(row=1, column=1, padx=5),
    (e_ing := tk.Entry(frame_ing, width=25)).grid(row=1, column=2, padx=5),

    (lista_ing := tk.Listbox(v, width=50, height=5)).pack(padx=10, pady=5),

    tk.Button(
        v,
        text="Agregar ingrediente",
        command=lambda: (
            ingredientes.append(f"{e_cant.get()} {e_unidad.get()} {e_ing.get()}"),
            lista_ing.insert(tk.END, ingredientes[-1]),
            e_cant.delete(0, tk.END),
            e_unidad.delete(0, tk.END),
            e_ing.delete(0, tk.END)
        ) if e_cant.get() and e_unidad.get() and e_ing.get() else messagebox.showerror("Error", "Completa los campos")
    ).pack(pady=5),

    # ----- PASOS -----
    tk.Label(v, text="Pasos:", font=("Arial", 10, "bold")).pack(padx=10, pady=(15,5)),

    (e_paso := tk.Entry(v, width=50)).pack(padx=10, pady=5),

    (lista_pasos := tk.Listbox(v, width=50, height=5)).pack(padx=10, pady=5),

    tk.Button(
        v,
        text="Agregar paso",
        command=lambda: (
            pasos.append(e_paso.get()),
            lista_pasos.insert(tk.END, f"{len(pasos)}. {pasos[-1]}"),
            e_paso.delete(0, tk.END)
        ) if e_paso.get() else messagebox.showerror("Error", "Escribe un paso")
    ).pack(pady=5),

    # ----- GUARDAR -----
    tk.Button(
        v,
        text="Guardar",
        bg="green",
        fg="white",
        command=lambda: (
            messagebox.showerror("Error", "Completa los campos obligatorios")
            if e_nombre.get()=="" or c_cat.get()=="" or e_tiempo.get()=="" or not ingredientes or not pasos
            else (
                recetas.append({
                    "nombre": e_nombre.get(),
                    "categoria": c_cat.get(),
                    "tiempo": e_tiempo.get(),
                    "porciones": e_porciones.get(),
                    "descripcion": t_desc.get("1.0", tk.END).strip(),
                    "ingredientes": ingredientes,
                    "pasos": pasos
                }),
                open(ruta_json, "w", encoding="utf-8").write(json.dumps(recetas, indent=4, ensure_ascii=False)),
                actualizar_tabla(),
                buscar(),
                messagebox.showinfo("Éxito", "Receta guardada correctamente"),
                v.destroy()
            )
        )
    ).pack(pady=20)
)

# ===== VER =====
ver = lambda: (
    messagebox.showerror("Error", "Selecciona una receta")
    if not tabla.selection()
    else (
        nombre := tabla.item(tabla.selection()[0])["values"][0],
        r := next(x for x in recetas if x["nombre"] == nombre),
        messagebox.showinfo(
            "Detalles",
            f"Nombre: {r['nombre']}\n"
            f"Categoría: {r['categoria']}\n"
            f"Tiempo: {r['tiempo']} min\n"
            f"Porciones: {r.get('porciones','')}\n\n"
            f"Descripción:\n{r.get('descripcion','')}\n\n"
            f"Ingredientes:\n" + "\n".join(r.get("ingredientes",[])) +
            "\n\nPasos:\n" + "\n".join(f"{i+1}. {p}" for i,p in enumerate(r.get("pasos",[])))
        )
    )[-1]
)

# ===== ELIMINAR =====
eliminar = lambda: (
    messagebox.showerror("Error", "Selecciona una receta")
    if not tabla.selection()
    else (
        nombre := tabla.item(tabla.selection()[0])["values"][0],
        (messagebox.askyesno("Confirmar", f"¿Eliminar '{nombre}'?") and (
            recetas.pop(next(i for i,r in enumerate(recetas) if r["nombre"]==nombre)),
            open(ruta_json,"w",encoding="utf-8").write(json.dumps(recetas,indent=4,ensure_ascii=False)),
            actualizar_tabla(),
            buscar(),
            messagebox.showinfo("Éxito", "Receta eliminada")
        ))
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