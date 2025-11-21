from tkinter import *

class Login:
    def log_in():
        ventana_login=Tk()
        ventana_login.title("Iniciar sesión")
        ventana_login.geometry("1920x1080")
        ventana_login.state("zoomed")
    
        fondo=Frame(ventana_login, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)
    
        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)
    
        titulo=Label(fondo2, text="El Barón Rojo",font=("Orelega One", 64), fg="#F1C045", bg="#A6171C")
        titulo.pack(padx=20, pady=20, side=LEFT)
    
        fondo3=Frame(fondo2, bg="white", width=630, height=720)
        fondo3.pack_propagate(False)
        fondo3.pack(padx=82, pady=124)
    
        contenedor_login=Frame(fondo3, bg="white", width=420, height=300)
        contenedor_login.pack_propagate(False)
        contenedor_login.pack(padx=100, pady=100)
    
        usuario=Label(contenedor_login, text="Usuario", font=("Orlega One", 24), fg="Black", bg="white")
        usuario.pack()
    
        usuario_entry=Entry(contenedor_login, font=("Orlega One", 24), fg="Black", bg="white")
        usuario_entry.pack()
    
        contrasenia=Label(contenedor_login, text="Contraseña", font=("Orlega One", 24), fg="Black", bg="white")
        contrasenia.pack()
    
        contrasenia_entry=Entry(contenedor_login, font=("Orlega One", 24), fg="Black", bg="white")
        contrasenia_entry.pack()
    
        ingresar=Button(contenedor_login, text="Ingresar", font=("Otomanopee One", 24), fg="#F1C045", bg="#A6171C", command=lambda: iniciar_sesion())
        ingresar.pack(side=BOTTOM)
    
    
        def iniciar_sesion():   
            #usuario_texto = usuario_entry.get()
            #contrasenia_texto = contrasenia_entry.get()
            ventana_login.destroy()
            from Menu_Principal.menu_principal import menu_principal
            menu_principal() 
            
    
        ventana_login.mainloop()
