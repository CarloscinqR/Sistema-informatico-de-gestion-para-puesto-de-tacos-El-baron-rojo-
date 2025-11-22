from tkinter import *
from view import menu_principal
from tkinter import ttk
from model import metodos_usuarios

class interfacesUsuario():
    def __init__(self,menu_usuarios):
        menu_usuarios.title("Menu Usuarios")
        menu_usuarios.geometry("1920x1080")
        menu_usuarios.state("zoomed")
        self.menu_usuario(menu_usuarios)

    def borrarPantalla(self,ventana_login):
        for widget in ventana_login.winfo_children():
            widget.destroy()

    def menu_usuario(self,menu_usuarios):
        self.borrarPantalla(menu_usuarios)
        fondo=Frame(menu_usuarios, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        lbl_titulo=Label(fondo2, text="Usuarios",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
        lbl_titulo.pack(padx=20, pady=20)

        contenedor_tabla=Frame(fondo2, width=2000, height=790)
        contenedor_tabla.pack_propagate(False)
        contenedor_tabla.pack(side=LEFT, padx=40, pady=20)

        # --- Tabla de productos (Treeview) ---
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Treeview',
                        foreground='black',
                        rowheight=30,
                        font=('Inter', 14))
        style.configure('Treeview.Heading',
                        background='#A6171C',
                        foreground='#F1C045',
                        font=('Orelega One', 16))
        style.map('Treeview', background=[('selected', '#F1C045')], foreground=[('selected', 'black')])

        # Agrego columna 'Acciones' para mostrar opciones sutiles por fila
        columns = ('Id_usuario', 'Usuario','Fecha_creacion','Fecha_eliminacion', 'Rol' ,'Acciones')
        tabla = ttk.Treeview(contenedor_tabla, columns=columns, show='headings', selectmode='browse')
        tabla.heading('Id_usuario', text='Id_usuario')
        tabla.heading('Usuario', text='Usuario')
        tabla.heading('Fecha_creacion', text='Fecha de creacion')
        tabla.heading('Fecha_eliminacion', text='Fecha de eliminacion')
        tabla.heading('Rol', text='Rol')
        tabla.heading('Acciones', text='Acciones')
        tabla.column('Id_usuario', width=120, anchor=CENTER)
        tabla.column('Usuario', width=200, anchor=W)
        tabla.column('Fecha_creacion', width=160, anchor=E)
        tabla.column('Fecha_eliminacion', width=180, anchor=CENTER)
        tabla.column('Rol', width=180, anchor=CENTER)
        tabla.column('Acciones', width=180, anchor=CENTER)

        vsb = ttk.Scrollbar(contenedor_tabla, orient="vertical")
        # comando personalizado para reposicionar botones al hacer scroll
        def _vsb_command(*args):
            tabla.yview(*args)
            try:
                reposition_buttons()
            except Exception:
                pass

        vsb.config(command=_vsb_command)
        tabla.configure(yscrollcommand=vsb.set)
        tabla.pack(fill=BOTH, expand=True, padx=20, pady=10)
        vsb.pack(side=RIGHT, fill=Y, pady=10, padx=(0,20))

        # Estilo de filas alternadas
        tabla.tag_configure('odd', background='#FFFFFF')
        tabla.tag_configure('even', background='#F6F0E8')

        # Cargar datos desde la base de datos usando el modelo
        usuarios = metodos_usuarios.Usuarios_acciones.obtener_usuarios()
        # contenedor para guardar referencias a botones por fila
        _row_buttons = {}

        for i, user in enumerate(usuarios):
            # producto es una tupla (id_prduct, prduct_name, unit_price)
            tag = 'even' if i % 2 == 0 else 'odd'
            # Insertar fila en la tabla (sin funciones)
            item_id = tabla.insert('', 'end', values=(user[0], user[1], user[3], user[4],user[6],''), tags=(tag,))

            # Crear botones visibles sobre la Treeview en la columna 'Acciones'
            # Los botones no tienen comando (no funcionales)
            btn_editar = Button(tabla, text='Editar', font=("Inter", 11), fg='#A6171C', bg='#F1F0EE', relief=RAISED, bd=1, padx=6, pady=2)
            btn_borrar = Button(tabla, text='Borrar', font=("Inter", 11), fg='#FFFFFF', bg='#A6171C', relief=RAISED, bd=1, padx=6, pady=2)
            _row_buttons[item_id] = (btn_editar, btn_borrar)

        # Forzar dibujo y posicionar los botones sobre cada celda 'Acciones'
        menu_usuarios.update_idletasks()

        def reposition_buttons():
            for iid, (b_ed, b_del) in _row_buttons.items():
                try:
                    bbox = tabla.bbox(iid, column='Acciones')
                except Exception:
                    bbox = None
                if not bbox:
                    # ocultar si no está visible
                    b_ed.place_forget()
                    b_del.place_forget()
                    continue
                x, y, width, height = bbox
                # ajustar posiciones relativas dentro de la celda
                btn_width = int(width * 0.45)
                gap = 6
                # colocar botones dentro del árbol usando coordenadas relativas al Treeview
                b_ed.place(x=x + 4, y=y + 2, width=btn_width - gap, height=height - 4)
                b_del.place(x=x + 4 + btn_width, y=y + 2, width=btn_width - gap, height=height - 4)

        # Ligar reposition a eventos que mueven la vista
        tabla.bind('<Configure>', lambda e: reposition_buttons())
        tabla.bind('<ButtonRelease-1>', lambda e: reposition_buttons())
        tabla.bind('<Motion>', lambda e: None)
        # rueda del ratón en Windows
        tabla.bind_all('<MouseWheel>', lambda e: (reposition_buttons(), None))

        # llamada inicial
        try:
            reposition_buttons()
        except Exception:
            pass

        btn_agregarProducto=Button(contenedor_tabla, text="Agregar producto", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: self.regresar(menu_usuarios), width=22)
        btn_agregarProducto.pack(padx=20, pady=10, fill="x", side=LEFT)

        btn_regresar=Button(contenedor_tabla, text="Regresar", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: self.regresar(menu_usuarios), width=22)
        btn_regresar.pack(padx=20, pady=10, fill="x", side=RIGHT)

    def nuevoUsuario(self,nuevo_usuario):
        self.borrarPantalla(nuevo_usuario)
        nuevo_usuario.title("Nuevo usuario")
        nuevo_usuario.geometry("1920x1080")
        nuevo_usuario.state("zoomed")

        fondo=Frame(nuevo_usuario, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        lbl_titulo=Label(fondo2, text="Nuevo usuario",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
        lbl_titulo.pack(padx=20, pady=20)

        fondo3=Frame(fondo2, bg="white", height=180)
        fondo3.pack(expand=True)

        lbl_nombre=Label(fondo3, text="Nombre", font=("Inter", 24), bg="white")
        lbl_nombre.pack(padx=20, pady=10)
        
        nombre_entry=Entry(fondo3, font=("Inter", 24), bg="white")
        nombre_entry.pack(padx=20, pady=10)

        lbl_contrasenia=Label(fondo3, text="contraseña", font=("Inter", 24), bg="white")
        lbl_contrasenia.pack(padx=20, pady=10)

        contrasenia_entry=Entry(fondo3, font=("Inter", 24), bg="white")
        contrasenia_entry.pack(padx=20, pady=10)

        btn_regresar=Button(fondo3, text="Regresar", font=("Inter", 24), bg="#F1C045", command=lambda: self.menu_usuario(nuevo_usuario))
        btn_regresar.pack(padx=20, pady=10)
        
        btn_agregar=Button(fondo3, text="Agregar", font=("Inter", 24), bg="#F1C045")
        btn_agregar.pack(padx=20, pady=10)

    def modificarUsuario(self,modificar_usuario):
        self.borrarPantalla(modificar_usuario)
        modificar_usuario.title("Modificar usuario")
        modificar_usuario.geometry("1920x1080")
        modificar_usuario.state("zoomed")

        fondo=Frame(modificar_usuario, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        lbl_titulo=Label(fondo2, text="Modificar usuarios",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
        lbl_titulo.pack(padx=20, pady=20)

        fondo3=Frame(fondo2, bg="white", height=180)
        fondo3.pack(expand=True)

        def volver_a_menu():
            pass

        lbl_usuario_modificado=Label(fondo3, text="Selecciona el usuario a modificar", font=("Inter", 24), bg="white")
        lbl_usuario_modificado.pack(padx=20, pady=10)

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
            print("usuarios seleccionado:", usuario_modificado_combo.get())
        
        usuario_modificado_combo.bind('<<ComboboxSelected>>', on_select)


        lbl_nombre=Label(fondo3, text="Nuevo nombre", font=("Inter", 24), bg="white")
        lbl_nombre.pack(padx=20, pady=10)
        
        nombre_entry=Entry(fondo3, font=("Inter", 24), bg="white")
        nombre_entry.pack(padx=20, pady=10)

        lbl_contrasenia=Label(fondo3, text="Nueva contraseña", font=("Inter", 24), bg="white")
        lbl_contrasenia.pack(padx=20, pady=10)

        contrasenia_entry=Entry(fondo3, font=("Inter", 24), bg="white")
        contrasenia_entry.pack(padx=20, pady=10)

        btn_regresar=Button(fondo3, text="Regresar", font=("Inter", 24), bg="#F1C045", command=lambda: self.menu_usuario(modificar_usuario))
        btn_regresar.pack(padx=20, pady=10)
        
        btn_agregar=Button(fondo3, text="Agregar", font=("Inter", 24), bg="#F1C045")
        btn_agregar.pack(padx=20, pady=10)

    def regresar(self,menu_usuarios):
        menu_principal.interfacesMenu(menu_usuarios)


