from tkinter import *
from Ingredientes.nuevo_ingrediente import nuevo_ingrediente_
from Ingredientes.modificar_ingrediente import modificar_ingrediente_
from Ingredientes.ver_ingredientes import ver_ingredientes_

def menu_ingrediente_(ventana_menu):
    ventana_menu.destroy()
    menu_ingredientes=Tk()
    menu_ingredientes.title("Menu ingredientes")
    menu_ingredientes.geometry("1920x1080")
    menu_ingredientes.state("zoomed")

    fondo=Frame(menu_ingredientes, bg="#D6D0C5")
    fondo.pack_propagate(False)
    fondo.pack(fill="both", expand=True)

    fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
    fondo2.pack_propagate(False)
    fondo2.pack(padx=99, pady=50)

    contenedor_botones=Frame(fondo2, bg="white", width=550, height=790)
    contenedor_botones.pack_propagate(False)
    contenedor_botones.pack(padx=300, pady=20)

    titulo=Label(contenedor_botones, text="Ingredientes",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
    titulo.pack(padx=20, pady=20)

    nuevoIngrediente=Button(contenedor_botones, text="Nuevo ingrediente", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: nuevo_ingrediente_(menu_ingredientes))
    nuevoIngrediente.pack(padx=20, pady=10, fill="x")
    
    verIngrediente=Button(contenedor_botones, text="Ver ingredientes", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: ver_ingredientes_(menu_ingredientes))
    verIngrediente.pack(padx=20, pady=10, fill="x")

    modificarIngrediente=Button(contenedor_botones, text="Modificar ingredientes", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: modificar_ingrediente_(menu_ingredientes))
    modificarIngrediente.pack(padx=20, pady=10, fill="x")
    
    def volver_al_menu_principal():
        from Menu_Principal.menu_principal import menu_principal
        menu_ingredientes.destroy()
        menu_principal()

    regresar=Button(contenedor_botones, text="Regresar", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=volver_al_menu_principal)
    regresar.pack(padx=20, pady=10, fill="x")
