import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

# Ruta donde guardar las recetas
ruta_json = "recetas.json"

class Recetario:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Recetario de Cocina")
        self.ventana.geometry("700x500")
        
        # Cargar recetas del JSON
        self.recetas = self.cargar_recetas()
        
        # ===== FRAME DE BUSQUEDA =====
        frame_busqueda = tk.Frame(ventana)
        frame_busqueda.pack(pady=10)
        
        tk.Label(frame_busqueda, text="Buscar:").pack(side=tk.LEFT, padx=5)
        self.entrada_busqueda = tk.Entry(frame_busqueda, width=30)
        self.entrada_busqueda.pack(side=tk.LEFT, padx=5)
        self.entrada_busqueda.bind("<KeyRelease>", lambda e: self.buscar())
        
        # ===== FRAME DE FILTRO POR CATEGORIA =====
        frame_filtro = tk.Frame(ventana)
        frame_filtro.pack(pady=10)
        
        tk.Label(frame_filtro, text="Categoría:").pack(side=tk.LEFT, padx=5)
        self.combo_categoria = ttk.Combobox(frame_filtro, 
                                           values=["Todas", "Desayuno", "Comida", "Cena", "Postre"],
                                           state="readonly", width=20)
        self.combo_categoria.set("Todas")
        self.combo_categoria.pack(side=tk.LEFT, padx=5)
        self.combo_categoria.bind("<<ComboboxSelected>>", lambda e: self.buscar())
        
        # ===== FRAME DE LA TABLA =====
        frame_tabla = tk.Frame(ventana)
        frame_tabla.pack(pady=10, fill=tk.BOTH, expand=True, padx=10)
        
        # Treeview para mostrar las recetas
        self.tabla = ttk.Treeview(frame_tabla, columns=("nombre", "categoria", "tiempo"), height=15)
        self.tabla.column("#0", width=0, stretch=tk.NO)
        self.tabla.column("nombre", anchor=tk.W, width=250)
        self.tabla.column("categoria", anchor=tk.W, width=150)
        self.tabla.column("tiempo", anchor=tk.W, width=100)
        
        self.tabla.heading("#0", text="")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("categoria", text="Categoría")
        self.tabla.heading("tiempo", text="Tiempo (min)")
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set)
        
        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Cargar recetas a la tabla
        self.actualizar_tabla()
        
        # ===== FRAME DE BOTONES =====
        frame_botones = tk.Frame(ventana)
        frame_botones.pack(pady=10)
        
        btn_agregar = tk.Button(frame_botones, text="Agregar Receta", command=self.abrir_agregar, bg="green", fg="white")
        btn_agregar.pack(side=tk.LEFT, padx=5)
        
        btn_ver = tk.Button(frame_botones, text="Ver Receta", command=self.ver_receta)
        btn_ver.pack(side=tk.LEFT, padx=5)
        
        btn_eliminar = tk.Button(frame_botones, text="Eliminar", command=self.eliminar_receta, bg="red", fg="white")
        btn_eliminar.pack(side=tk.LEFT, padx=5)
    
    # ===== FUNCIONES DE BUSQUEDA =====
    def buscar(self):
        # Obtener valores de búsqueda
        texto_busqueda = self.entrada_busqueda.get().lower()
        categoria_seleccionada = self.combo_categoria.get()
        
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # Filtrar y mostrar recetas
        for receta in self.recetas:
            nombre = receta["nombre"].lower()
            categoria = receta["categoria"]
            ingredientes = str(receta.get("ingredientes", "")).lower()
            
            # Verificar si coincide con la búsqueda
            coincide_busqueda = (texto_busqueda == "" or 
                                texto_busqueda in nombre or 
                                texto_busqueda in ingredientes)
            
            # Verificar si coincide con la categoría
            coincide_categoria = (categoria_seleccionada == "Todas" or 
                                 categoria == categoria_seleccionada)
            
            # Si coincide con ambos, mostrar
            if coincide_busqueda and coincide_categoria:
                self.tabla.insert("", tk.END, values=(receta["nombre"], receta["categoria"], receta["tiempo"]))
    
    # ===== FUNCIONES DE TABLA =====
    def actualizar_tabla(self):
        # Limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        
        # Mostrar todas las recetas
        for receta in self.recetas:
            self.tabla.insert("", tk.END, values=(receta["nombre"], receta["categoria"], receta["tiempo"]))
    
    # ===== FUNCIONES DE RECETAS =====
    def abrir_agregar(self):
        # Crear ventana nueva
        ventana_agregar = tk.Toplevel(self.ventana)
        ventana_agregar.title("Agregar Nueva Receta")
        ventana_agregar.geometry("400x400")
        
        # Nombre
        tk.Label(ventana_agregar, text="Nombre de la Receta:").pack(pady=5)
        entrada_nombre = tk.Entry(ventana_agregar, width=40)
        entrada_nombre.pack(pady=5)
        
        # Categoría
        tk.Label(ventana_agregar, text="Categoría:").pack(pady=5)
        combo_cat = ttk.Combobox(ventana_agregar, values=["Desayuno", "Comida", "Cena", "Postre"], state="readonly")
        combo_cat.pack(pady=5)
        
        # Tiempo de preparación
        tk.Label(ventana_agregar, text="Tiempo (minutos):").pack(pady=5)
        entrada_tiempo = tk.Entry(ventana_agregar, width=40)
        entrada_tiempo.pack(pady=5)
        
        # Ingredientes (simple)
        tk.Label(ventana_agregar, text="Ingredientes (separados por comas):").pack(pady=5)
        texto_ingredientes = tk.Text(ventana_agregar, height=5, width=40)
        texto_ingredientes.pack(pady=5)
        
        # Función para guardar
        def guardar():
            nombre = entrada_nombre.get()
            categoria = combo_cat.get()
            tiempo = entrada_tiempo.get()
            ingredientes = texto_ingredientes.get("1.0", tk.END).strip()
            
            # Validar que los campos no estén vacíos
            if not nombre or not categoria or not tiempo or not ingredientes:
                messagebox.showerror("Error", "Completa todos los campos")
                return
            
            # Crear receta
            receta = {
                "nombre": nombre,
                "categoria": categoria,
                "tiempo": tiempo,
                "ingredientes": ingredientes
            }
            
            # Agregar a la lista
            self.recetas.append(receta)
            
            # Guardar en JSON
            self.guardar_recetas()
            
            # Actualizar tabla
            self.actualizar_tabla()
            
            messagebox.showinfo("Éxito", "Receta guardada correctamente")
            ventana_agregar.destroy()
        
        # Botones
        btn_guardar = tk.Button(ventana_agregar, text="Guardar", command=guardar, bg="green", fg="white")
        btn_guardar.pack(pady=10)
        
        btn_cancelar = tk.Button(ventana_agregar, text="Cancelar", command=ventana_agregar.destroy)
        btn_cancelar.pack(pady=5)
    
    def ver_receta(self):
        # Obtener la receta seleccionada
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona una receta")
            return
        
        item = self.tabla.item(seleccion[0])
        nombre_seleccionado = item["values"][0]
        
        # Buscar la receta en la lista
        for receta in self.recetas:
            if receta["nombre"] == nombre_seleccionado:
                # Mostrar detalles
                detalles = f"""
Nombre: {receta['nombre']}
Categoría: {receta['categoria']}
Tiempo: {receta['tiempo']} minutos

Ingredientes:
{receta['ingredientes']}
                """
                messagebox.showinfo("Detalles de la Receta", detalles)
                return
    
    def eliminar_receta(self):
        # Obtener la receta seleccionada
        seleccion = self.tabla.selection()
        if not seleccion:
            messagebox.showerror("Error", "Selecciona una receta para eliminar")
            return
        
        item = self.tabla.item(seleccion[0])
        nombre_seleccionado = item["values"][0]
        
        # Confirmar eliminación
        if messagebox.askyesno("Confirmar", f"¿Eliminar '{nombre_seleccionado}'?"):
            # Buscar y eliminar
            for i, receta in enumerate(self.recetas):
                if receta["nombre"] == nombre_seleccionado:
                    self.recetas.pop(i)
                    break
            
            # Guardar cambios
            self.guardar_recetas()
            
            # Actualizar tabla
            self.actualizar_tabla()
            messagebox.showinfo("Éxito", "Receta eliminada")
    
    # ===== FUNCIONES DE ARCHIVO JSON =====
    def cargar_recetas(self):
        # Si el archivo existe, cargarlo
        if os.path.exists(ruta_json):
            try:
                with open(ruta_json, "r", encoding="utf-8") as archivo:
                    return json.load(archivo)
            except:
                return []
        return []
    
    def guardar_recetas(self):
        # Guardar en JSON
        with open(ruta_json, "w", encoding="utf-8") as archivo:
            json.dump(self.recetas, archivo, indent=4, ensure_ascii=False)

# Crear la ventana principal
if __name__ == "__main__":
    ventana_principal = tk.Tk()
    app = Recetario(ventana_principal)
    ventana_principal.mainloop()