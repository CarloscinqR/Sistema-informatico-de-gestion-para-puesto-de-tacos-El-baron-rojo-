from tkinter import *

def ver_productos_(ventana_menu):
    ventana_menu.destroy()
    ver_productos=Tk()
    ver_productos.title("Ver productos")
    ver_productos.geometry("1920x1080")
    ver_productos.state("zoomed")

    fondo=Frame(ver_productos, bg="#D6D0C5")
    fondo.pack_propagate(False)
    fondo.pack(fill="both", expand=True)

    fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
    fondo2.pack_propagate(False)
    fondo2.pack(padx=99, pady=50)

    contenedor_botones=Frame(fondo2, bg="white", width=550, height=790)
    contenedor_botones.pack_propagate(False)
    contenedor_botones.pack(padx=300, pady=20)

    titulo=Label(contenedor_botones, text="Ver productos",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
    titulo.pack(padx=20, pady=20)
    
    def volver_a_menu():
        from Prodcutos.menu_productos import menu_producto_
        menu_producto_(ver_productos)

    regresar=Button(contenedor_botones, text="Regresar", font=("Inter", 24), bg="#F1C045", command=volver_a_menu)
    regresar.pack(padx=20, pady=10)
