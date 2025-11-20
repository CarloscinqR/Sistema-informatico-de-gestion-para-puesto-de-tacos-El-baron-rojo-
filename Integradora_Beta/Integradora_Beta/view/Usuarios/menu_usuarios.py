from tkinter import *
from view.Usuarios.nuevo_usuario import nuevo_usuario_
from view.Usuarios.modificar_usuario import modificar_usuario_
from view.Usuarios.ver_usuarios import ver_usuarios_

class menuusuario():
    @staticmethod
    def menu_usuario_(ventana_menu):
        ventana_menu.destroy()
        menu_usuarioss=Tk()
        menu_usuarioss.title("Menu Usuarios")
        menu_usuarioss.geometry("1920x1080")
        menu_usuarioss.state("zoomed")

        fondo=Frame(menu_usuarioss, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        contenedor_botones=Frame(fondo2, bg="#A6171C", width=550, height=790)
        contenedor_botones.pack_propagate(False)
        contenedor_botones.pack(padx=300, pady=20)

        titulo=Label(contenedor_botones, text="Usuarios",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
        titulo.pack(padx=20, pady=20)

        nuevoUsuario=Button(contenedor_botones, text="Nuevo usuario", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: nuevo_usuario_(menu_usuarioss))
        nuevoUsuario.pack(padx=20, pady=10, fill="x")
        
        verUsuario=Button(contenedor_botones, text="Ver usuario", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: ver_usuarios_(menu_usuarioss))
        verUsuario.pack(padx=20, pady=10, fill="x")

        modificarUsuario=Button(contenedor_botones, text="Modificar usuario", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: modificar_usuario_(menu_usuarioss))
        modificarUsuario.pack(padx=20, pady=10, fill="x")
        
        def volver_al_menu_principal():
            from view.Menu_Principal.menu_principal import menuprincipal
            menu_usuarioss.destroy()
            menuprincipal.menu_principal()

        regresar=Button(contenedor_botones, text="Regresar", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=volver_al_menu_principal)
        regresar.pack(padx=20, pady=10, fill="x")

