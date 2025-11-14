from tkinter import *

def ver_usuarios_(ventana_menu):
    ventana_menu.destroy()
    ver_usuarios=Tk()
    ver_usuarios.title("Ver usuarios")
    ver_usuarios.geometry("1920x1080")
    ver_usuarios.state("zoomed")

    fondo=Frame(ver_usuarios, bg="#D6D0C5")
    fondo.pack_propagate(False)
    fondo.pack(fill="both", expand=True)

    fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
    fondo2.pack_propagate(False)
    fondo2.pack(padx=99, pady=50)

    contenedor_botones=Frame(fondo2, bg="white", width=550, height=790)
    contenedor_botones.pack_propagate(False)
    contenedor_botones.pack(padx=300, pady=20)

    titulo=Label(contenedor_botones, text="Ver usuarios",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
    titulo.pack(padx=20, pady=20)
    
    def volver_a_menu():
        from Usuarios.menu_usuarios import menu_usuario_
        menu_usuario_(ver_usuarios)

    regresar=Button(contenedor_botones, text="Regresar", font=("Inter", 24), bg="#F1C045", command=volver_a_menu)
    regresar.pack(padx=20, pady=10)
