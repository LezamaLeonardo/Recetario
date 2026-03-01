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

# ===== COLORES =====
COLOR_FONDO = "#F5E6D3"
COLOR_DESAYUNO = "#FFD966"
COLOR_COMIDA = "#E74C3C"
COLOR_CENA = "#2E86DE"
COLOR_POSTRE = "#E91E63"
COLOR_TEXTO = "#2C3E50"
COLOR_BOTON = "#27AE60"

# ===== VENTANA PRINCIPAL =====
ventana = tk.Tk()
ventana.title("Recetario Virtual")
ventana.geometry("1000x700")
ventana.resizable(False, False)
ventana.config(bg=COLOR_FONDO)

# ===== PANTALLA 1: INICIO =====
frame_inicio = tk.Frame(ventana, bg=COLOR_FONDO)

titulo_inicio = tk.Label(
    frame_inicio,
    text="📚 RECETARIO VIRTUAL 📚",
    font=("Arial", 40, "bold"),
    bg=COLOR_FONDO,
    fg=COLOR_TEXTO
)
titulo_inicio.pack(pady=30)

subtitulo_inicio = tk.Label(
    frame_inicio,
    text="Bienvenido a tu recetario digital",
    font=("Arial", 16),
    bg=COLOR_FONDO,
    fg=COLOR_TEXTO
)
subtitulo_inicio.pack(pady=10)

frame_categorias = tk.Frame(frame_inicio, bg=COLOR_FONDO)
frame_categorias.pack(pady=30)

# ===== FUNCIONES PARA CAMBIAR DE PANTALLA =====
mostrar_inicio = lambda: (
    frame_recetas.pack_forget(),
    frame_inicio.pack(fill=tk.BOTH, expand=True)
)

mostrar_recetas = lambda cat: (
    frame_inicio.pack_forget(),
    label_categoria.config(text=f"📖 {cat.upper()}"),
    actualizar_tabla_categoria(cat),
    frame_recetas.pack(fill=tk.BOTH, expand=True)
)

# ===== BOTONES DE CATEGORÍAS EN INICIO =====
btn_desayuno = tk.Button(
    frame_categorias,
    text="🌅 DESAYUNO",
    font=("Arial", 14, "bold"),
    bg=COLOR_DESAYUNO,
    fg=COLOR_TEXTO,
    width=20,
    height=3,
    command=lambda: mostrar_recetas("Desayuno")
)
btn_desayuno.pack(pady=10)

btn_comida = tk.Button(
    frame_categorias,
    text="🍽️ COMIDA",
    font=("Arial", 14, "bold"),
    bg=COLOR_COMIDA,
    fg="white",
    width=20,
    height=3,
    command=lambda: mostrar_recetas("Comida")
)
btn_comida.pack(pady=10)

btn_cena = tk.Button(
    frame_categorias,
    text="🌙 CENA",
    font=("Arial", 14, "bold"),
    bg=COLOR_CENA,
    fg="white",
    width=20,
    height=3,
    command=lambda: mostrar_recetas("Cena")
)
btn_cena.pack(pady=10)

btn_postre = tk.Button(
    frame_categorias,
    text="🍰 POSTRE",
    font=("Arial", 14, "bold"),
    bg=COLOR_POSTRE,
    fg="white",
    width=20,
    height=3,
    command=lambda: mostrar_recetas("Postre")
)
btn_postre.pack(pady=10)

# ===== PANTALLA 2: RECETAS =====
frame_recetas = tk.Frame(ventana, bg=COLOR_FONDO)

# Header de la pantalla de recetas
frame_header = tk.Frame(frame_recetas, bg=COLOR_FONDO)
frame_header.pack(fill=tk.X, padx=20, pady=15)

label_categoria = tk.Label(
    frame_header,
    text="",
    font=("Arial", 24, "bold"),
    bg=COLOR_FONDO,
    fg=COLOR_TEXTO
)
label_categoria.pack(side=tk.LEFT)

btn_volver = tk.Button(
    frame_header,
    text="← Volver al Inicio",
    font=("Arial", 10),
    bg=COLOR_TEXTO,
    fg="white",
    command=mostrar_inicio
)
btn_volver.pack(side=tk.RIGHT)

