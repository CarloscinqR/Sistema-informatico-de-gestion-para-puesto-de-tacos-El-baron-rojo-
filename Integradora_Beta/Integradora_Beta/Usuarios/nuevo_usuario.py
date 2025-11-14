from tkinter import *

def nuevo_usuario_(menu_usuario):
    menu_usuario.destroy()
    nuevo_usuario=Tk()
    nuevo_usuario.title("Nnuevo usuario")
    nuevo_usuario.geometry("1920x1080")
    nuevo_usuario.state("zoomed")

    fondo=Frame(nuevo_usuario, bg="#D6D0C5")
    fondo.pack_propagate(False)
    fondo.pack(fill="both", expand=True)

    fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
    fondo2.pack_propagate(False)
    fondo2.pack(padx=99, pady=50)

    titulo=Label(fondo2, text="Nuevo usuario",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
    titulo.pack(padx=20, pady=20)

    fondo3=Frame(fondo2, bg="white", height=180)
    fondo3.pack(expand=True)

    def volver_a_menu():
        from Usuarios.menu_usuarios import menu_usuario_
        menu_usuario_(nuevo_usuario)

    nombre=Label(fondo3, text="Nombre", font=("Inter", 24), bg="white")
    nombre.pack(padx=20, pady=10)
    
    nombre_entry=Entry(fondo3, font=("Inter", 24), bg="white")
    nombre_entry.pack(padx=20, pady=10)

    contrasenia=Label(fondo3, text="contraseña", font=("Inter", 24), bg="white")
    contrasenia.pack(padx=20, pady=10)

    contrasenia_entry=Entry(fondo3, font=("Inter", 24), bg="white")
    contrasenia_entry.pack(padx=20, pady=10)

    regresar=Button(fondo3, text="Regresar", font=("Inter", 24), bg="#F1C045", command=volver_a_menu)
    regresar.pack(padx=20, pady=10)
    
    agregar=Button(fondo3, text="Agregar", font=("Inter", 24), bg="#F1C045")
    agregar.pack(padx=20, pady=10)