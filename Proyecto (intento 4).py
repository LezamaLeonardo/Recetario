import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ===== ARCHIVO JSON =====
ruta_json = "recetas.json" # Puedes cambiar el nombre o la ruta del archivo JSON si lo deseas
recetas = [] # Lista para almacenar las recetas cargadas desde el JSON

if os.path.exists(ruta_json): # Verificar si el archivo JSON existe antes de intentar cargarlo
    try:
        with open(ruta_json, "r", encoding="utf-8") as archivo: # Abrir el archivo JSON en modo lectura
            recetas = json.load(archivo) # Cargar las recetas desde el archivo JSON y almacenarlas en la lista 'recetas'
    except:
        pass

# ===== VENTANA PRINCIPAL =====
ventana = tk.Tk()
ventana.title("Recetario de Cocina") # Establecer el título de la ventana principal
ventana.geometry("900x550") # Establecer el tamaño de la ventana principal (ancho x alto)
ventana.resizable(False, False) # Evitar que la ventana principal sea redimensionable (tanto en ancho como en alto)

# ===== FRAME SUPERIOR =====
frame_superior = tk.Frame(ventana) # Crear un frame para contener los elementos de búsqueda y filtro en la parte superior de la ventana
frame_superior.pack(fill=tk.X, padx=20, pady=15) # Empaquetar el frame superior para que ocupe todo el ancho de la ventana, con un margen horizontal de 20 píxeles y un margen vertical de 15 píxeles

tk.Label(frame_superior, text="Buscar:").grid(row=0, column=0, padx=5) # Crear una etiqueta con el texto "Buscar:" y colocarla en la fila 0, columna 0 del grid del frame superior, con un margen horizontal de 5 píxeles
entrada_busqueda = tk.Entry(frame_superior, width=30) # Crear un campo de entrada de texto para la búsqueda, con un ancho de 30 caracteres
entrada_busqueda.grid(row=0, column=1, padx=5) 

tk.Label(frame_superior, text="Categoría:").grid(row=0, column=2, padx=20) # Crear una etiqueta con el texto "Categoría:" y colocarla en la fila 0, columna 2 del grid del frame superior, con un margen horizontal de 20 píxeles
combo_categoria = ttk.Combobox(
    frame_superior,
    values=["Todas", "Desayuno", "Comida", "Cena", "Postre"], # Crear un combobox para seleccionar la categoría de las recetas, con las opciones "Todas", "Desayuno", "Comida", "Cena" y "Postre"
    state="readonly", # Establece que el usuario solo pueda seleccionar una opción de la lista y no pueda escribir en el campo
    width=20
)
combo_categoria.set("Todas") # Establecer el valor predeterminado del combobox de categoría a "Todas"
combo_categoria.grid(row=0, column=3, padx=5) # Colocar el combobox de categoría en la fila 0, columna 3 del grid del frame superior, con un margen horizontal de 5 píxeles

# ===== FRAME CENTRAL =====
frame_central = tk.Frame(ventana)
frame_central.pack(fill=tk.BOTH, expand=True, padx=20)

# ===== TABLA =====
frame_tabla = tk.Frame(frame_central) # Crear un frame para contener la tabla de recetas en la parte central de la ventana
frame_tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

tabla = ttk.Treeview( # Crear un widget Treeview para mostrar la tabla de recetas, con las columnas "nombre", "categoria" y "tiempo"
    frame_tabla, # El widget Treeview se coloca dentro del frame_tabla
    columns=("nombre", "categoria", "tiempo"), # Definir las columnas de la tabla: "nombre", "categoria" y "tiempo"
    show="headings",
    height=18
)

# Configurar los encabezados de las columnas de la tabla
tabla.heading("nombre", text="Nombre")
tabla.heading("categoria", text="Categoría")
tabla.heading("tiempo", text="Tiempo (min)")

# Configurar el ancho y alineación de las columnas de la tabla
tabla.column("nombre", width=300)
tabla.column("categoria", width=150)
tabla.column("tiempo", width=120, anchor="center")

# Agregar una barra de desplazamiento vertical a la tabla
scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tabla.yview) # Crear un widget Scrollbar para la tabla, con orientación vertical y que controle la vista de la tabla
tabla.configure(yscrollcommand=scrollbar.set) # Configurar la tabla para que actualice la posición de la barra de desplazamiento cuando se desplace por la tabla

tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True) # Empaquetar la tabla para que se coloque a la izquierda del frame_tabla
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# ===== FUNCIONES LAMBDA =====

# Función lambda para actualizar la tabla de recetas en la interfaz gráfica, eliminando todas las filas actuales y 
# agregando las recetas almacenadas en la lista 'recetas'
actualizar_tabla = lambda: (
    tabla.delete(*tabla.get_children()),
    [tabla.insert("", tk.END, values=(r["nombre"], r["categoria"], r["tiempo"])) for r in recetas]
)

# Función lambda para buscar recetas en la tabla según el texto ingresado en el campo de búsqueda y la categoría seleccionada en el combobox, 
# filtrando las recetas que coincidan con los criterios de búsqueda y actualizando la tabla con los resultados
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

# Vincular los eventos de teclado en el campo de búsqueda y la selección del combobox de categoría 
# para que se ejecute la función de búsqueda cada vez que el usuario escriba o cambie la categoría
entrada_busqueda.bind("<KeyRelease>", buscar)
combo_categoria.bind("<<ComboboxSelected>>", buscar)

# ===== AGREGAR RECETA =====

