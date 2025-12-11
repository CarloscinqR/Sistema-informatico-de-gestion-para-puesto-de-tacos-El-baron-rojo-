from tkinter import *
from view import user,ordenes,productos,ingredientes
from controller import funciones

class interfacesMenu():
    def __init__(self,ventana_menu):
        ventana_menu.title("Menu Principal")
        ventana_menu.geometry("1920x1080")
        ventana_menu.state("zoomed")
        self.menu_principal(ventana_menu)
        
    def menu_principal(self, ventana_menu):
        self.borrarPantalla(ventana_menu)

        # ===== FONDO PRINCIPAL =====
        fondo = Frame(ventana_menu, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        # ===== CONTENEDOR ROJO =====
        fondo2 = Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        # ===== TARJETA CENTRAL =====
        contenedor_botones = Frame(
            fondo2,
            bg="#A6171C",
            width=500,
            height=750
        )
        contenedor_botones.pack_propagate(False)
        contenedor_botones.pack(padx=300, pady=20)

        # ===== TÍTULO =====
        lbl_titulo = Label(
            contenedor_botones,
            text="El Barón Rojo",
            font=("Orelega One", 50, "bold"),
            fg="white",
            bg="#A6171C"
        )
        lbl_titulo.pack(pady=25)

        # ===== ESTILO DE BOTONES AJUSTADO =====
        estilo_boton = {
            "font": ("Inter", 22, "bold"),
            "fg": "#A6171C",
            "bg": "white",
            "activebackground": "#E6E6E6",
            "activeforeground": "#A6171C",
            "bd": 0,
            "relief": "flat",
            "cursor": "hand2",
            "height": 1,        # <<<<< Más proporcionado
            "pady": 10          # <<<<< Reduce altura visual
        }

        # ===== BOTONES =====
        btn_orden = Button(
            contenedor_botones,
            text="Órdenes",
            command=lambda: self.menuOrden(ventana_menu),
            **estilo_boton
        )
        btn_orden.pack(padx=20, pady=12, fill="x")

        # Obtener rol actual (guardado en controller.funciones por el login)
        current_role = None
        try:
            current_role = funciones.get_current_user_role()
        except Exception:
            try:
                current_role = funciones.current_user_role
            except Exception:
                current_role = None

        # Si el usuario es 'Empleado', solo mostrar el botón Órdenes y Salir
        if current_role == 'Empleado':
            btn_salir = Button(
                contenedor_botones,
                text="Salir",
                command=ventana_menu.quit,
                **estilo_boton
            )
            btn_salir.pack(padx=20, pady=12, fill="x")
            return

        btn_productos = Button(
            contenedor_botones,
            text="Productos",
            command=lambda: self.menuProductos(ventana_menu),
            **estilo_boton
        )
        btn_productos.pack(padx=20, pady=12, fill="x")

        btn_ingredientes = Button(
            contenedor_botones,
            text="Ingredientes",
            command=lambda: self.menuIngredientes(ventana_menu),
            **estilo_boton
        )
        btn_ingredientes.pack(padx=20, pady=12, fill="x")

        btn_usuarios = Button(
            contenedor_botones,
            text="Usuarios",
            command=lambda: self.menuUsuario(ventana_menu),
            **estilo_boton
        )
        btn_usuarios.pack(padx=20, pady=12, fill="x")

        btn_salir = Button(
            contenedor_botones,
            text="Salir",
            command=ventana_menu.quit,
            **estilo_boton
        )
        btn_salir.pack(padx=20, pady=12, fill="x")

    

    def menuUsuario(self,ventana_menu):  
        self.borrarPantalla(ventana_menu)
        user.interfacesUsuario(ventana_menu)

    def menuOrden(self,ventana_menu):  
        self.borrarPantalla(ventana_menu)
        ordenes.interfacesOrdenes(ventana_menu)
    
    def menuProductos(self,ventana_menu):  
        self.borrarPantalla(ventana_menu)
        productos.interfacesProducto(ventana_menu)

    def menuIngredientes(self,ventana_menu):  
        self.borrarPantalla(ventana_menu)
        ingredientes.interfacesIngrediente(ventana_menu)


    def borrarPantalla(self,ventana_menu):
        for widget in ventana_menu.winfo_children():
            widget.destroy()

