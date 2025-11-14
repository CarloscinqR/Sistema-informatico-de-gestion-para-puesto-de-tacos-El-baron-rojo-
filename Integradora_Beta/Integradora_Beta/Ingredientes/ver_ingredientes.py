from tkinter import *

def ver_ingredientes_(ventana_menu):
    ventana_menu.destroy()
    ver_ingredientes=Tk()
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

    titulo=Label(contenedor_botones, text="Ver ingredientes",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
    titulo.pack(padx=20, pady=20)
    
    def volver_a_menu():
        from Ingredientes.menu_ingredientes import menu_ingrediente_
        menu_ingrediente_(ver_ingredientes)

    regresar=Button(contenedor_botones, text="Regresar", font=("Inter", 24), bg="#F1C045", command=volver_a_menu)
    regresar.pack(padx=20, pady=10)