# Frame de búsqueda
frame_busqueda = tk.Frame(frame_recetas, bg=COLOR_FONDO)
frame_busqueda.pack(fill=tk.X, padx=20, pady=10)

tk.Label(frame_busqueda, text="Buscar:", font=("Arial", 11), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side=tk.LEFT, padx=5)
entrada_busqueda = tk.Entry(frame_busqueda, width=40, font=("Arial", 10))
entrada_busqueda.pack(side=tk.LEFT, padx=5)

# Frame central con tabla
frame_central = tk.Frame(frame_recetas, bg=COLOR_FONDO)
frame_central.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

frame_tabla = tk.Frame(frame_central, bg="white")
frame_tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

tabla = ttk.Treeview(
    frame_tabla,
    columns=("nombre", "tiempo"),
    show="headings",
    height=15
)

tabla.heading("nombre", text="Nombre")
tabla.heading("tiempo", text="Tiempo (min)")

tabla.column("nombre", width=400)
tabla.column("tiempo", width=100, anchor="center")

scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tabla.yview)
tabla.configure(yscrollcommand=scrollbar.set)

tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Frame de botones
frame_botones = tk.Frame(frame_central, bg=COLOR_FONDO)
frame_botones.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

# ===== ACTUALIZAR Y BUSCAR POR CATEGORÍA =====
categoria_actual = ""

actualizar_tabla = lambda: (
    tabla.delete(*tabla.get_children()),
    [tabla.insert("", tk.END, values=(r["nombre"], r["tiempo"])) for r in recetas]
)

actualizar_tabla_categoria = lambda cat: (
    entrada_busqueda.delete(0, tk.END),
    tabla.delete(*tabla.get_children()),
    [tabla.insert("", tk.END, values=(r["nombre"], r["tiempo"])) 
     for r in recetas if r["categoria"] == cat]
)

buscar_receta = lambda e=None: (
    tabla.delete(*tabla.get_children()),
    [tabla.insert("", tk.END, values=(r["nombre"], r["tiempo"]))
     for r in recetas
     if r["categoria"] == label_categoria.cget("text").split()[-1]
     and (entrada_busqueda.get().lower() == "" 
          or entrada_busqueda.get().lower() in r["nombre"].lower())]
)

entrada_busqueda.bind("<KeyRelease>", buscar_receta)

