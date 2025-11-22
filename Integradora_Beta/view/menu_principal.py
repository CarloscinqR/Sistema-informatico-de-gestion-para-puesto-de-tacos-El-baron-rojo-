from tkinter import *
from view import user,ordenes,productos,ingredientes

class interfacesMenu():
    def __init__(self,ventana_menu):
        ventana_menu.title("Menu Principal")
        ventana_menu.geometry("1920x1080")
        ventana_menu.state("zoomed")
        self.menu_principal(ventana_menu)
        
    def menu_principal(self,ventana_menu):
        self.borrarPantalla(ventana_menu)
        fondo=Frame(ventana_menu, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        contenedor_botones=Frame(fondo2, bg="#A6171C", width=550, height=790)
        contenedor_botones.pack_propagate(False)
        contenedor_botones.pack(padx=300, pady=20)

        lbl_titulo=Label(contenedor_botones, text="El Barón Rojo",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
        lbl_titulo.pack(padx=20, pady=20)
        
        btn_orden=Button(contenedor_botones, text="Ordenes", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: self.menuOrden(ventana_menu))
        btn_orden.pack(padx=20, pady=10, fill="x")
        
        btn_productos=Button(contenedor_botones, text="Productos", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: self.menuProductos(ventana_menu))
        btn_productos.pack(padx=20, pady=10, fill="x")
        
        btn_ingredientes=Button(contenedor_botones, text="Ingredientes", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: self.menuIngredientes(ventana_menu))
        btn_ingredientes.pack(padx=20, pady=10, fill="x")

        btn_usuarios=Button(contenedor_botones, text="Usuarios", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: self.menuUsuario(ventana_menu))
        btn_usuarios.pack(padx=20, pady=10, fill="x")

        btn_salir=Button(contenedor_botones, text="Salir", font=("Inter", 24), fg="#A6171C", bg="#F1C045",command=ventana_menu.quit)
        btn_salir.pack(padx=20, pady=10, fill="x")
    

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

