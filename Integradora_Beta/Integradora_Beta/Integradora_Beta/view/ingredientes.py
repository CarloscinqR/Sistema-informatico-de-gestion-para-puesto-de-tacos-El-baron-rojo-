from tkinter import *
from tkinter import ttk
from view import menu_principal

class interfacesIngrediente():
    def __init__(self,menu_ingredientes):
        menu_ingredientes.title("Menu ingredientes")
        menu_ingredientes.geometry("1920x1080")
        menu_ingredientes.state("zoomed")
        self.menu_ingrediente(menu_ingredientes)

    def borrarPantalla(self,ventana_login):
        for widget in ventana_login.winfo_children():
            widget.destroy()

    def menu_ingrediente(self,menu_ingredientes):
        self.borrarPantalla(menu_ingredientes)
        fondo=Frame(menu_ingredientes, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        contenedor_botones=Frame(fondo2, bg="#A6171C", width=550, height=790)
        contenedor_botones.pack_propagate(False)
        contenedor_botones.pack(padx=300, pady=20)

        lbl_titulo=Label(contenedor_botones, text="Ingredientes",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
        lbl_titulo.pack(padx=20, pady=20)

        btn_nuevoIngrediente=Button(contenedor_botones, text="Nuevo ingrediente", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: self.nuevoIngrediente(menu_ingredientes))
        btn_nuevoIngrediente.pack(padx=20, pady=10, fill="x")
        
        btn_verIngrediente=Button(contenedor_botones, text="Ver ingredientes", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: self.verIngrediente(menu_ingredientes))
        btn_verIngrediente.pack(padx=20, pady=10, fill="x")

        btn_modificarIngrediente=Button(contenedor_botones, text="Modificar ingredientes", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: self.modificarIngrediente(menu_ingredientes))
        btn_modificarIngrediente.pack(padx=20, pady=10, fill="x")

        btn_regresar=Button(contenedor_botones, text="Regresar", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: self.regresar(menu_ingredientes))
        btn_regresar.pack(padx=20, pady=10, fill="x")

    def nuevoIngrediente(self,nuevo_ingrediente):
        self.borrarPantalla(nuevo_ingrediente)
        nuevo_ingrediente.title("Nuevo ingrediente")
        nuevo_ingrediente.geometry("1920x1080")
        nuevo_ingrediente.state("zoomed")

        fondo=Frame(nuevo_ingrediente, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        lbl_titulo=Label(fondo2, text="Nuevo ingrediente",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
        lbl_titulo.pack(padx=20, pady=20)

        fondo3=Frame(fondo2, bg="white")
        fondo3.pack(expand=True)

        lbl_nombre=Label(fondo3, text="Nombre del ingrediente", font=("Inter", 24), bg="white")
        lbl_nombre.pack(padx=20, pady=10)
        
        nombre_entry=Entry(fondo3, font=("Inter", 24), bg="white")
        nombre_entry.pack(padx=20, pady=10)

        lbl_cantidad=Label(fondo3, text="Nueva cantidad", font=("Inter", 24), bg="white")
        lbl_cantidad.pack(padx=20, pady=10)

        cantidad_entry=Entry(fondo3, font=("Inter", 24), bg="white")
        cantidad_entry.pack(padx=20, pady=10)

        lbl_unidad=Label(fondo3, text="Unidad de medida", font=("Inter", 24), bg="white")
        lbl_unidad.pack(padx=20, pady=10)

        # Lista de unidades de medida comunes
        unidades_medida = [
            "Kilogramos (kg)",
            "Gramos (g)",
            "Litros (L)",
            "Mililitros (ml)",
            "Piezas (pz)",
            "Unidades (u)",
            "Paquetes (paq)"
        ]

        # Crear el Combobox
        unidad_combo = ttk.Combobox(fondo3, values=unidades_medida, font=("Inter", 24))
        unidad_combo.set("Selecciona una unidad")  # Valor por defecto
        unidad_combo.pack(padx=20, pady=10)

        # Función para cuando se selecciona una opción
        def on_select(event):
            print("Unidad seleccionada:", unidad_combo.get())
        
        # Vincular la función al evento de selección
        unidad_combo.bind('<<ComboboxSelected>>', on_select)

        lbl_producto=Label(fondo3, text="Seleccionar producto", font=("Inter", 24), bg="white")
        lbl_producto.pack(padx=20, pady=10)

        prodcutos=[
            "Producto 1",
            "Producto 2",
            "Producto 3",
            "Producto 4"
        ]

        prodcutos_combo=ttk.Combobox(fondo3, values=prodcutos, font=("Inter", 24))
        prodcutos_combo.set("Selecciona un producto")
        prodcutos_combo.pack(padx=20, pady=10)

        #def on_select(event):
        #   print("Producto seleccionado:", prodcutos_combo.get())
        
        prodcutos_combo.bind('<<ComboboxSelected>>', on_select)

        btn_regresar=Button(fondo3, text="Regresar", font=("Inter", 24), bg="#F1C045", command=lambda: self.menu_ingrediente(nuevo_ingrediente))
        btn_regresar.pack(padx=20, pady=10)
        
        btn_agregar=Button(fondo3, text="Agregar", font=("Inter", 24), bg="#F1C045")
        btn_agregar.pack(padx=20, pady=10)

    def verIngrediente(self,ver_ingredientes):
        self.borrarPantalla(ver_ingredientes)
        ver_ingredientes.title("Ver ingredientes")
        ver_ingredientes.geometry("1920x1080")
        ver_ingredientes.state("zoomed")

        fondo=Frame(ver_ingredientes, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        contenedor_botones=Frame(fondo2, bg="white", width=550, height=790)
        contenedor_botones.pack_propagate(False)
        contenedor_botones.pack(padx=300, pady=20)

        lbl_titulo=Label(contenedor_botones, text="Ver ingredientes",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
        lbl_titulo.pack(padx=20, pady=20)

        btn_regresar=Button(contenedor_botones, text="Regresar", font=("Inter", 24), bg="#F1C045", command=lambda: self.menu_ingrediente(ver_ingredientes))
        btn_regresar.pack(padx=20, pady=10)

    def modificarIngrediente(self,modificar_ingrediente):
        self.borrarPantalla(modificar_ingrediente)
        modificar_ingrediente.title("Modificar ingrediente")
        modificar_ingrediente.geometry("1920x1080")
        modificar_ingrediente.state("zoomed")

        fondo=Frame(modificar_ingrediente, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        lbl_titulo=Label(fondo2, text="Modificar ingredientes",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
        lbl_titulo.pack(padx=20, pady=20)

        fondo3=Frame(fondo2, bg="white", height=180)
        fondo3.pack(expand=True)


        lbl_ingrediente_modificado=Label(fondo3, text="Selecciona el ingrediente a modificar", font=("Inter", 18), bg="white")
        lbl_ingrediente_modificado.pack(padx=20, pady=10)

        ingredientes=[
            "Ingrediente 1",
            "Ingrediente 2",
            "Ingrediente 3",
            "Ingrediente 4"
        ]

        ingrediente_modificado_combo=ttk.Combobox(fondo3, values=ingredientes, font=("Inter", 18))
        ingrediente_modificado_combo.set("Selecciona un ingrediente")
        ingrediente_modificado_combo.pack(padx=20, pady=10)

        def on_select(event):
            print("Producto seleccionado:", ingrediente_modificado_combo.get())
        
        ingrediente_modificado_combo.bind('<<ComboboxSelected>>', on_select)

        lbl_nombre=Label(fondo3, text="Nuevo nombre del ingrediente", font=("Inter", 18), bg="white")
        lbl_nombre.pack(padx=20, pady=10)
        
        nombre_entry=Entry(fondo3, font=("Inter", 18), bg="white")
        nombre_entry.pack(padx=20, pady=10)

        lbl_cantidad=Label(fondo3, text="Nueva cantidad", font=("Inter", 18), bg="white")
        lbl_cantidad.pack(padx=20, pady=10)

        cantidad_entry=Entry(fondo3, font=("Inter", 18), bg="white")
        cantidad_entry.pack(padx=20, pady=10)

        lbl_unidad=Label(fondo3, text="Cambiar unidad de medida", font=("Inter", 18), bg="white")
        lbl_unidad.pack(padx=20, pady=10)

        # Lista de unidades de medida comunes
        unidades_medida = [
            "Kilogramos (kg)",
            "Gramos (g)",
            "Litros (L)",
            "Mililitros (ml)",
            "Piezas (pz)",
            "Unidades (u)",
            "Paquetes (paq)"
        ]

        # Crear el Combobox
        unidad_combo = ttk.Combobox(fondo3, values=unidades_medida, font=("Inter", 18))
        unidad_combo.set("Selecciona un producto")  # Valor por defecto
        unidad_combo.pack(padx=20, pady=10)

        # Función para cuando se selecciona una opción
        def on_select(event):
            print("Producto seleccionad:", unidad_combo.get())
        
        # Vincular la función al evento de selección
        unidad_combo.bind('<<ComboboxSelected>>', on_select)

        lbl_producto=Label(fondo3, text="Cambiar producto", font=("Inter", 18), bg="white")
        lbl_producto.pack(padx=20, pady=10)

        prodcutos=[
            "Producto 1",
            "Producto 2",
            "Producto 3",
            "Producto 4"
        ]

        prodcutos_combo=ttk.Combobox(fondo3, values=prodcutos, font=("Inter", 18))
        prodcutos_combo.set("Selecciona un producto")
        prodcutos_combo.pack(padx=20, pady=10)

        def on_select(event):
            print("Unidad seleccionada:", prodcutos_combo.get())
        
        prodcutos_combo.bind('<<ComboboxSelected>>', on_select)

        #Este boton no aparece y no se porqué, puede ser por el pack...
        btn_regresar=Button(fondo3, text="Regresar", font=("Inter", 18), bg="#F1C045", command=lambda: self.menu_ingrediente(modificar_ingrediente))
        btn_regresar.pack(padx=20, pady=10)
        
        btn_agregar=Button(fondo3, text="Modificar", font=("Inter", 18), bg="#F1C045")
        btn_agregar.pack(padx=20, pady=10)

    def regresar(self,menu_usuarios):
        menu_principal.interfacesMenu(menu_usuarios)