# ===== AGREGAR RECETA =====
agregar = lambda: (
    (v := tk.Toplevel(ventana),
     v.title("Agregar Receta"),
     v.geometry("700x580"),
     v.config(bg=COLOR_FONDO)),

    ingredientes := [],
    pasos := [],

    # ===== ROW 1: NOMBRE Y CATEGORÍA =====
    frame_row1 := tk.Frame(v, bg=COLOR_FONDO),
    frame_row1.pack(padx=10, pady=5, fill=tk.X),

    tk.Label(frame_row1, text="Nombre:", font=("Arial", 10), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side=tk.LEFT, padx=5),
    (e_nombre := tk.Entry(frame_row1, width=25, font=("Arial", 10))).pack(side=tk.LEFT, padx=5),

    tk.Label(frame_row1, text="Categoría:", font=("Arial", 10), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side=tk.LEFT, padx=5),
    (c_cat := ttk.Combobox(frame_row1, values=["Desayuno","Comida","Cena","Postre"], state="readonly", width=15, font=("Arial", 10))).pack(side=tk.LEFT, padx=5),

    # ===== ROW 2: TIEMPO Y PORCIONES =====
    frame_row2 := tk.Frame(v, bg=COLOR_FONDO),
    frame_row2.pack(padx=10, pady=5, fill=tk.X),

    tk.Label(frame_row2, text="Tiempo (min):", font=("Arial", 10), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side=tk.LEFT, padx=5),
    (e_tiempo := tk.Entry(frame_row2, width=25, font=("Arial", 10))).pack(side=tk.LEFT, padx=5),

    tk.Label(frame_row2, text="Porciones:", font=("Arial", 10), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side=tk.LEFT, padx=5),
    (e_porciones := tk.Entry(frame_row2, width=15, font=("Arial", 10))).pack(side=tk.LEFT, padx=5),

    # ===== DESCRIPCIÓN =====
    tk.Label(v, text="Descripción:", font=("Arial", 10), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(padx=10, pady=(10,2)),
    (t_desc := tk.Text(v, height=2, width=50, font=("Arial", 10))).pack(padx=10, pady=5),

    # ===== INGREDIENTES =====
    tk.Label(v, text="Ingredientes:", font=("Arial", 10, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(padx=10, pady=(10,2)),
    frame_ing := tk.Frame(v, bg=COLOR_FONDO),
    frame_ing.pack(padx=10, pady=5),

    tk.Label(frame_ing, text="Cantidad", font=("Arial", 8), bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=0, column=0, padx=3),
    tk.Label(frame_ing, text="Unidad", font=("Arial", 8), bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=0, column=1, padx=3),
    tk.Label(frame_ing, text="Ingrediente", font=("Arial", 8), bg=COLOR_FONDO, fg=COLOR_TEXTO).grid(row=0, column=2, padx=3),

    (e_cant := tk.Entry(frame_ing, width=8, font=("Arial", 9))).grid(row=1, column=0, padx=3),
    (e_unidad := tk.Entry(frame_ing, width=10, font=("Arial", 9))).grid(row=1, column=1, padx=3),
    (e_ing := tk.Entry(frame_ing, width=20, font=("Arial", 9))).grid(row=1, column=2, padx=3),

    (lista_ing := tk.Listbox(v, width=50, height=3, font=("Arial", 8))).pack(padx=10, pady=5),

    tk.Button(
        v,
        text="Agregar ingrediente",
        font=("Arial", 9),
        bg=COLOR_BOTON,
        fg="white",
        command=lambda: (
            ingredientes.append(f"{e_cant.get()} {e_unidad.get()} {e_ing.get()}"),
            lista_ing.insert(tk.END, ingredientes[-1]),
            e_cant.delete(0, tk.END),
            e_unidad.delete(0, tk.END),
            e_ing.delete(0, tk.END)
        ) if e_cant.get() and e_unidad.get() and e_ing.get() else messagebox.showerror("Error", "Completa los campos")
    ).pack(pady=3),

    # ===== PASOS =====
    tk.Label(v, text="Pasos:", font=("Arial", 10, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(padx=10, pady=(10,2)),

    (e_paso := tk.Entry(v, width=50, font=("Arial", 10))).pack(padx=10, pady=5),

    (lista_pasos := tk.Listbox(v, width=50, height=3, font=("Arial", 8))).pack(padx=10, pady=5),

    tk.Button(
        v,
        text="Agregar paso",
        font=("Arial", 9),
        bg=COLOR_BOTON,
        fg="white",
        command=lambda: (
            pasos.append(e_paso.get()),
            lista_pasos.insert(tk.END, f"{len(pasos)}. {pasos[-1]}"),
            e_paso.delete(0, tk.END)
        ) if e_paso.get() else messagebox.showerror("Error", "Escribe un paso")
    ).pack(pady=3),

    # ===== GUARDAR =====
    tk.Button(
        v,
        text="💾 Guardar Receta",
        font=("Arial", 10, "bold"),
        bg="#27AE60",
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
                messagebox.showinfo("Éxito", "Receta guardada correctamente"),
                v.destroy()
            )
        )
    ).pack(pady=10)
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
            actualizar_tabla_categoria(label_categoria.cget("text").split()[-1]),
            buscar_receta(),
            messagebox.showinfo("Éxito", "Receta eliminada")
        ))
    )[-1]
)

# ===== BOTONES EN PANTALLA DE RECETAS =====
tk.Button(frame_botones, text="➕ Agregar Receta", bg=COLOR_BOTON, fg="white", font=("Arial", 10, "bold"), command=agregar, width=18).pack(pady=10, fill=tk.X)
tk.Button(frame_botones, text="👁️ Ver Receta", bg="#3498DB", fg="white", font=("Arial", 10, "bold"), command=ver, width=18).pack(pady=10, fill=tk.X)
tk.Button(frame_botones, text="🗑️ Eliminar", bg="#E74C3C", fg="white", font=("Arial", 10, "bold"), command=eliminar, width=18).pack(pady=10, fill=tk.X)

# ===== INICIAR =====
actualizar_tabla()
frame_inicio.pack(fill=tk.BOTH, expand=True)
ventana.mainloop()