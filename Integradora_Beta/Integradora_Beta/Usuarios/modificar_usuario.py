from tkinter import *
from tkinter import ttk

def modificar_usuario_(menu_usuario):
    menu_usuario.destroy()
    modificar_usuario=Tk()
    modificar_usuario.title("Modificar usuario")
    modificar_usuario.geometry("1920x1080")
    modificar_usuario.state("zoomed")

    fondo=Frame(modificar_usuario, bg="#D6D0C5")
    fondo.pack_propagate(False)
    fondo.pack(fill="both", expand=True)

    fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
    fondo2.pack_propagate(False)
    fondo2.pack(padx=99, pady=50)

    titulo=Label(fondo2, text="Modificar usuarios",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
    titulo.pack(padx=20, pady=20)

    fondo3=Frame(fondo2, bg="white", height=180)
    fondo3.pack(expand=True)

    def volver_a_menu():
        from Usuarios.menu_usuarios import menu_usuario_
        menu_usuario_(modificar_usuario)

    usuario_modificado=Label(fondo3, text="Selecciona el usuario a modificar", font=("Inter", 24), bg="white")
    usuario_modificado.pack(padx=20, pady=10)

    usuarios=[
        "Usuario 1",
        "Usuario 2",
        "Usuario 3",
        "usuario 4"
    ]

    usuario_modificado_combo=ttk.Combobox(fondo3, values=usuarios, font=("Inter", 24))
    usuario_modificado_combo.set("Selecciona un usuario")
    usuario_modificado_combo.pack(padx=20, pady=10)

    def on_select(event):
        print("Producto seleccionado:", usuario_modificado_combo.get())
    
    usuario_modificado_combo.bind('<<ComboboxSelected>>', on_select)


    nombre=Label(fondo3, text="Nuevo nombre", font=("Inter", 24), bg="white")
    nombre.pack(padx=20, pady=10)
    
    nombre_entry=Entry(fondo3, font=("Inter", 24), bg="white")
    nombre_entry.pack(padx=20, pady=10)

    contrasenia=Label(fondo3, text="Nueva contraseña", font=("Inter", 24), bg="white")
    contrasenia.pack(padx=20, pady=10)

    contrasenia_entry=Entry(fondo3, font=("Inter", 24), bg="white")
    contrasenia_entry.pack(padx=20, pady=10)

    regresar=Button(fondo3, text="Regresar", font=("Inter", 24), bg="#F1C045", command=volver_a_menu)
    regresar.pack(padx=20, pady=10)
    
    agregar=Button(fondo3, text="Agregar", font=("Inter", 24), bg="#F1C045")
    agregar.pack(padx=20, pady=10)