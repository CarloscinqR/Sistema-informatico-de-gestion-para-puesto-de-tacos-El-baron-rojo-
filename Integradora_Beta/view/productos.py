from tkinter import *
from view import menu_principal
from tkinter import ttk
from model import metodos_productos
from tkinter import messagebox, simpledialog

class interfacesProducto():
    def __init__(self,menu_productos):
        menu_productos.title("Menu productos")
        menu_productos.geometry("1920x1080")
        menu_productos.state("zoomed")
        self.menu_producto(menu_productos)

    def borrarPantalla(self,ventana_login):
        for widget in ventana_login.winfo_children():
            widget.destroy()

    def menu_producto(self,menu_productos):
        self.borrarPantalla(menu_productos)
        fondo=Frame(menu_productos, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        lbl_titulo=Label(fondo2, text="Productos",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
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
        columns = ('Id_producto', 'Nombre_producto', 'Precio_unitario', 'Acciones')

        # Encabezado personalizado: uso Labels en lugar de los headings del Treeview
        header_frame = Frame(contenedor_tabla, bg='#A6171C')
        header_frame.pack(fill='x', padx=20, pady=(10, 0))
        # Mantener proporciones similares a las columnas del Treeview
        header_frame.columnconfigure(0, weight=120)
        header_frame.columnconfigure(1, weight=480)
        header_frame.columnconfigure(2, weight=160)
        header_frame.columnconfigure(3, weight=180)

        lbl_h_id = Label(header_frame, text='Id_producto', bg='#A6171C', fg='#F1C045', font=('Orelega One', 16))
        lbl_h_nombre = Label(header_frame, text='Nombre_producto', bg='#A6171C', fg='#F1C045', font=('Orelega One', 16))
        lbl_h_precio = Label(header_frame, text='Precio_unitario', bg='#A6171C', fg='#F1C045', font=('Orelega One', 16))
        lbl_h_acciones = Label(header_frame, text='Acciones', bg='#A6171C', fg='#F1C045', font=('Orelega One', 16))

        lbl_h_id.grid(row=0, column=0, sticky='we', padx=(4,2))
        lbl_h_nombre.grid(row=0, column=1, sticky='we', padx=2)
        lbl_h_precio.grid(row=0, column=2, sticky='we', padx=2)
        lbl_h_acciones.grid(row=0, column=3, sticky='we', padx=(2,4))

        # Crear Treeview sin mostrar los headings nativos (los reemplazamos por Labels)
        # Nota: ocultamos los headings nativos con `show=''` porque queremos
        # controlar la apariencia mediante Labels personalizados (mismo color,
        # fuente y estilo). Esto evita que el encabezado parezca un botón
        # interactivo si no deseamos esa conducta. Si más adelante se desea
        # ordenamiento o interacción, se pueden reactivar los headings o
        # añadir bindings a los Labels para replicar esa funcionalidad.
        tabla = ttk.Treeview(contenedor_tabla, columns=columns, show='', selectmode='browse')
        tabla.column('Id_producto', width=120, anchor=CENTER)
        tabla.column('Nombre_producto', width=480, anchor=W)
        tabla.column('Precio_unitario', width=160, anchor=E)
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
        productos = metodos_productos.Productos_acciones.obtener_productos()
        # contenedor para guardar referencias a botones por fila
        _row_buttons = {}

        def on_borrar(iid, pid, pname):
            confirm = messagebox.askyesno("Confirmar eliminación", f"¿Desea eliminar el producto?\nID: {pid}\nNombre: {pname}")
            if not confirm:
                return

            pwd = simpledialog.askstring("Autorización", "Ingrese la contraseña para eliminar:", show='*', parent=menu_productos)
            if pwd is None:
                return
            if pwd != '1234':
                messagebox.showerror("Error", "Contraseña incorrecta.")
                return

            eliminado = metodos_productos.Productos_acciones.borrar(pid)
            if eliminado:
                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
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
                messagebox.showerror("Error", "No se pudo eliminar el producto. Verifique la conexión o los datos.")

        # Handler para editar un producto: abre la interfaz de modificarProducto
        def on_editar(iid, pid, pname, pprice):
            # Abrir la vista de modificación pre-llenada con los datos seleccionados
            try:
                self.modificarProducto(menu_productos, (pid, pname, pprice))
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir la ventana de modificación: {e}")

        for i, producto in enumerate(productos):
            precio = producto[2]
            try:
                precio_text = f"{float(precio):.2f} MXN"
            except Exception:
                precio_text = str(precio)
            tag = 'even' if i % 2 == 0 else 'odd'
            # Insertar fila en la tabla (sin funciones)
            item_id = tabla.insert('', 'end', values=(producto[0], producto[1], precio_text, ''), tags=(tag,))

            btn_editar = Button(tabla, text='Editar', font=("Inter", 11), fg='#A6171C', bg='#F1F0EE', relief=RAISED, bd=1, padx=6, pady=2)
            btn_borrar = Button(tabla, text='Borrar', font=("Inter", 11), fg='#FFFFFF', bg='#A6171C', relief=RAISED, bd=1, padx=6, pady=2)
            btn_editar.config(command=lambda iid=item_id, pid=producto[0], pname=producto[1], pprice=producto[2]: on_editar(iid, pid, pname, pprice))
            btn_borrar.config(command=lambda iid=item_id, pid=producto[0], pname=producto[1]: on_borrar(iid, pid, pname))
            _row_buttons[item_id] = (btn_editar, btn_borrar)

        # Forzar dibujo y posicionar los botones sobre cada celda 'Acciones'
        menu_productos.update_idletasks()

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

        # Botón 'Agregar producto'
        btn_agregarProducto=Button(contenedor_tabla, text="Agregar producto", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: self.nuevoProducto(menu_productos), width=22)
        btn_agregarProducto.pack(padx=20, pady=10, fill="x", side=LEFT)

        btn_regresar=Button(contenedor_tabla, text="Regresar", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: self.regresar(menu_productos), width=22)
        btn_regresar.pack(padx=20, pady=10, fill="x", side=RIGHT)

    def nuevoProducto(self,nuevo_producto):
        self.borrarPantalla(nuevo_producto)
        nuevo_producto.title("Nnuevo producto")
        nuevo_producto.geometry("1920x1080")
        nuevo_producto.state("zoomed")

        fondo=Frame(nuevo_producto, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        lbl_titulo=Label(fondo2, text="Nuevo producto",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
        lbl_titulo.pack(padx=20, pady=20)

        fondo3=Frame(fondo2, bg="white", height=180)
        fondo3.pack(expand=True)

        lbl_nombre=Label(fondo3, text="Nombre del producto", font=("Inter", 24), bg="white")
        lbl_nombre.pack(padx=20, pady=10)
        
        nombre_entry=Entry(fondo3, font=("Inter", 24), bg="white")
        nombre_entry.pack(padx=20, pady=10)

        lbl_precio=Label(fondo3, text="Precio unitario", font=("Inter", 24), bg="white")
        lbl_precio.pack(padx=20, pady=10)

        precio_entry=Entry(fondo3, font=("Inter", 24), bg="white")
        precio_entry.pack(padx=20, pady=10)

        btn_regresar=Button(fondo3, text="Regresar", font=("Inter", 24), bg="#F1C045", command=lambda: self.menu_producto(nuevo_producto))
        btn_regresar.pack(padx=20, pady=10)
        
        def on_agregar():
            nombre = nombre_entry.get().strip()
            precio_text = precio_entry.get().strip()

            if not nombre:
                messagebox.showerror("Error", "El nombre del producto no puede estar vacío.")
                return

            try:
                precio = float(precio_text)
            except Exception:
                messagebox.showerror("Error", "Precio inválido. Introduce un número válido.")
                return

            agregado = metodos_productos.Productos_acciones.agregar(nombre, precio)
            if agregado:
                messagebox.showinfo("Éxito", "Producto agregado exitosamente.")
                self.menu_producto(nuevo_producto)
            else:
                messagebox.showerror("Error", "No se pudo agregar el producto. Revisa la conexión o los datos.")

        btn_agregar=Button(fondo3, text="Agregar", font=("Inter", 24), bg="#F1C045", command=on_agregar)
        btn_agregar.pack(padx=20, pady=10)

    def modificarProducto(self, modificar_producto, producto=None):
 
        self.borrarPantalla(modificar_producto)
        modificar_producto.title("Modificar producto")
        modificar_producto.geometry("1920x1080")
        modificar_producto.state("zoomed")

        fondo=Frame(modificar_producto, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        lbl_titulo=Label(fondo2, text="Modificar producto",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
        lbl_titulo.pack(padx=20, pady=20)

        fondo3=Frame(fondo2, bg="white", height=180)
        fondo3.pack(expand=True)

        pid = None
        initial_name = ""
        initial_price = ""
        if producto:
            try:
                pid = producto[0]
                initial_name = producto[1]
                initial_price = str(producto[2])
            except Exception:
                pid = None

        lbl_nombre=Label(fondo3, text="Nuevo nombre del producto", font=("Inter", 24), bg="white")
        lbl_nombre.pack(padx=20, pady=10)
        
        nombre_entry=Entry(fondo3, font=("Inter", 24), bg="white")
        nombre_entry.insert(0, initial_name)
        nombre_entry.pack(padx=20, pady=10)

        lbl_precio=Label(fondo3, text="Nuevo precio unitario", font=("Inter", 24), bg="white")
        lbl_precio.pack(padx=20, pady=10)

        precio_entry=Entry(fondo3, font=("Inter", 24), bg="white")
        precio_entry.insert(0, initial_price)
        precio_entry.pack(padx=20, pady=10)

        def on_modificar():
            nonlocal pid
            nuevo_nombre = nombre_entry.get().strip()
            precio_text = precio_entry.get().strip()
            if not nuevo_nombre:
                messagebox.showerror("Error", "El nombre no puede estar vacío.")
                return
            try:
                nuevo_precio = float(precio_text)
            except Exception:
                messagebox.showerror("Error", "Precio inválido. Introduce un número válido.")
                return

            if pid is None:
                messagebox.showerror("Error", "Id de producto desconocido. No se puede modificar.")
                return

            # Pedir contraseña antes de modificar
            pwd = simpledialog.askstring("Autorización", "Ingrese la contraseña para modificar:", show='*', parent=modificar_producto)
            if pwd is None:
                return
            if pwd != '1234':
                messagebox.showerror("Error", "Contraseña incorrecta.")
                return

            modificado = metodos_productos.Productos_acciones.modificar_producto(nuevo_nombre, nuevo_precio, pid)
            if modificado:
                messagebox.showinfo("Éxito", "Producto modificado correctamente.")
                self.menu_producto(modificar_producto)
            else:
                messagebox.showerror("Error", "No se pudo modificar el producto. Verifique la conexión o los datos.")

        btn_agregar=Button(fondo3, text="Modificar", font=("Inter", 24), bg="#F1C045", command=on_modificar)
        btn_agregar.pack(padx=20, pady=10)

        btn_regresar=Button(fondo3, text="Regresar", font=("Inter", 24), bg="#F1C045", command=lambda: self.menu_producto(modificar_producto))
        btn_regresar.pack(padx=20, pady=10)

    def regresar(self,menu_usuarios):
        menu_principal.interfacesMenu(menu_usuarios)
