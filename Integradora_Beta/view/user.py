from tkinter import *
from view import menu_principal
from tkinter import ttk,messagebox,simpledialog
from model import metodos_usuarios
from controller import funciones

class interfacesUsuario():
    def __init__(self,menu_usuarios):
        menu_usuarios.title("Menu Usuarios")
        menu_usuarios.geometry("1920x1080")
        menu_usuarios.state("zoomed")
        self.menu_usuario(menu_usuarios)

    def borrarPantalla(self,ventana_login):
        for widget in ventana_login.winfo_children():
            widget.destroy()

    def menu_usuario(self, menu_usuarios):
        self.borrarPantalla(menu_usuarios)

        # -------------------------------------------
        # Fondo general
        # -------------------------------------------
        fondo = Frame(menu_usuarios, bg="#F4F4F4")
        fondo.pack(fill="both", expand=True)

        # -------------------------------------------
        # Contenedor central 85% del tamaño de la ventana
        # -------------------------------------------
        fondo2 = Frame(
            fondo,
            bg="#A6171C",
            highlightbackground="#610E11",
            highlightthickness=4
        )
        fondo2.place(relx=0.5, rely=0.5, anchor="center",
                    relwidth=0.85, relheight=0.85)

        # -------------------------------------------
        # TÍTULO
        # -------------------------------------------
        titulo_frame = Frame(fondo2, bg="#A6171C")
        titulo_frame.place(relx=0.5, y=50, anchor="center")

        lbl_titulo = Label(
            titulo_frame,
            text="Usuarios",
            font=("Orelega One", 52),
            fg="white",
            bg="#A6171C"
        )
        lbl_titulo.pack()

        # -------------------------------------------
        # TARJETA DE LA TABLA
        # -------------------------------------------
        tabla_card = Frame(
            fondo2,
            bg="white",
            highlightbackground="#C0C0C0",
            highlightthickness=2
        )
        tabla_card.place(relx=0.5, rely=0.52, anchor="center",
                        relwidth=0.90, relheight=0.70)

        # -------------------------------------------
        # Contenedor interno tabla
        # -------------------------------------------
        contenedor_tabla = Frame(tabla_card, bg="white")
        contenedor_tabla.pack(fill="both", expand=True, padx=20, pady=20)

        # -------------------------------------------
        # Treeview estilo
        # -------------------------------------------
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview",
            background="white",
            foreground="black",
            rowheight=32,
            font=('Inter', 14),
            fieldbackground="white"
        )

        style.configure(
            "Treeview.Heading",
            background="#A6171C",
            foreground="#FFFFFF",
            font=('Orelega One', 15),
            borderwidth=0
        )
        style.map("Treeview", background=[('selected', '#FF5E5E')], foreground=[('selected', 'black')])

        # -------------------------------------------
        # ENCABEZADO
        # -------------------------------------------
        columns = ('Id_usuario', 'Usuario', 'Fecha_cre', 'Fecha_el', 'Rol', 'Acciones')

        header_frame = Frame(contenedor_tabla, bg="#A6171C")
        header_frame.pack(fill='x')

        header_cfg = dict(bg="#A6171C", fg="white", font=('Orelega One', 15))

        Label(header_frame, text='Id_usuario', anchor='center', **header_cfg).grid(row=0, column=0, sticky='we')
        Label(header_frame, text='Usuario', anchor='w', **header_cfg).grid(row=0, column=1, sticky='we')
        Label(header_frame, text='Fecha_creación', anchor='center', **header_cfg).grid(row=0, column=2, sticky='we')
        Label(header_frame, text='Fecha_eliminación', anchor='center', **header_cfg).grid(row=0, column=3, sticky='we')
        Label(header_frame, text='Rol', anchor='center', **header_cfg).grid(row=0, column=4, sticky='we')
        Label(header_frame, text='Acciones', anchor='center', **header_cfg).grid(row=0, column=5, sticky='we')

        header_frame.columnconfigure(0, weight=1)   # ID
        header_frame.columnconfigure(1, weight=3)   # Usuario
        header_frame.columnconfigure(2, weight=2)   # Fecha cre
        header_frame.columnconfigure(3, weight=2)   # Fecha elim
        header_frame.columnconfigure(4, weight=2)   # Rol
        header_frame.columnconfigure(5, weight=3)   # Acciones (más ancho)

        # -------------------------------------------
        # TABLA TREEVIEW
        # -------------------------------------------
        tabla = ttk.Treeview(contenedor_tabla, columns=columns, show='', selectmode='browse')
        total_width = tabla_card.winfo_width()
        tabla.column('Id_usuario',     width=int(total_width * 0.07),  anchor=CENTER)
        tabla.column('Usuario',        width=int(total_width * 0.21),  anchor=W)
        tabla.column('Fecha_cre',      width=int(total_width * 0.14),  anchor=CENTER)
        tabla.column('Fecha_el',       width=int(total_width * 0.14),  anchor=CENTER)
        tabla.column('Rol',            width=int(total_width * 0.14),  anchor=CENTER)
        tabla.column('Acciones',       width=int(total_width * 0.23),  anchor=CENTER) 

        vsb = ttk.Scrollbar(contenedor_tabla, orient="vertical")

        def _vsb_command(*args):
            tabla.yview(*args)
            try:
                reposition_buttons()
            except:
                pass

        vsb.config(command=_vsb_command)
        tabla.configure(yscrollcommand=vsb.set)

        tabla.pack(fill=BOTH, expand=True, side=LEFT)
        vsb.pack(side=RIGHT, fill=Y)

        tabla.tag_configure('odd', background='#FFFFFF')
        tabla.tag_configure('even', background='#F8F8F8')

        usuarios = metodos_usuarios.Usuarios_acciones.obtener_usuarios()
        _row_buttons = {}

        # -------------------------------------------
        # Función botones borrar / editar
        # -------------------------------------------
        def on_borrar(iid, uid, uname):
            confirm = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Desea eliminar el usuario?\nID: {uid}\nNombre: {uname}"
            )
            if not confirm:
                return

            eliminado = metodos_usuarios.Usuarios_acciones.borrar(uid)

            if eliminado:
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
                try:
                    b_ed, b_del = _row_buttons.pop(iid, (None, None))
                    if b_ed: b_ed.destroy()
                    if b_del: b_del.destroy()
                    tabla.delete(iid)
                    reposition_buttons()
                except:
                    pass
            else:
                messagebox.showerror("Error", "No se pudo eliminar al usuario.")

        def on_editar(iid, uid, uname, upassw, urol):
            try:
                self.modificarUsuario(menu_usuarios, (uid, uname, upassw, urol))
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir la ventana: {e}")

        # -------------------------------------------
        # Insertar filas con botones
        # -------------------------------------------
        for i, user in enumerate(usuarios):
            fecha_el = user[4] if user[4] else "-----"
            tag = 'even' if i % 2 == 0 else 'odd'

            item_id = tabla.insert(
                '', 'end',
                values=(i+1, user[1], user[3], fecha_el, user[6], ''),
                tags=(tag,)
            )

            btn_editar = Button(
                tabla,
                text='Editar',
                font=("Inter", 9),
                bg="white",
                fg="#A6171C",
                relief="solid",
                bd=1,
                highlightthickness=0,
                command=lambda iid=item_id, u=user: on_editar(iid, u[0], u[1], u[2], u[6])
            )

            btn_borrar = Button(
                tabla,
                text='Borrar',
                font=("Inter", 9),
                bg="#A6171C",
                fg="white",
                relief="solid",
                bd=1,
                highlightthickness=0,
                command=lambda iid=item_id, u=user: on_borrar(iid, u[0], u[1])
            )

            _row_buttons[item_id] = (btn_editar, btn_borrar)

        menu_usuarios.update_idletasks()

        # -------------------------------------------
        # Reposicionar botones dentro del Treeview
        # -------------------------------------------
        def reposition_buttons():
            for iid, (b_ed, b_del) in _row_buttons.items():
                try:
                    bbox = tabla.bbox(iid, column='Acciones')
                except:
                    bbox = None

                if not bbox:
                    b_ed.place_forget()
                    b_del.place_forget()
                    continue

                x, y, width, height = bbox
                btn_width = int((width - 16) / 2)  # Más espacio lateral
                b_ed.place(x=x+2, y=y+4, width=btn_width, height=height-8)
                b_del.place(x=x+btn_width+6, y=y+4, width=btn_width, height=height-8)

        tabla.bind('<Configure>', lambda e: reposition_buttons())
        tabla.bind('<ButtonRelease-1>', lambda e: reposition_buttons())
        tabla.bind_all('<MouseWheel>', lambda e: reposition_buttons())

        try:
            reposition_buttons()
        except:
            pass

        # -------------------------------------------
        # BOTONES INFERIORES (PEQUEÑOS)
        # -------------------------------------------
        botones_frame = Frame(fondo2, bg="#A6171C")
        botones_frame.place(relx=0.5, rely=0.92, anchor="center")

        btn_agregar = Button(
            botones_frame,
            text="Agregar usuario",
            font=("Inter", 16),
            fg="white",
            bg="#A6171C",
            relief="flat",
            padx=24,
            pady=6,
            width=18,
            command=lambda: self.nuevoUsuario(menu_usuarios)
        )
        btn_agregar.grid(row=0, column=0, padx=25)

        btn_regresar = Button(
            botones_frame,
            text="Regresar",
            font=("Inter", 16),
            fg="#A6171C",
            bg="white",
            relief="flat",
            padx=24,
            pady=6,
            width=18,
            command=lambda: self.regresar(menu_usuarios)
        )
        btn_regresar.grid(row=0, column=1, padx=25)


    def nuevoUsuario(self, nuevo_usuario):
        self.borrarPantalla(nuevo_usuario)
        nuevo_usuario.title("Nuevo usuario")
        nuevo_usuario.geometry("1920x1080")
        nuevo_usuario.state("zoomed")

        # Fondo general rojo
        fondo = Frame(nuevo_usuario, bg="#A6171C")
        fondo.pack(fill="both", expand=True)

        # Contenedor centrado blanco con borde decorativo
        container = Frame(
            fondo,
            bg="white",
            width=750,
            height=750,
            highlightbackground="#F1C045",
            highlightthickness=4
        )
        container.place(relx=0.5, rely=0.5, anchor="center")

        # Título
        lbl_titulo = Label(
            container,
            text="Nuevo usuario",
            font=("Orelega One", 42),
            fg="#A6171C",
            bg="white"
        )
        lbl_titulo.pack(pady=(40, 10))

        # Marco del formulario
        form_frame = Frame(container, bg="white")
        form_frame.pack(pady=20)

        # --- Nombre ---
        Label(form_frame, text="Nombre", font=("Inter", 20), bg="white").pack(anchor="w", padx=40)
        nomb = StringVar()
        nombre_entry = Entry(form_frame, font=("Inter", 20), bg="#F7F7F7", relief="flat",textvariable=nomb)
        nombre_entry.pack(padx=40, pady=(0, 15), ipady=5, fill="x")

        # --- Contraseña ---
        Label(form_frame, text="Contraseña", font=("Inter", 20), bg="white").pack(anchor="w", padx=40)
        contr = StringVar()
        contrasenia_entry = Entry(form_frame, font=("Inter", 20), bg="#F7F7F7", relief="flat", show="*")
        contrasenia_entry.pack(padx=40, pady=(0, 15), ipady=5, fill="x")

        # --- Confirmar Contraseña ---
        Label(form_frame, text="Confirmar contraseña", font=("Inter", 20), bg="white").pack(anchor="w", padx=40)
        contr2 = StringVar()
        contrasenia2_entry = Entry(form_frame, font=("Inter", 20), bg="#F7F7F7", relief="flat", show="*")
        contrasenia2_entry.pack(padx=40, pady=(0, 15), ipady=5, fill="x")

        # --- Rol ---
        Label(form_frame, text="Rol", font=("Inter", 20), bg="white").pack(anchor="w", padx=40)
        roles = ["Administrador", "Empleado"]
        rol_cbx = ttk.Combobox(
            form_frame,
            values=roles,
            font=("Inter", 20),
            state="readonly"
        )
        rol_cbx.set(roles[0])
        rol_cbx.pack(padx=40, pady=(0, 20), fill="x")

        # Marco de botones
        botones_frame = Frame(container, bg="white")
        botones_frame.pack(pady=25)

        # Botón Regresar
        btn_regresar = Button(
            botones_frame,
            text="Regresar",
            font=("Inter", 20),
            bg="#FFFFFF",
            fg="black",
            activebackground="#ABABAB",
            relief="flat",
            width=12,
            command=lambda: self.menu_usuario(nuevo_usuario)
        )
        btn_regresar.grid(row=0, column=0, padx=20)

        # Botón Agregar
        btn_agregar = Button(
            botones_frame,
            text="Agregar",
            font=("Inter", 20),
            bg="#A6171C",
            fg="white",
            activebackground="#8F1318",
            relief="flat",
            width=12,
            command=lambda: funciones.Controladores.respuesta_sql(
                "Agregar usuario", metodos_usuarios.Usuarios_acciones.agregar(nomb.get(), contr.get(), contr2.get(), rol_cbx.get().strip())
            )
        )
        btn_agregar.grid(row=0, column=1, padx=20)



    def modificarUsuario(self, modificar_usuario, usuario=None):
        self.borrarPantalla(modificar_usuario)
        modificar_usuario.title("Modificar Usuario")
        modificar_usuario.geometry("1920x1080")
        modificar_usuario.state("zoomed")

        # ================================
        # 🔴 Fondo rojo global
        # ================================
        fondo = Frame(modificar_usuario, bg="#A6171C")
        fondo.pack(fill="both", expand=True)

        # ================================
        # 📦 Tarjeta blanca centrada
        # ================================
        container = Frame(
            fondo,
            bg="white",
            width=750,
            height=780,
            highlightbackground="#F1C045",
            highlightthickness=4
        )
        container.place(relx=0.5, rely=0.5, anchor="center")

        # ================================
        # 🔤 Título
        # ================================
        lbl_titulo = Label(
            container,
            text="Modificar Usuario",
            font=("Orelega One", 42),
            fg="#A6171C",
            bg="white"
        )
        lbl_titulo.pack(pady=(40, 15))

        # ================================
        # 📋 Obtener datos iniciales
        # ================================
        uid = None
        initial_name = ""
        initial_passw = ""
        initial_rol = ""

        if usuario:
            try:
                uid = usuario[0]
                initial_name = usuario[1]
                initial_rol = usuario[3]
            except:
                uid = None

        # ================================
        # 🧾 Frame del formulario
        # ================================
        form_frame = Frame(container, bg="white")
        form_frame.pack(pady=10)

        # --- Nombre ---
        Label(form_frame, text="Nombre", font=("Inter", 20), bg="white").pack(anchor="w", padx=40)
        nombre_entry = Entry(form_frame, font=("Inter", 20), bg="#F7F7F7", relief="flat")
        nombre_entry.insert(0, initial_name)
        nombre_entry.pack(padx=40, pady=(0, 15), ipady=5, fill="x")

        # --- Contraseña ---
        Label(form_frame, text="Contraseña", font=("Inter", 20), bg="white").pack(anchor="w", padx=40)
        passw_entry = Entry(form_frame, font=("Inter", 20), bg="#F7F7F7", relief="flat", show="*")
        passw_entry.insert(0, initial_passw)
        passw_entry.pack(padx=40, pady=(0, 15), ipady=5, fill="x")

        # --- Confirmar Contraseña ---
        Label(form_frame, text="Confirmar contraseña", font=("Inter", 20), bg="white").pack(anchor="w", padx=40)
        passw_entry2 = Entry(form_frame, font=("Inter", 20), bg="#F7F7F7", relief="flat", show="*")
        passw_entry2.insert(0, initial_passw)
        passw_entry2.pack(padx=40, pady=(0, 15), ipady=5, fill="x")

        # --- Rol ---
        Label(form_frame, text="Rol", font=("Inter", 20), bg="white").pack(anchor="w", padx=40)
        roles = ["Administrador", "Empleado"]
        rol_cbx = ttk.Combobox(
            form_frame,
            values=roles,
            font=("Inter", 20),
            state="readonly"
        )
        rol_cbx.set(initial_rol)
        rol_cbx.pack(padx=40, pady=(0, 25), fill="x")

        # ================================
        # 🔧 Función para modificar
        # ================================
        def on_modificar():
            nonlocal uid
            nuevo_nombre = nombre_entry.get().strip()
            passw_text = passw_entry.get().strip()
            passw2_text = passw_entry2.get().strip()
            rol_text = rol_cbx.get().strip()

            if not nuevo_nombre:
                messagebox.showerror("Error", "El nombre no puede estar vacío.")
                return
            if uid is None:
                messagebox.showerror("Error", "Id del usuario desconocido. No se puede modificar.")
                return

            modificado = metodos_usuarios.Usuarios_acciones.modificar_usuario(
                nuevo_nombre, passw_text, passw2_text, rol_text, uid
            )

            if modificado:
                messagebox.showinfo("Éxito", "Usuario modificado correctamente.")
                self.menu_usuario(modificar_usuario)
            else:
                messagebox.showerror("Error", "No se pudo modificar al usuario.")

        # ================================
        # 🎛 Botones Inferiores
        # ================================
        botones_frame = Frame(container, bg="white")
        botones_frame.pack(pady=25)

        # Botón Modificar
        btn_modificar = Button(
            botones_frame,
            text="Modificar",
            font=("Inter", 20),
            bg="#A6171C",
            fg="white",
            activebackground="#8F1318",
            relief="flat",
            width=12,
            command=on_modificar
        )
        btn_modificar.grid(row=0, column=1, padx=20)

        # Botón Regresar
        btn_regresar = Button(
            botones_frame,
            text="Regresar",
            font=("Inter", 20),
            bg="#FFFFFF",
            fg="black",
            activebackground="#ABABAB",
            relief="flat",
            width=12,
            command=lambda: self.menu_usuario(modificar_usuario)
        )
        btn_regresar.grid(row=0, column=0, padx=20)


    def regresar(self,menu_usuarios):
        menu_principal.interfacesMenu(menu_usuarios)


