import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
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

# ===== PANTALLA 2: RECETAS =====
frame_recetas = tk.Frame(ventana, bg=COLOR_FONDO)

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

frame_busqueda = tk.Frame(frame_recetas, bg=COLOR_FONDO)
frame_busqueda.pack(fill=tk.X, padx=20, pady=10)

tk.Label(frame_busqueda, text="Buscar:", font=("Arial", 11), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side=tk.LEFT, padx=5)
entrada_busqueda = tk.Entry(frame_busqueda, width=40, font=("Arial", 10))
entrada_busqueda.pack(side=tk.LEFT, padx=5)

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

frame_botones = tk.Frame(frame_central, bg=COLOR_FONDO)
frame_botones.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

# ===== PANTALLA 3: DETALLE DE RECETA =====
frame_detalle = tk.Frame(ventana, bg=COLOR_FONDO)

canvas_detalle = tk.Canvas(frame_detalle, bg=COLOR_FONDO, highlightthickness=0)
scrollbar_detalle = ttk.Scrollbar(frame_detalle, orient=tk.VERTICAL, command=canvas_detalle.yview)
frame_contenido_detalle = tk.Frame(canvas_detalle, bg=COLOR_FONDO)

frame_contenido_detalle.bind(
    "<Configure>",
    lambda e: canvas_detalle.configure(scrollregion=canvas_detalle.bbox("all"))
)

canvas_detalle.create_window((0, 0), window=frame_contenido_detalle, anchor="nw")
canvas_detalle.configure(yscrollcommand=scrollbar_detalle.set)

# ===== PANTALLA 4: LISTA DE COMPRAS =====
frame_lista_compras = tk.Frame(ventana, bg=COLOR_FONDO)

frame_header_compras = tk.Frame(frame_lista_compras, bg=COLOR_FONDO)
frame_header_compras.pack(fill=tk.X, padx=20, pady=15)

tk.Label(frame_header_compras, text="🛒 LISTA DE COMPRAS", font=("Arial", 24, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side=tk.LEFT)

frame_contenido_compras = tk.Frame(frame_lista_compras, bg=COLOR_FONDO)
frame_contenido_compras.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

lista_compras_text = tk.Text(frame_contenido_compras, font=("Arial", 10), bg="white", fg=COLOR_TEXTO)
lista_compras_text.pack(fill=tk.BOTH, expand=True)

frame_botones_compras = tk.Frame(frame_lista_compras, bg=COLOR_FONDO)
frame_botones_compras.pack(fill=tk.X, padx=20, pady=10)

# ===== VARIABLES GLOBALES =====
receta_actual = [None]
imagenes_referencias = []
recetas_seleccionadas = []
datos_spinbox = {"spinbox": None, "lista": None, "receta": None}

# ===== FUNCIONES PARA CAMBIAR DE PANTALLA =====
mostrar_inicio = lambda: (
    frame_recetas.pack_forget(),
    frame_detalle.pack_forget(),
    frame_lista_compras.pack_forget(),
    frame_inicio.pack(fill=tk.BOTH, expand=True)
)

limpiar_header = lambda: (
    [widget.destroy() for widget in frame_header.winfo_children()]
)

mostrar_recetas = lambda cat: (
    frame_inicio.pack_forget(),
    frame_detalle.pack_forget(),
    frame_lista_compras.pack_forget(),
    limpiar_header(),
    tk.Label(frame_header, text=f"📖 {cat.upper()}", font=("Arial", 24, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side=tk.LEFT),
    tk.Button(frame_header, text="← Volver al Inicio", font=("Arial", 10), bg=COLOR_TEXTO, fg="white", command=mostrar_inicio).pack(side=tk.RIGHT),
    actualizar_tabla_categoria(cat),
    frame_recetas.pack(fill=tk.BOTH, expand=True)
)

# ===== ACTUALIZAR Y BUSCAR POR CATEGORÍA =====
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
     if r["categoria"] == [w for w in frame_header.winfo_children() if isinstance(w, tk.Label)][0].cget("text").split()[-1]
     and (entrada_busqueda.get().lower() == "" 
          or entrada_busqueda.get().lower() in r["nombre"].lower())]
)

entrada_busqueda.bind("<KeyRelease>", buscar_receta)

