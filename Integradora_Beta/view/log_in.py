from tkinter import *
from tkinter import messagebox
from view import menu_principal
from model import metodos_usuarios
from controller import funciones

class InterfacesLogin():
    def __init__(self,ventana_login):
        ventana_login.title("Login")
        ventana_login.geometry("1920x1080")
        ventana_login.state("zoomed")
        ventana_login.configure(bg="#8C0F12")  # rojo oscuro
        self.log_in(ventana_login)

    def crear_tarjeta_redondeada(self, parent, w, h, radius=40, bg="white"):
        """Frame con bordes redondeados usando Canvas."""
        canvas = Canvas(parent, width=w, height=h, bg=parent["bg"], highlightthickness=0)
        canvas.pack()

        # Dibujo borde redondeado (sombras sutiles)
        canvas.create_oval(5, 5, radius, radius, fill=bg, outline=bg)
        canvas.create_oval(w-radius, 5, w-5, radius, fill=bg, outline=bg)
        canvas.create_oval(5, h-radius, radius, h-5, fill=bg, outline=bg)
        canvas.create_oval(w-radius, h-radius, w-5, h-5, fill=bg, outline=bg)
        canvas.create_rectangle(radius/2, 5, w - radius/2, h - 5, fill=bg, outline=bg)
        canvas.create_rectangle(5, radius/2, w - 5, h - radius/2, fill=bg, outline=bg)

        # creación del frame encima del canvas
        frame = Frame(canvas, bg=bg)
        frame_window = canvas.create_window(w/2, h/2, window=frame)
        return frame

    def log_in(self,ventana_login):

        # Fondo general rojo
        fondo = Frame(ventana_login, bg="#8C0F12")
        fondo.pack(fill="both", expand=True)

        # Contenedor central con sombra
        contenedor = Frame(fondo, bg="#8C0F12")
        contenedor.place(relx=0.5, rely=0.5, anchor="center")

        # Tarjeta principal
        card = self.crear_tarjeta_redondeada(contenedor, 1100, 700, bg="#A6171C")

        # Título
        lbl_titulo = Label(
            card,
            text="El Barón Rojo",
            font=("Orelega One", 64),
            fg="#F1C045",
            bg="#A6171C"
        )
        lbl_titulo.pack(pady=20)

        # Tarjeta blanca interna
        card_login = self.crear_tarjeta_redondeada(card, 500, 500, bg="white")

        # Contenido login
        lbl_usuario = Label(card_login, text="Usuario", font=("Orlega One", 24), bg="white", fg="black")
        lbl_usuario.pack(pady=10)

        usuario_entry = Entry(card_login, font=("Orlega One", 22), relief="flat", bg="#F2F2F2")
        usuario_entry.pack(ipady=8, padx=40)

        lbl_contrasenia = Label(card_login, text="Contraseña", font=("Orlega One", 24), bg="white", fg="black")
        lbl_contrasenia.pack(pady=10)

        contrasenia_entry = Entry(card_login, font=("Orlega One", 22), relief="flat", bg="#F2F2F2", show="*")
        contrasenia_entry.pack(ipady=8, padx=40)
        # ==========================================================
        #   BOTÓN – MISMO MÉTODO Y MISMA LÓGICA
        # ==========================================================
        btn_ingresar = Button(
            card_login,
            text="Ingresar",
            font=("Otomanopee One", 24),
            fg="white",
            bg="#A6171C",
            relief="flat",
            activebackground="#D01E24",
            activeforeground="white",
            cursor="hand2",
            command=lambda: self.iniciar_sesion(
                ventana_login,
                usuario_entry.get(),
                contrasenia_entry.get()
            )
        )
        btn_ingresar.pack(pady=50, ipadx=30, ipady=10)

        # Hover
        btn_ingresar.bind("<Enter>", lambda e: btn_ingresar.config(bg="#C41E25"))
        btn_ingresar.bind("<Leave>", lambda e: btn_ingresar.config(bg="#A6171C"))

    # ==========================================================
    #   LÓGICA ORIGINAL NO MODIFICADA
    # ==========================================================
    def iniciar_sesion(self,ventana_login,usuario_entry,contrasenia_entry):

        usuario_texto = usuario_entry
        contrasenia_texto = contrasenia_entry

        if not usuario_texto and not contrasenia_texto:
            messagebox.showerror("Error", "Ingresa un usuario y contraseña.")
        else:
            if not usuario_texto:
                messagebox.showerror("Error", "Ingresa un usuario.")
                return
            if not contrasenia_texto:
                messagebox.showerror("Error", "Ingresa una contraseña.")
                return
            else:
                verification = metodos_usuarios.Usuarios_acciones.verificar_usuario(
                    usuario_texto, contrasenia_texto
                )

                if verification:
                    # verification es la tupla del usuario; el rol suele estar en la posición 6
                    try:
                        user_role = verification[6]
                    except Exception:
                        user_role = None

                    # guardar rol en controlador global
                    try:
                        funciones.set_current_user_role(user_role)
                    except Exception:
                        try:
                            funciones.current_user_role = user_role
                        except:
                            pass

                    self.borrarPantalla(ventana_login)
                    menu_principal.interfacesMenu(ventana_login)
                else:
                    return

    def borrarPantalla(self,ventana_login):
        for widget in ventana_login.winfo_children():
            widget.destroy()
