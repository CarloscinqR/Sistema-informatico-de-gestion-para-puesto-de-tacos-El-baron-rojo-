from tkinter import *
from view import menu_principal
class InterfacesLogin():
    def __init__(self,ventana_login):
        ventana_login.title("Login")
        ventana_login.geometry("1920x1080")
        ventana_login.state("zoomed")
        self.log_in(ventana_login)

    def log_in(self,ventana_login):
        fondo=Frame(ventana_login, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        lbl_titulo=Label(fondo2, text="El Barón Rojo",font=("Orelega One", 64), fg="#F1C045", bg="#A6171C")
        lbl_titulo.pack(padx=20, pady=20, side=LEFT)

        fondo3=Frame(fondo2, bg="white", width=630, height=720)
        fondo3.pack_propagate(False)
        fondo3.pack(padx=82, pady=124)

        contenedor_login=Frame(fondo3, bg="white", width=420, height=300)
        contenedor_login.pack_propagate(False)
        contenedor_login.pack(padx=100, pady=100)

        lbl_usuario=Label(contenedor_login, text="Usuario", font=("Orlega One", 24), fg="Black", bg="white")
        lbl_usuario.pack()

        usuario_entry=Entry(contenedor_login, font=("Orlega One", 24), fg="Black", bg="white")
        usuario_entry.pack()

        lbl_contrasenia=Label(contenedor_login, text="Contraseña", font=("Orlega One", 24), fg="Black", bg="white")
        lbl_contrasenia.pack()

        contrasenia_entry=Entry(contenedor_login, font=("Orlega One", 24), fg="Black", bg="white")
        contrasenia_entry.pack()

        btn_ingresar=Button(contenedor_login, text="Ingresar", font=("Otomanopee One", 24), fg="#F1C045", bg="#A6171C", command=lambda: self.iniciar_sesion(ventana_login))
        btn_ingresar.pack(side=BOTTOM)

    def iniciar_sesion(self,ventana_login):   
        #usuario_texto = usuario_entry.get()
        #contrasenia_texto = contrasenia_entry.get()
        self.borrarPantalla(ventana_login)
        menu_principal.interfacesMenu(ventana_login)
    
    def borrarPantalla(self,ventana_login):
        for widget in ventana_login.winfo_children():
            widget.destroy()