from tkinter import *
from Ordenes.menu_ordenes import menu_ordenes_
from Productos.menu_productos import menu_producto_
from Usuarios.menu_usuarios import menu_usuario_
from Ingredientes.menu_ingredientes import menu_ingrediente_

def menu_principal():
    ventana_menu=Tk()
    ventana_menu.title("Menu Principal")
    ventana_menu.geometry("1920x1080")
    ventana_menu.state("zoomed")

    fondo=Frame(ventana_menu, bg="#D6D0C5")
    fondo.pack_propagate(False)
    fondo.pack(fill="both", expand=True)

    fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
    fondo2.pack_propagate(False)
    fondo2.pack(padx=99, pady=50)

    contenedor_botones=Frame(fondo2, bg="white", width=550, height=790)
    contenedor_botones.pack_propagate(False)
    contenedor_botones.pack(padx=300, pady=20)

    titulo=Label(contenedor_botones, text="El Barón Rojo",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
    titulo.pack(padx=20, pady=20)

    orden=Button(contenedor_botones, text="Ordenes", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: menu_ordenes_(ventana_menu))
    orden.pack(padx=20, pady=10, fill="x")
    
    productos=Button(contenedor_botones, text="Productos", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: menu_producto_(ventana_menu))
    productos.pack(padx=20, pady=10, fill="x")
    
    ingredientes=Button(contenedor_botones, text="Ingredientes", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: menu_ingrediente_(ventana_menu))
    ingredientes.pack(padx=20, pady=10, fill="x")

    contenedor_botones2=Frame(contenedor_botones, bg="#A6171C")
    contenedor_botones2.pack()

    salir=Button(contenedor_botones2, text="Salir", font=("Inter", 24), fg="#A6171C", bg="#F1C045",command=ventana_menu.quit())
    salir.pack(padx=20, pady=10, side=LEFT, fill="x")

    usuarios=Button(contenedor_botones2, text="Usuarios", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: menu_usuario_(ventana_menu))
    usuarios.pack(padx=20, pady=10, side=LEFT, fill="x")

    ventana_menu.mainloop()
