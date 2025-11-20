from tkinter import *
from view.Productos.nuevo_producto import nuevoproducto
from view.Productos.modificar_producto import modificarproducto
from view.Productos.ver_productos import verproductos


class menuproducto():
    @staticmethod
    def menu_producto_(ventana_menu):
        ventana_menu.destroy()
        menu_productos=Tk()
        menu_productos.title("Menu productos")
        menu_productos.geometry("1920x1080")
        menu_productos.state("zoomed")

        fondo=Frame(menu_productos, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        contenedor_botones=Frame(fondo2, bg="#A6171C", width=550, height=790)
        contenedor_botones.pack_propagate(False)
        contenedor_botones.pack(padx=300, pady=20)

        titulo=Label(contenedor_botones, text="Productos",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
        titulo.pack(padx=20, pady=20)

        nuevoProducto=Button(contenedor_botones, text="Nuevo producto", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: nuevoproducto.nuevo_producto_(menu_productos))
        nuevoProducto.pack(padx=20, pady=10, fill="x")
        
        verProducto=Button(contenedor_botones, text="Ver productos", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: verproductos.ver_productos_(menu_productos))
        verProducto.pack(padx=20, pady=10, fill="x")

        modificarProducto=Button(contenedor_botones, text="Modificar producto", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: modificarproducto.modificar_producto_(menu_productos))
        modificarProducto.pack(padx=20, pady=10, fill="x")
        

        def volver_al_menu_principal():
            from view.Menu_Principal.menu_principal import menuprincipal
            menu_productos.destroy()
            menuprincipal.menu_principal()

        regresar=Button(contenedor_botones, text="Regresar", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=volver_al_menu_principal)
        regresar.pack(padx=20, pady=10, fill="x")