# Función lambda para agregar una nueva receta a la lista de recetas, mostrando una ventana emergente
agregar = lambda: (
    (v_agregar := tk.Toplevel(ventana),
     v_agregar.title("Agregar Receta"),
     v_agregar.geometry("400x450")),

# Crear los campos de entrada para el nombre, categoría, tiempo e ingredientes de la receta, y los botones para guardar o cancelar la acción
    tk.Label(v_agregar, text="Nombre:").pack(pady=5),
    (e_nombre := tk.Entry(v_agregar, width=40), e_nombre.pack(pady=5)),

# Crear un combobox para seleccionar la categoría de la receta, con las opciones "Desayuno", "Comida", "Cena" y "Postre"
    tk.Label(v_agregar, text="Categoría:").pack(pady=5),
    (c_cat := ttk.Combobox(
        v_agregar,
        values=["Desayuno", "Comida", "Cena", "Postre"],
        state="readonly",
        width=38
    ), c_cat.pack(pady=5)),

# Crear un campo de entrada para el tiempo de preparación de la receta, con una etiqueta que indique que se debe ingresar el tiempo en minutos
    tk.Label(v_agregar, text="Tiempo (min):").pack(pady=5),
    (e_tiempo := tk.Entry(v_agregar, width=40), e_tiempo.pack(pady=5)),

# Crear un campo de texto para ingresar los ingredientes de la receta, con una etiqueta que indique que se deben ingresar los ingredientes
    tk.Label(v_agregar, text="Ingredientes:").pack(pady=5),
    (t_ing := tk.Text(v_agregar, height=5, width=40), t_ing.pack(pady=5)),

# Crear un botón para guardar la receta, que al hacer clic verifique que todos los campos estén completos
    tk.Button(
        v_agregar,
        text="Guardar",
        bg="green",
        fg="white",
        width=20,
        command=lambda: (
            messagebox.showerror("Error", "Completa todos los campos")
            if (e_nombre.get() == "" or c_cat.get() == "" or e_tiempo.get() == "" or t_ing.get("1.0", tk.END).strip() == "") # Verificar que ninguno de los campos esté vacío, mostrando un mensaje de error si alguno está incompleto
            else (
                recetas.append({
                    "nombre": e_nombre.get(),
                    "categoria": c_cat.get(),
                    "tiempo": e_tiempo.get(),
                    "ingredientes": t_ing.get("1.0", tk.END).strip()
                }),
                open(ruta_json, "w", encoding="utf-8").write(json.dumps(recetas, indent=4, ensure_ascii=False)), # Guardar la nueva receta en el archivo JSON
                actualizar_tabla(),
                buscar(),
                messagebox.showinfo("Éxito", "Receta guardada"), # Mostrar un mensaje de éxito indicando que la receta ha sido guardada correctamente
                v_agregar.destroy()
            )
        )
    ).pack(pady=10),

# Crear un botón para cancelar la acción de agregar una nueva receta, que al hacer clic cierre la ventana emergente sin guardar ningún cambio   
    tk.Button(v_agregar, text="Cancelar", command=v_agregar.destroy, width=20).pack(pady=5)
)

# ===== VER RECETA =====
ver = lambda: (
    messagebox.showerror("Error", "Selecciona una receta")
    if not tabla.selection()
    else (
        nombre_sel := tabla.item(tabla.selection()[0])["values"][0], # Obtener el nombre de la receta seleccionada en la tabla
        messagebox.showinfo(
            "Detalles",
            "\n".join([
                f"Nombre: {r['nombre']}\n"
                f"Categoría: {r['categoria']}\n"
                f"Tiempo: {r['tiempo']} min\n\n"
                f"Ingredientes:\n{r['ingredientes']}"
                for r in recetas if r["nombre"] == nombre_sel # Buscar la receta en la lista de recetas que coincida con el nombre seleccionado y mostrar sus detalles en un mensaje de información
            ])
        )
    )[-1] # El [-1] al final de la función lambda se utiliza para devolver el resultado de la última expresión evaluada dentro del bloque de código
)

# ===== ELIMINAR RECETA =====

# Función lambda para eliminar una receta seleccionada en la tabla, mostrando un mensaje de confirmación antes de eliminarla
eliminar = lambda: (
    messagebox.showerror("Error", "Selecciona una receta")
    if not tabla.selection() # Verificar si no hay ninguna receta seleccionada en la tabla, mostrando un mensaje de error si no se ha seleccionado ninguna receta   
    else (
        nombre_sel := tabla.item(tabla.selection()[0])["values"][0],
        messagebox.askyesno("Confirmar", f"¿Eliminar '{nombre_sel}'?") 
        and (
            recetas.pop(next(i for i, r in enumerate(recetas) if r["nombre"] == nombre_sel)), # Eliminar la receta de la lista de recetas utilizando pop() y next() para encontrar el índice de la receta que coincide con el nombre seleccionado
            open(ruta_json, "w", encoding="utf-8").write(json.dumps(recetas, indent=4, ensure_ascii=False)),
            actualizar_tabla(),
            buscar(),
            messagebox.showinfo("Éxito", "Receta eliminada")
        )
    )[-1]
)

# ===== BOTONES =====

# Crear un frame para contener los botones de agregar, ver y eliminar recetas en la parte derecha del frame central
frame_botones = tk.Frame(frame_central)
frame_botones.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

# Crear los botones para agregar, ver y eliminar recetas, con estilos de fondo y texto para diferenciarlos visualmente

tk.Button(frame_botones, text="Agregar Receta", bg="green", fg="white", command=agregar).pack(pady=10, fill=tk.X)
tk.Button(frame_botones, text="Ver Receta", command=ver).pack(pady=10, fill=tk.X)
tk.Button(frame_botones, text="Eliminar", bg="red", fg="white", command=eliminar).pack(pady=10, fill=tk.X)

# ===== INICIAR =====
actualizar_tabla()
ventana.mainloop()
