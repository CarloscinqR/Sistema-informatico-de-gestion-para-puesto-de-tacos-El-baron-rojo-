from tkinter import *
from Ordenes.nueva_orden import nueva_orden_
from Ordenes.ver_ordenes import ver_ordenes_

def menu_ordenes_(ventana_menu):
    ventana_menu.destroy()
    menu_ordenes=Tk()
    menu_ordenes.title("Menu ordenes")
    menu_ordenes.geometry("1920x1080")
    menu_ordenes.state("zoomed")

    fondo=Frame(menu_ordenes, bg="#D6D0C5")
    fondo.pack_propagate(False)
    fondo.pack(fill="both", expand=True)

    fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
    fondo2.pack_propagate(False)
    fondo2.pack(padx=99, pady=50)

    contenedor_botones=Frame(fondo2, bg="white", width=550, height=790)
    contenedor_botones.pack_propagate(False)
    contenedor_botones.pack(padx=300, pady=20)

    titulo=Label(contenedor_botones, text="Ordenes",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
    titulo.pack(padx=20, pady=20)

    nuevaOrden=Button(contenedor_botones, text="Nueva orden", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: nueva_orden_(menu_ordenes))
    nuevaOrden.pack(padx=20, pady=10, fill="x")
    
    verOrden=Button(contenedor_botones, text="Ver ordenes", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command= lambda: ver_ordenes_(menu_ordenes))
    verOrden.pack(padx=20, pady=10, fill="x")

    modificarOrden=Button(contenedor_botones, text="Modificar orden", font=("Inter", 24), fg="#A6171C", bg="#F1C045")
    modificarOrden.pack(padx=20, pady=10, fill="x")
    
    def volver_al_menu_principal():
        from Menu_Principal.menu_principal import menu_principal
        menu_ordenes.destroy()
        menu_principal()

    regresar=Button(contenedor_botones, text="Regresar", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=volver_al_menu_principal)
    regresar.pack(padx=20, pady=10, fill="x")