# ===== CARGAR DETALLE DE RECETA =====
cargar_detalle_receta = lambda: (
    (
        nombre_seleccionado := tabla.item(tabla.selection()[0])["values"][0],
        r := next((x for x in recetas if x["nombre"] == nombre_seleccionado), None),
        r and (
            receta_actual.__setitem__(0, r),
            [widget.destroy() for widget in frame_contenido_detalle.winfo_children()],
            imagenes_referencias.clear(),
            mostrar_detalle_completo(r),
            frame_recetas.pack_forget(),
            canvas_detalle.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10),
            scrollbar_detalle.pack(side=tk.RIGHT, fill=tk.Y),
            frame_detalle.pack(fill=tk.BOTH, expand=True)
        )
    )
)

actualizar_ingredientes_spinbox = lambda: (
    datos_spinbox["lista"] and datos_spinbox["spinbox"] and datos_spinbox["receta"] and (
        r := datos_spinbox["receta"],
        sp := datos_spinbox["spinbox"],
        lista := datos_spinbox["lista"],
        lista.delete(0, tk.END),
        [lista.insert(tk.END, ajustar_ingrediente(ing, float(r.get('porciones', 1) or 1), float(sp.get() or 1))) 
         for ing in r.get("ingredientes", [])],
        None
    )
)

ajustar_ingrediente = lambda ing, porciones_base, porciones_nueva: (
    (partes := ing.split()),
    (float_cant := float(partes[0].replace(',', '.')) if partes and partes[0].replace('.', '').replace(',', '').isdigit() else 1),
    (nueva_cant := float_cant * (porciones_nueva / porciones_base)),
    f"{nueva_cant:.2f} {' '.join(partes[1:])}"
)[-1] if len(ing.split()) > 0 and ing.split()[0].replace('.', '').replace(',', '').isdigit() else ing

