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

        def on_borrar(iid, uid, uname):
            confirm = messagebox.askyesno("Confirmar eliminación", f"¿Desea eliminar el usuario?\nID: {uid}\nNombre: {uname}")
            if not confirm:
                return
            eliminado = metodos_usuarios.Usuarios_acciones.borrar(uid)
            if eliminado:
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente.")
                try:
                    b_ed, b_del = _row_buttons.pop(iid, (None, None))
                    if b_ed:
                        try:
                            b_ed.destroy()
                        except Exception:
                            pass
                    if b_del:
                        try:
                            b_del.destroy()
                        except Exception:
                            pass
                    try:
                        tabla.delete(iid)
                    except Exception:
                        pass
                    try:
                        reposition_buttons()
                    except Exception:
                        pass
                except Exception:
                    pass
            else:
                messagebox.showerror("Error", "No se pudo eliminar al usuario. Verifique la conexión o los datos.")
        
        def on_editar(iid, uid, uname, upassw,urol):
            # Abrir la vista de modificación pre-llenada con los datos seleccionados
            try:
                self.modificarUsuario(menu_usuarios, (uid,uname,upassw,urol))
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir la ventana de modificación: {e}")
        
        for i, user in enumerate(usuarios):
            # producto es una tupla (id_prduct, prduct_name, unit_price)
            tag = 'even' if i % 2 == 0 else 'odd'
            # Insertar fila en la tabla (sin funciones)
            if user[4]==None:
                fecha_el="-----"
            else:
                fecha_el=user[4]
            
            item_id = tabla.insert('', 'end', values=(i+1, user[1], user[3], fecha_el,user[6],''), tags=(tag,))

            # Crear botones visibles sobre la Treeview en la columna 'Acciones'
            # Los botones no tienen comando (no funcionales)
            btn_editar = Button(tabla, text='Editar', font=("Inter", 11), fg='#A6171C', bg='#F1F0EE', relief=RAISED, bd=1, padx=6, pady=2,command=lambda iid=item_id, uid=user[0], uname=user[1], upassw=user[2],urol=user[6]: on_editar(iid, uid, uname, upassw,urol))
            btn_borrar = Button(tabla, text='Borrar', font=("Inter", 11), fg='#FFFFFF', bg='#A6171C', relief=RAISED, bd=1, padx=6, pady=2,command=lambda iid=item_id, uid=user[0], uname=user[1]: on_borrar(iid, uid, uname))
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

        btn_agregarProducto=Button(contenedor_tabla, text="Agregar usuario", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: self.nuevoUsuario(menu_usuarios), width=22)
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
        
        nomb=StringVar()
        nombre_entry=Entry(fondo3, font=("Inter", 24), bg="white",textvariable=nomb)
        nombre_entry.pack(padx=20, pady=10)

        lbl_contrasenia=Label(fondo3, text="Contraseña", font=("Inter", 24), bg="white")
        lbl_contrasenia.pack(padx=20, pady=10)

        contr=StringVar()
        contrasenia_entry=Entry(fondo3, font=("Inter", 24), bg="white",textvariable=contr)
        contrasenia_entry.pack(padx=20, pady=10)

        lbl_contrasenia2=Label(fondo3, text="Confirmar contraseña", font=("Inter", 24), bg="white")
        lbl_contrasenia2.pack(padx=20, pady=10)
        contr2=StringVar()
        contrasenia2_entry=Entry(fondo3, font=("Inter", 24), bg="white",textvariable=contr2)
        contrasenia2_entry.pack(padx=20, pady=10)

        lbl_rol=Label(fondo3, text="Rol", font=("Inter", 24), bg="white")
        lbl_rol.pack(padx=20, pady=10)

        roles=["Administrador","Empleado"]
        rol_cbx=ttk.Combobox(fondo3,values=roles,font=("Inter", 24),state="readonly")
        rol_cbx.set(roles[0])
        rol_cbx.pack()
        

        btn_regresar=Button(fondo3, text="Regresar", font=("Inter", 24), bg="#F1C045", command=lambda: self.menu_usuario(nuevo_usuario))
        btn_regresar.pack(padx=20, pady=10)
        
        btn_agregar=Button(fondo3, text="Agregar", font=("Inter", 24), bg="#F1C045" ,command=lambda: funciones.Controladores.respuesta_sql("Agregar usuario",metodos_usuarios.Usuarios_acciones.agregar(nomb.get(),contr.get(),contr2.get(),rol_cbx.get())))
        btn_agregar.pack(padx=20, pady=10)

    def modificarUsuario(self,modificar_usuario,usuario=None):
        self.borrarPantalla(modificar_usuario)
        modificar_usuario.title("Modificar Usuario")
        modificar_usuario.geometry("1920x1080")
        modificar_usuario.state("zoomed")

        fondo=Frame(modificar_usuario, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        lbl_titulo=Label(fondo2, text="Modificar Usuario",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
        lbl_titulo.pack(padx=20, pady=20)

        fondo3=Frame(fondo2, bg="white", height=180)
        fondo3.pack(expand=True)

        uid = None
        initial_name = ""
        initial_passw=""
        initial_rol = ""
        if usuario:
            try:
                uid = usuario[0]
                initial_name = usuario[1]
                initial_rol = usuario[3]
            except Exception:
                uid = None

        lbl_nombre=Label(fondo3, text="Nombre del usuario", font=("Inter", 24), bg="white")
        lbl_nombre.pack(padx=20, pady=10)
        
        nombre_entry=Entry(fondo3, font=("Inter", 24), bg="white")
        nombre_entry.insert(0, initial_name)
        nombre_entry.pack(padx=20, pady=10)

        lbl_passw=Label(fondo3, text="Contraseña", font=("Inter", 24), bg="white")
        lbl_passw.pack(padx=20, pady=10)

        passw_entry=Entry(fondo3, font=("Inter", 24), bg="white")
        passw_entry.insert(0, initial_passw)
        passw_entry.pack(padx=20, pady=10)

        lbl_passw2=Label(fondo3, text="Confirmar contraseña", font=("Inter", 24), bg="white")
        lbl_passw2.pack(padx=20, pady=10)

        passw_entry2=Entry(fondo3, font=("Inter", 24), bg="white")
        passw_entry2.insert(0, initial_passw)
        passw_entry2.pack(padx=20, pady=10)


        lbl_rol=Label(fondo3, text="Rol", font=("Inter", 24), bg="white")
        lbl_rol.pack(padx=20, pady=10)
        roles=["Administrador","Empleado"]
        rol_cbx=ttk.Combobox(fondo3,values=roles,font=("Inter", 24),state="readonly")
        rol_cbx.set(initial_rol)
        rol_cbx.pack()



        def on_modificar():
            nonlocal uid
            nuevo_nombre = nombre_entry.get().strip()
            passw_text = passw_entry.get().strip()
            passw2_text=passw_entry2.get().strip()
            rol_text=rol_cbx.get().strip()
            if not nuevo_nombre:
                messagebox.showerror("Error", "El nombre no puede estar vacío.")
                return
            if uid is None:
                messagebox.showerror("Error", "Id del usuario desconocido. No se puede modificar.")
                return
            # Pedir contraseña antes de modificar

            modificado = metodos_usuarios.Usuarios_acciones.modificar_usuario(nuevo_nombre, passw_text,passw2_text,rol_text,uid)
            if modificado:
                messagebox.showinfo("Éxito", "Usuario modificado correctamente.")
                self.menu_usuario(modificar_usuario)
            else:
                messagebox.showerror("Error", "No se pudo modificar al usuario. Verifique la conexión o los datos.")

        btn_agregar=Button(fondo3, text="Modificar", font=("Inter", 24), bg="#F1C045", command=on_modificar)
        btn_agregar.pack(padx=20, pady=10)

        btn_regresar=Button(fondo3, text="Regresar", font=("Inter", 24), bg="#F1C045", command=lambda: self.menu_usuario(modificar_usuario))
        btn_regresar.pack(padx=20, pady=10)

    def regresar(self,menu_usuarios):
        menu_principal.interfacesMenu(menu_usuarios)


