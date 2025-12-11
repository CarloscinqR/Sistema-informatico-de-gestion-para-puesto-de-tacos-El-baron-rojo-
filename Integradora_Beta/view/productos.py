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

    def menu_producto(self, menu_productos):
        self.borrarPantalla(menu_productos)

        # -------------------------------------------
        # Fondo general
        # -------------------------------------------
        fondo = Frame(menu_productos, bg="#F4F4F4")
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
            text="Productos",
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
        style.map("Treeview", background=[('selected', "#FF5E5E")], foreground=[('selected', 'black')])

        # -------------------------------------------
        # ENCABEZADO
        # -------------------------------------------
        columns = ('Id_producto', 'Nombre_producto', 'Categoria', 'Precio_unitario', 'Acciones')

        header_frame = Frame(contenedor_tabla, bg="#A6171C")
        header_frame.pack(fill='x')

        header_cfg = dict(bg="#A6171C", fg="white", font=('Orelega One', 15))

        Label(header_frame, text='Id_producto', anchor='center', **header_cfg).grid(row=0, column=0, sticky='we')
        Label(header_frame, text='Nombre_producto', anchor='w', **header_cfg).grid(row=0, column=1, sticky='we')
        Label(header_frame, text='Categoría', anchor='center', **header_cfg).grid(row=0, column=2, sticky='we')
        Label(header_frame, text='Precio_unitario', anchor='e', **header_cfg).grid(row=0, column=3, sticky='we')
        Label(header_frame, text='Acciones', anchor='center', **header_cfg).grid(row=0, column=4, sticky='we')

        header_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=3)
        header_frame.columnconfigure(2, weight=2)
        header_frame.columnconfigure(3, weight=2)
        header_frame.columnconfigure(4, weight=2)

        # -------------------------------------------
        # TABLA TREEVIEW
        # -------------------------------------------
        tabla = ttk.Treeview(contenedor_tabla, columns=columns, show='', selectmode='browse')

        tabla.column('Id_producto', anchor=CENTER)
        tabla.column('Nombre_producto', anchor=W)
        tabla.column('Categoria', anchor=CENTER)
        tabla.column('Precio_unitario', anchor=E)
        tabla.column('Acciones', anchor=CENTER)

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

        productos = metodos_productos.Productos_acciones.mostrar_productos()
        _row_buttons = {}

        def on_borrar(iid, pid, pname):
            confirm = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Desea eliminar el producto?\nID: {pid}\nNombre: {pname}"
            )
            if not confirm:
                return

            eliminado = metodos_productos.Productos_acciones.borrar(pid)
            if eliminado:
                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
                try:
                    b_ed, b_del = _row_buttons.pop(iid, (None, None))
                    if b_ed: b_ed.destroy()
                    if b_del: b_del.destroy()
                    tabla.delete(iid)
                    reposition_buttons()
                except:
                    pass
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto.")

        def on_editar(iid, producto_tuple):
            try:
                self.modificarProducto(menu_productos, producto_tuple)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir la ventana: {e}")

        # -------------------------------------------
        # LLENAR TABLA CON BOTONES
        # -------------------------------------------
        for i, producto in enumerate(productos):
            precio = producto[3]
            try:
                precio_text = f"{float(precio):.2f} MXN"
            except:
                precio_text = str(precio)

            tag = 'even' if i % 2 == 0 else 'odd'

            item_id = tabla.insert('', 'end',
                                values=(i+1, producto[1], producto[2], precio_text, ''),
                                tags=(tag,))

            btn_editar = Button(
                tabla,
                text='Editar',
                font=("Inter", 9),
                bg="white",
                fg="#A6171C",
                relief="solid",
                bd=1,
                highlightthickness=0
            )

            btn_borrar = Button(
                tabla,
                text='Borrar',
                font=("Inter", 9),
                bg="#A6171C",
                fg="white",
                relief="solid",
                bd=1,
                highlightthickness=0
            )

            btn_editar.config(command=lambda iid=item_id, prod=producto: on_editar(iid, prod))
            btn_borrar.config(command=lambda iid=item_id, pid=producto[0], pname=producto[1]: on_borrar(iid, pid, pname))

            _row_buttons[item_id] = (btn_editar, btn_borrar)

        menu_productos.update_idletasks()

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
                btn_width = int((width - 8) / 2)
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
        # BOTONES INFERIORES (REDUCIDOS)
        # -------------------------------------------
        botones_frame = Frame(fondo2, bg="#A6171C")
        botones_frame.place(relx=0.5, rely=0.92, anchor="center")

        btn_agregarProducto = Button(
            botones_frame,
            text="Agregar producto",
            font=("Inter", 16),
            fg="white",
            bg="#A6171C",
            relief="flat",
            padx=24,
            pady=6,
            width=18,
            command=lambda: self.nuevoProducto(menu_productos)
        )
        btn_agregarProducto.grid(row=0, column=0, padx=25)

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
            command=lambda: self.regresar(menu_productos)
        )
        btn_regresar.grid(row=0, column=1, padx=25)



    def nuevoProducto(self, nuevo_producto):
        self.borrarPantalla(nuevo_producto)
        nuevo_producto.title("Nuevo producto")
        nuevo_producto.geometry("1920x1080")
        nuevo_producto.state("zoomed")

        # ===========================
        # FONDO GENERAL ROJO (como nuevoUsuario)
        # ===========================
        fondo = Frame(nuevo_producto, bg="#A6171C")
        fondo.pack(fill="both", expand=True)

        # ===========================
        # CONTENEDOR BLANCO CENTRADO
        # ===========================
        container = Frame(
            fondo,
            bg="white",
            width=600,
            height=750,
            highlightbackground="#F1C045",
            highlightthickness=4
        )
        container.place(relx=0.5, rely=0.5, anchor="center")
        container.pack_propagate(False)

        # ===========================
        # TÍTULO
        # ===========================
        lbl_titulo = Label(
            container,
            text="Nuevo producto",
            font=("Orelega One", 42),
            fg="#A6171C",
            bg="white"
        )
        lbl_titulo.pack(pady=(40, 10))

        # ===========================
        # FORM FRAME (scrollable pero manteniendo estilo)
        # ===========================
        form_container = Frame(container, bg="white")
        form_container.pack(fill="both", expand=True)

        canvas = Canvas(form_container, bg="white", highlightthickness=0)
        scroll = ttk.Scrollbar(form_container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)

        scroll.pack(side=RIGHT, fill=Y)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        inner = Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=inner, anchor="nw")

        def update_scroll(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner.bind("<Configure>", update_scroll)

        # ===========================
        # CAMPOS DEL PRODUCTO
        # ===========================
        def formato_label(texto):
            return Label(inner, text=texto, font=("Inter", 20), bg="white", anchor="w")

        def formato_entry():
            return Entry(inner, font=("Inter", 20), bg="#F7F7F7", relief="flat")

        # Nombre
        formato_label("Nombre del producto").pack(anchor="w", padx=40, pady=(10, 0))
        entry_nombre = formato_entry()
        entry_nombre.pack(padx=40, pady=10, fill="x")

        # Precio
        formato_label("Precio unitario").pack(anchor="w", padx=40, pady=(10, 0))
        entry_precio = formato_entry()
        entry_precio.pack(padx=40, pady=10, fill="x")

        # Categoría
        formato_label("Categoría").pack(anchor="w", padx=40, pady=(10, 0))
        categorias = ["Alimentos", "Bebida", "Especiales"]
        combo_categoria = ttk.Combobox(inner, values=categorias, state="readonly", font=("Inter", 18))
        combo_categoria.set(categorias[0])
        combo_categoria.pack(padx=40, pady=10, fill="x")

        # ===========================
        # INGREDIENTES (checkbox + cantidad)
        # ===========================
        formato_label("Ingredientes").pack(anchor="w", padx=40, pady=(20, 10))

        ingredientes = metodos_productos.Productos_acciones.obtener_ingredientes()
        ingredientes_vars = []
        ingredientes_entries = []

        ingredientes_frame = Frame(inner, bg="white")
        ingredientes_frame.pack(padx=20, pady=10)

        columnas = 2  # mejor estética dentro del cuadro blanco

        for i, (id_ing, nombre) in enumerate(ingredientes):
            fila = i // columnas
            col = i % columnas

            # checkbox
            var = IntVar(value=0)
            chk = Checkbutton(
                ingredientes_frame,
                text=nombre,
                variable=var,
                onvalue=id_ing,
                offvalue=0,
                bg="white",
                font=("Inter", 16),
                anchor="w"
            )
            chk.grid(row=fila, column=col*2, sticky="w", padx=10, pady=5)

            # campo cantidad
            ent = Entry(ingredientes_frame, width=5, font=("Inter", 14), bg="#F7F7F7", relief="flat")
            ent.grid(row=fila, column=col*2 + 1, padx=5)

            ingredientes_vars.append(var)
            ingredientes_entries.append(ent)

        # ===========================
        # GUARDAR PRODUCTO
        # ===========================
        def on_agregar():
            nombre = entry_nombre.get().strip()
            precio = entry_precio.get().strip()
            categoria = combo_categoria.get().strip()

            if not nombre or not precio:
                messagebox.showerror("Error", "Completa todos los campos del producto.")
                return

            try:
                precio = float(precio)
            except:
                messagebox.showerror("Error", "El precio debe ser numérico.")
                return

            ingredientes_sel = []
            for i, var in enumerate(ingredientes_vars):
                if var.get() != 0:
                    cantidad = ingredientes_entries[i].get().strip()
                    if not cantidad.isdigit() or int(cantidad) <= 0:
                        messagebox.showerror("Cantidad inválida", "Las cantidades deben ser números mayores a 0.")
                        return
                    ingredientes_sel.append((var.get(), int(cantidad)))

            nuevo_id = metodos_productos.Productos_acciones.agregar(nombre, precio, categoria)
            if not nuevo_id:
                messagebox.showerror("Error", "No se pudo registrar producto.")
                return

            if ingredientes_sel:
                ok = metodos_productos.Productos_acciones.agregar_ingredientes_detalle(nuevo_id, ingredientes_sel)
                if not ok:
                    messagebox.showerror("Advertencia", "Producto guardado, pero hubo errores con ingredientes.")

            messagebox.showinfo("Éxito", "Producto registrado correctamente.")
            self.menu_producto(nuevo_producto)

        # ===========================
        # BOTONES
        # ===========================
        botones_frame = Frame(inner, bg="white")
        botones_frame.pack(pady=30)

        btn_regresar = Button(
            botones_frame,
            text="Regresar",
            font=("Inter", 20),
            bg="#FFFFFF",
            fg="black",
            activebackground="#ABABAB",
            relief="flat",
            width=12,
            command=lambda: self.menu_producto(nuevo_producto)
        )
        btn_regresar.grid(row=0, column=0, padx=20)

        btn_agregar = Button(
            botones_frame,
            text="Agregar",
            font=("Inter", 20),
            bg="#A6171C",
            fg="white",
            activebackground="#8F1318",
            relief="flat",
            width=12,
            command=on_agregar
        )
        btn_agregar.grid(row=0, column=1, padx=20)


    def modificarProducto(self, modificar_producto, producto=None):
        self.borrarPantalla(modificar_producto)
        modificar_producto.title("Modificar producto")
        modificar_producto.geometry("1920x1080")
        modificar_producto.state("zoomed")

        # =====================================================
        # FONDO ROJO (mismo estilo que nuevoProducto)
        # =====================================================
        fondo = Frame(modificar_producto, bg="#A6171C")
        fondo.pack(fill="both", expand=True)

        # =====================================================
        # CONTENEDOR BLANCO CENTRADO — MISMO DISEÑO
        # =====================================================
        container = Frame(
            fondo,
            bg="white",
            width=650,
            height=820,
            highlightbackground="#F1C045",
            highlightthickness=4
        )
        container.place(relx=0.5, rely=0.5, anchor="center")
        container.pack_propagate(False)

        # =====================================================
        # TÍTULO
        # =====================================================
        lbl_titulo = Label(
            container,
            text="Modificar producto",
            font=("Orelega One", 42),
            fg="#A6171C",
            bg="white"
        )
        lbl_titulo.pack(pady=(40, 10))

        # =====================================================
        # CONTENEDOR SCROLLEABLE (igual que nuevoProducto)
        # =====================================================
        form_container = Frame(container, bg="white")
        form_container.pack(fill="both", expand=True)

        canvas = Canvas(form_container, bg="white", highlightthickness=0)
        scroll = ttk.Scrollbar(form_container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scroll.set)

        scroll.pack(side=RIGHT, fill=Y)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        inner = Frame(canvas, bg="white")
        canvas.create_window((0, 0), window=inner, anchor="nw")

        def update_scroll(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner.bind("<Configure>", update_scroll)

        # =====================================================
        # ESTILO DE CONTROLES DEL FORMULARIO
        # =====================================================
        def formato_label(texto):
            return Label(inner, text=texto, font=("Inter", 20), bg="white", anchor="w")

        def formato_entry():
            return Entry(inner, font=("Inter", 20), bg="#F7F7F7", relief="flat")

        # =====================================================
        # CARGA DE PRODUCTO
        # =====================================================
        pid = producto[0] if producto else None
        initial_name = producto[1] if producto else ""
        initial_category = producto[2] if producto else ""
        initial_price = str(producto[3]) if producto else ""

        # =====================================================
        # CAMPOS: Nombre
        # =====================================================
        formato_label("Nombre del producto").pack(anchor="w", padx=40, pady=(10, 0))
        entry_nombre = formato_entry()
        entry_nombre.insert(0, initial_name)
        entry_nombre.pack(padx=40, pady=10, fill="x")

        # =====================================================
        # Precio
        # =====================================================
        formato_label("Precio unitario").pack(anchor="w", padx=40, pady=(10, 0))
        entry_precio = formato_entry()
        entry_precio.insert(0, initial_price)
        entry_precio.pack(padx=40, pady=10, fill="x")

        # =====================================================
        # Categoría
        # =====================================================
        formato_label("Categoría").pack(anchor="w", padx=40, pady=(10, 0))

        categorias = ["Alimentos", "Bebida", "Especiales"]
        combo_categoria = ttk.Combobox(inner, values=categorias, state="readonly", font=("Inter", 18))
        combo_categoria.set(initial_category if initial_category in categorias else categorias[0])
        combo_categoria.pack(padx=40, pady=10, fill="x")

        # =====================================================
        # INGREDIENTES
        # =====================================================
        formato_label("Ingredientes").pack(anchor="w", padx=40, pady=(20, 10))

        ingredientes = metodos_productos.Productos_acciones.obtener_ingredientes()
        ingredientes_actuales = metodos_productos.Productos_acciones.obtener_ingredientes_producto(pid)
        cantidades_existentes = metodos_productos.Productos_acciones.obtener_ingredientes_con_cantidad(pid)

        ingredientes_vars = []

        ingredientes_frame = Frame(inner, bg="white")
        ingredientes_frame.pack(padx=20, pady=10)

        columnas = 2

        for i, (id_ing, nombre) in enumerate(ingredientes):

            fila = i // columnas
            col = i % columnas

            valor_inicial = id_ing if id_ing in ingredientes_actuales else 0
            var = IntVar(value=valor_inicial)

            chk = Checkbutton(
                ingredientes_frame,
                text=nombre,
                variable=var,
                onvalue=id_ing,
                offvalue=0,
                bg="white",
                font=("Inter", 16),
                anchor="w"
            )
            chk.grid(row=fila, column=col*2, sticky="w", padx=10, pady=5)

            ent = Entry(ingredientes_frame, width=5, font=("Inter", 14), bg="#F7F7F7", relief="flat")
            ent.grid(row=fila, column=col*2 + 1, padx=5)

            if id_ing in cantidades_existentes:
                ent.insert(0, str(cantidades_existentes[id_ing]))

            ingredientes_vars.append((var, id_ing, ent))

        # =====================================================
        # ACCIÓN DE GUARDAR
        # =====================================================
        def on_modificar():
            nombre = entry_nombre.get().strip()
            precio = entry_precio.get().strip()
            categoria = combo_categoria.get()

            if not nombre or not precio:
                messagebox.showerror("Error", "Completa todos los campos.")
                return

            try:
                precio = float(precio)
            except:
                messagebox.showerror("Error", "Precio inválido.")
                return

            ok = metodos_productos.Productos_acciones.modificar_producto(nombre, precio, pid, categoria)

            nuevos_ing = []
            for var, id_ing, ent in ingredientes_vars:
                if var.get() != 0:
                    cant = ent.get().strip()
                    if not cant.isdigit() or int(cant) <= 0:
                        messagebox.showerror("Error", "Cantidad inválida.")
                        return
                    nuevos_ing.append((id_ing, int(cant)))

            metodos_productos.Productos_acciones.actualizar_ingredientes(pid, nuevos_ing)

            if ok:
                messagebox.showinfo("Éxito", "Producto modificado.")
                self.menu_producto(modificar_producto)
            else:
                messagebox.showerror("Error", "No se pudo modificar el producto.")

        # =====================================================
        # BOTONES — MISMO ESTILO QUE NUEVOPRODUCTO
        # =====================================================
        botones_frame = Frame(inner, bg="white")
        botones_frame.pack(pady=30)

        btn_regresar = Button(
            botones_frame,
            text="Regresar",
            font=("Inter", 20),
            bg="#FFFFFF",
            fg="black",
            activebackground="#ABABAB",
            relief="flat",
            width=12,
            command=lambda: self.menu_producto(modificar_producto)
        )
        btn_regresar.grid(row=0, column=0, padx=20)

        btn_guardar = Button(
            botones_frame,
            text="Guardar",
            font=("Inter", 20),
            bg="#A6171C",
            fg="white",
            activebackground="#8F1318",
            relief="flat",
            width=12,
            command=on_modificar
        )
        btn_guardar.grid(row=0, column=1, padx=20)


    def regresar(self,menu_usuarios):
        menu_principal.interfacesMenu(menu_usuarios)

        