mostrar_detalle_completo = lambda r: (
    # Header con botón volver
    frame_header_det := tk.Frame(frame_contenido_detalle, bg=COLOR_FONDO),
    frame_header_det.pack(fill=tk.X, pady=10),
    tk.Button(frame_header_det, text="← Volver", font=("Arial", 10), bg=COLOR_TEXTO, fg="white", 
              command=lambda: (frame_detalle.pack_forget(), frame_recetas.pack(fill=tk.BOTH, expand=True))).pack(side=tk.LEFT),

    # Nombre
    tk.Label(frame_contenido_detalle, text=r["nombre"], font=("Arial", 18, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=5),

    # Info básica
    tk.Label(frame_contenido_detalle, text=f"Categoría: {r['categoria']} | Tiempo: {r['tiempo']} min | Porciones base: {r.get('porciones', '1')}", 
             font=("Arial", 10), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(pady=5),

    # Mostrar imagen si existe
    (r.get("imagen_url") and os.path.exists(r.get("imagen_url", "")) and (
        img := Image.open(r.get("imagen_url")),
        img.thumbnail((300, 250)),
        photo := ImageTk.PhotoImage(img),
        imagenes_referencias.append(photo),
        label_img := tk.Label(frame_contenido_detalle, image=photo, bg=COLOR_FONDO),
        label_img.pack(pady=10),
        None
    )),

    # Selector de porciones
    frame_porciones := tk.Frame(frame_contenido_detalle, bg=COLOR_FONDO),
    frame_porciones.pack(pady=10),

    tk.Label(frame_porciones, text="Porciones:", font=("Arial", 11, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(side=tk.LEFT, padx=5),
    (spinbox_porciones := tk.Spinbox(frame_porciones, from_=1, to=100, font=("Arial", 10), width=5, command=actualizar_ingredientes_spinbox)),
    spinbox_porciones.pack(side=tk.LEFT, padx=5),
    spinbox_porciones.delete(0, tk.END),
    spinbox_porciones.insert(0, r.get('porciones', '1')),
    datos_spinbox.update({"spinbox": spinbox_porciones, "receta": r}),

    # Descripción
    tk.Label(frame_contenido_detalle, text="Descripción:", font=("Arial", 11, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(anchor=tk.W, padx=10, pady=(10, 2)),
    tk.Label(frame_contenido_detalle, text=r.get('descripcion', ''), font=("Arial", 10), bg=COLOR_FONDO, fg=COLOR_TEXTO, wraplength=600, justify=tk.LEFT).pack(anchor=tk.W, padx=10, pady=5),

    # Ingredientes
    tk.Label(frame_contenido_detalle, text="Ingredientes:", font=("Arial", 11, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(anchor=tk.W, padx=10, pady=(10, 2)),
    
    (lista_ing_detalle := tk.Listbox(frame_contenido_detalle, width=70, height=6, font=("Arial", 9))),
    lista_ing_detalle.pack(padx=10, pady=5),
    datos_spinbox.update({"lista": lista_ing_detalle}),

    [lista_ing_detalle.insert(tk.END, ing) for ing in r.get("ingredientes", [])],

    # Pasos
    tk.Label(frame_contenido_detalle, text="Pasos:", font=("Arial", 11, "bold"), bg=COLOR_FONDO, fg=COLOR_TEXTO).pack(anchor=tk.W, padx=10, pady=(10, 2)),
    (lista_pasos_detalle := tk.Listbox(frame_contenido_detalle, width=70, height=6, font=("Arial", 9))),
    lista_pasos_detalle.pack(padx=10, pady=5),
    [lista_pasos_detalle.insert(tk.END, f"{i+1}. {p}") for i, p in enumerate(r.get("pasos", []))],

    # Botones de acción
    frame_acciones := tk.Frame(frame_contenido_detalle, bg=COLOR_FONDO),
    frame_acciones.pack(pady=20),
    
    tk.Button(frame_acciones, text="💾 Guardar como TXT", font=("Arial", 10, "bold"), bg=COLOR_BOTON, fg="white",
              command=lambda: guardar_receta_txt(r, int(spinbox_porciones.get()))).pack(side=tk.LEFT, padx=5),
    
    tk.Button(frame_acciones, text="🛒 Agregar a Lista de Compras", font=("Arial", 10, "bold"), bg="#FF9800", fg="white",
              command=lambda: (recetas_seleccionadas.append((r, int(spinbox_porciones.get()))), messagebox.showinfo("Éxito", f"{r['nombre']} agregado a lista de compras"))).pack(side=tk.LEFT, padx=5),
)

guardar_receta_txt = lambda r, porciones: (
    archivo := filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo de texto", "*.txt")]),
    archivo and (
        ingredientes_ajustados := [ajustar_ingrediente(ing, float(r.get('porciones', 1) or 1), float(porciones)) for ing in r.get('ingredientes', [])],
        contenido := f"""
================== RECETA: {r['nombre']} ==================

CATEGORÍA: {r['categoria']}
TIEMPO: {r['tiempo']} minutos
PORCIONES: {porciones}

DESCRIPCIÓN:
{r.get('descripcion', '')}

INGREDIENTES:
{chr(10).join(f"- {ing}" for ing in ingredientes_ajustados)}

PASOS:
{chr(10).join(f"{i+1}. {p}" for i, p in enumerate(r.get('pasos', [])))}

IMAGEN: {r.get('imagen_url', 'No especificada')}

================== FIN DE LA RECETA ==================
        """,
        open(archivo, 'w', encoding='utf-8').write(contenido),
        messagebox.showinfo("Éxito", f"Receta guardada en:\n{archivo}"),
        None
    )
)

generar_lista_compras = lambda: (
    lista_compras_text.delete("1.0", tk.END),
    (
        ingredientes_dict := {},
        [
            (
                [ingredientes_dict.update({ing_ajustado: ingredientes_dict.get(ing_ajustado, "") + " " + ing_ajustado})
                for ing in r.get('ingredientes', [])
                if (ing_ajustado := ajustar_ingrediente(ing, float(r.get('porciones', 1) or 1), float(porciones)))
                ],
                None
            )
            for r, porciones in recetas_seleccionadas
        ],
        lista_compras_text.insert("1.0", f"{'='*50}\n🛒 LISTA DE COMPRAS COMBINADA 🛒\n{'='*50}\n\n"),
        [lista_compras_text.insert(tk.END, f"☐ {ing}\n") for ing in ingredientes_dict.keys()],
        lista_compras_text.insert(tk.END, f"\n{'='*50}\nRecetas incluidas:\n"),
        [lista_compras_text.insert(tk.END, f"- {r['nombre']} ({porciones} porciones)\n") for r, porciones in recetas_seleccionadas],
    )[-1]
)

exportar_lista_compras = lambda: (
    archivo := filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivo de texto", "*.txt")]),
    archivo and (
        contenido := lista_compras_text.get("1.0", tk.END),
        open(archivo, 'w', encoding='utf-8').write(contenido),
        messagebox.showinfo("Éxito", f"Lista de compras guardada en:\n{archivo}"),
        None
    )
)

mostrar_lista_compras = lambda: (
    len(recetas_seleccionadas) == 0 and messagebox.showerror("Error", "Agrega recetas a la lista primero")
) or (
    frame_recetas.pack_forget(),
    frame_detalle.pack_forget(),
    frame_inicio.pack_forget(),
    generar_lista_compras(),
    frame_lista_compras.pack(fill=tk.BOTH, expand=True)
)

# ===== AGREGAR RECETA =====
agregar = lambda: (
    (v := tk.Toplevel(ventana),
     v.title("Agregar Receta"),
     v.geometry("700x700"),
     v.config(bg=COLOR_FONDO)),

    ingredientes := [],
    pasos := [],
    imagen_path := [""],

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

    # ===== IMAGEN =====
    frame_img := tk.Frame(v, bg=COLOR_FONDO),
    frame_img.pack(padx=10, pady=5, fill=tk.X),

    tk.Button(frame_img, text="📷 Seleccionar Imagen", font=("Arial", 9), bg=COLOR_BOTON, fg="white",
              command=lambda: (imagen_path.__setitem__(0, filedialog.askopenfilename(filetypes=[("Imágenes", "*.jpg *.png *.jpeg")])), 
                               label_img_nombre.config(text=os.path.basename(imagen_path[0]) if imagen_path[0] else "Sin imagen"))).pack(side=tk.LEFT, padx=5),

    (label_img_nombre := tk.Label(frame_img, text="Sin imagen", font=("Arial", 9), bg=COLOR_FONDO, fg=COLOR_TEXTO)).pack(side=tk.LEFT, padx=5),

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

    (lista_ing := tk.Listbox(v, width=50, height=2, font=("Arial", 8))).pack(padx=10, pady=5),

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

    (lista_pasos := tk.Listbox(v, width=50, height=2, font=("Arial", 8))).pack(padx=10, pady=5),

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
                    "porciones": e_porciones.get() or "1",
                    "descripcion": t_desc.get("1.0", tk.END).strip(),
                    "ingredientes": ingredientes,
                    "pasos": pasos,
                    "imagen_url": imagen_path[0]
                }),
                open(ruta_json, "w", encoding="utf-8").write(json.dumps(recetas, indent=4, ensure_ascii=False)),
                messagebox.showinfo("Éxito", "Receta guardada correctamente"),
                actualizar_tabla_categoria([w for w in frame_header.winfo_children() if isinstance(w, tk.Label)][0].cget("text").split()[-1]),
                v.destroy()
            )
        )
    ).pack(pady=10)
)

# ===== VER =====
ver = lambda: (
    tabla.selection() and cargar_detalle_receta() or messagebox.showerror("Error", "Selecciona una receta")
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
            actualizar_tabla_categoria([w for w in frame_header.winfo_children() if isinstance(w, tk.Label)][0].cget("text").split()[-1]),
            buscar_receta(),
            messagebox.showinfo("Éxito", "Receta eliminada")
        ))
    )[-1]
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

# ===== BOTONES EN PANTALLA DE RECETAS =====
tk.Button(frame_botones, text="➕ Agregar Receta", bg=COLOR_BOTON, fg="white", font=("Arial", 10, "bold"), command=agregar, width=18).pack(pady=10, fill=tk.X)
tk.Button(frame_botones, text="👁️ Ver Receta", bg="#3498DB", fg="white", font=("Arial", 10, "bold"), command=ver, width=18).pack(pady=10, fill=tk.X)
tk.Button(frame_botones, text="🗑️ Eliminar", bg="#E74C3C", fg="white", font=("Arial", 10, "bold"), command=eliminar, width=18).pack(pady=10, fill=tk.X)
tk.Button(frame_botones, text="🛒 Ver Lista de Compras", bg="#FF9800", fg="white", font=("Arial", 10, "bold"), command=mostrar_lista_compras, width=18).pack(pady=10, fill=tk.X)

# ===== BOTONES EN PANTALLA DE LISTA DE COMPRAS =====
tk.Button(frame_botones_compras, text="💾 Exportar Lista", bg=COLOR_BOTON, fg="white", font=("Arial", 10, "bold"), command=exportar_lista_compras).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones_compras, text="🔄 Regenerar", bg="#3498DB", fg="white", font=("Arial", 10, "bold"), command=generar_lista_compras).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones_compras, text="← Volver", bg=COLOR_TEXTO, fg="white", font=("Arial", 10, "bold"), command=mostrar_inicio).pack(side=tk.LEFT, padx=5)
tk.Button(frame_botones_compras, text="🗑️ Limpiar", bg="#E74C3C", fg="white", font=("Arial", 10, "bold"), command=lambda: (recetas_seleccionadas.clear(), lista_compras_text.delete("1.0", tk.END))).pack(side=tk.LEFT, padx=5)

# ===== INICIAR =====
actualizar_tabla()
frame_inicio.pack(fill=tk.BOTH, expand=True)
ventana.mainloop()