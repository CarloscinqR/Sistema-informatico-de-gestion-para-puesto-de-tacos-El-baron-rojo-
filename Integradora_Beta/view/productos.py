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
        style.configure('Treeview',foreground='black',rowheight=30,font=('Inter', 14))
        style.configure('Treeview.Heading',background='#A6171C',foreground='#F1C045',font=('Orelega One', 16))
        style.map('Treeview', background=[('selected', '#F1C045')], foreground=[('selected', 'black')])

        columns = ('Id_producto', 'Nombre_producto', 'Categoria', 'Precio_unitario', 'Acciones')
        header_frame = Frame(contenedor_tabla, bg='#A6171C')
        header_frame.pack(fill='x', padx=20, pady=(10, 0))
        header_frame.columnconfigure(0, weight=120)
        header_frame.columnconfigure(1, weight=480)
        header_frame.columnconfigure(2, weight=160)
        header_frame.columnconfigure(3, weight=160)
        header_frame.columnconfigure(4, weight=180)

        lbl_h_id = Label(header_frame, text='Id_producto', bg='#A6171C', fg='#F1C045', font=('Orelega One', 16), anchor='center')
        lbl_h_nombre = Label(header_frame, text='Nombre_producto', bg='#A6171C', fg='#F1C045', font=('Orelega One', 16), anchor='w')
        lbl_h_categoria = Label(header_frame, text='Categoría', bg='#A6171C', fg='#F1C045', font=('Orelega One', 16), anchor='center')
        lbl_h_precio = Label(header_frame, text='Precio_unitario', bg='#A6171C', fg='#F1C045', font=('Orelega One', 16), anchor='e')
        lbl_h_acciones = Label(header_frame, text='Acciones', bg='#A6171C', fg='#F1C045', font=('Orelega One', 16), anchor='center')

        lbl_h_id.grid(row=0, column=0, sticky='we', padx=(4,2))
        lbl_h_nombre.grid(row=0, column=1, sticky='we', padx=2)
        lbl_h_categoria.grid(row=0, column=2, sticky='we', padx=2)
        lbl_h_precio.grid(row=0, column=3, sticky='we', padx=2)
        lbl_h_acciones.grid(row=0, column=4, sticky='we', padx=(2,4))

        tabla = ttk.Treeview(contenedor_tabla, columns=columns, show='', selectmode='browse')
        tabla.column('Id_producto', width=120, anchor=CENTER)
        tabla.column('Nombre_producto', width=480, anchor=W)
        tabla.column('Categoria', width=160, anchor=CENTER)
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
        productos = metodos_productos.Productos_acciones.mostrar_productos()
        # contenedor para guardar referencias a botones por fila
        _row_buttons = {}

        def on_borrar(iid, pid, pname):
            confirm = messagebox.askyesno("Confirmar eliminación", f"¿Desea eliminar el producto?\nID: {pid}\nNombre: {pname}")
            if not confirm:
                return

            eliminado = metodos_productos.Productos_acciones.borrar(pid)
            if eliminado:
                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")

                try:
                    b_ed, b_del = _row_buttons.pop(iid, (None, None))
                    if b_ed:
                        b_ed.destroy()
                    if b_del:
                        b_del.destroy()
                    tabla.delete(iid)
                    reposition_buttons()
                except Exception:
                    pass
            else:
                messagebox.showerror("Error", "No se pudo eliminar el producto. Verifique la conexión o los datos.")

        # Handler para editar un producto: abre la interfaz de modificarProducto
        def on_editar(iid, producto_tuple):
            # Abrir la vista de modificación pre-llenada con la tupla completa
            # (id, nombre, precio, [categoria]) — si existe categoría la
            # pasamos para que el formulario se precargue.
            try:
                self.modificarProducto(menu_productos, producto_tuple)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir la ventana de modificación: {e}")

        for i, producto in enumerate(productos):
            precio = producto[3]
            try:
                precio_text = f"{float(precio):.2f} MXN"
            except Exception:
                precio_text = str(precio)
            tag = 'even' if i % 2 == 0 else 'odd'
            item_id = tabla.insert('', 'end', values=(i+1, producto[1], producto[2], precio_text, ''), tags=(tag,))

            btn_editar = Button(tabla, text='Editar', font=("Inter", 11), fg='#A6171C', bg='#F1F0EE', relief=RAISED, bd=1, padx=6, pady=2)
            btn_borrar = Button(tabla, text='Borrar', font=("Inter", 11), fg='#FFFFFF', bg='#A6171C', relief=RAISED, bd=1, padx=6, pady=2)
            # pass full producto tuple to the editor so it can populate category
            btn_editar.config(command=lambda iid=item_id, prod=producto: on_editar(iid, prod))
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

        tabla.bind('<Configure>', lambda e: reposition_buttons())
        tabla.bind('<ButtonRelease-1>', lambda e: reposition_buttons())
        tabla.bind('<Motion>', lambda e: None)
        # rueda del ratón en Windows
        tabla.bind_all('<MouseWheel>', lambda e: (reposition_buttons(), None))

        try:
            reposition_buttons()
        except Exception:
            pass

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

        desired_width = 1200
        fondo3 = Frame(fondo2, bg="white", width=desired_width, height=700)
        fondo3.pack_propagate(False)
        # pack without fill so the white panel stays centered horizontally
        # and sits under the title
        fondo3.pack(padx=20, pady=10)

        # Canvas + scrollbar inside the white frame — only this area scrolls
        canvas = Canvas(fondo3, bg="white", highlightthickness=0)
        v_scroll = ttk.Scrollbar(fondo3, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=v_scroll.set)
        v_scroll.pack(side=RIGHT, fill=Y)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)

        # Inner frame that will hold the actual form/widgets
        inner = Frame(canvas, bg='white')
        # Create a window inside the canvas to host the inner frame and keep
        # a reference so we can resize it to match the canvas width.
        inner_window = canvas.create_window((0, 0), window=inner, anchor='nw')

        # Update scrollregion when inner frame resizes
        def _on_inner_configure(event=None):
            canvas.configure(scrollregion=canvas.bbox('all'))
            try:
                # make the inner window match the visible canvas width so
                # widgets expand correctly and there is no horizontal scroll
                canvas.itemconfig(inner_window, width=canvas.winfo_width())
            except Exception:
                pass

        inner.bind('<Configure>', _on_inner_configure)

        # Only scroll the canvas when mouse is over it
        def _bind_to_mousewheel(event):
            canvas.bind_all('<MouseWheel>', _on_mousewheel)

        def _unbind_from_mousewheel(event):
            canvas.unbind_all('<MouseWheel>')

        def _on_mousewheel(event):
            # Windows scroll direction uses event.delta in multiples of 120
            canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

        canvas.bind('<Enter>', _bind_to_mousewheel)
        canvas.bind('<Leave>', _unbind_from_mousewheel)

        # Keep the inner frame width in sync when the canvas is resized
        def _on_canvas_configure(event):
            try:
                canvas.itemconfig(inner_window, width=event.width)
            except Exception:
                pass

        canvas.bind('<Configure>', _on_canvas_configure)

        # adjust fondo3 height so it reaches close to the bottom of fondo2
        def _adjust_fondo3_height():
            try:
                total = fondo2.winfo_height()
                title_h = lbl_titulo.winfo_height()
                # leave some padding at bottom and top
                new_h = max(300, total - title_h - 80)
                fondo3.configure(height=new_h)
                # ensure the canvas item is updated after the change
                canvas.update_idletasks()
                _on_inner_configure()
            except Exception:
                pass

        # schedule an initial adjustment after widgets are drawn
        fondo2.after(100, _adjust_fondo3_height)

        # place widgets inside the scrollable inner frame
        lbl_nombre = Label(inner, text="Nombre del producto", font=("Inter", 24), bg="white")
        lbl_nombre.pack(padx=20, pady=10)

        nombre_entry = Entry(inner, font=("Inter", 24), bg="white")
        nombre_entry.pack(padx=20, pady=10)

        lbl_precio = Label(inner, text="Precio unitario", font=("Inter", 24), bg="white")
        lbl_precio.pack(padx=20, pady=10)

        precio_entry = Entry(inner, font=("Inter", 24), bg="white")
        precio_entry.pack(padx=20, pady=10)
        
        lbl_categoria = Label(inner, text="Categoría", font=("Inter", 24), bg="white")
        lbl_categoria.pack(padx=20, pady=10)
        # use a Combobox (dropdown) for category selection so user can only
        # select one value easily
        categories = ["Alimentos", "Bebida", "Especiales"]
        combobox_categoria = ttk.Combobox(inner, values=categories, font=("Inter", 20), state='readonly')
        combobox_categoria.set(categories[0])
        combobox_categoria.pack(padx=20, pady=10)

        def on_agregar():
            nombre = nombre_entry.get().strip()
            precio = precio_entry.get().strip()
            categoria = combobox_categoria.get().strip()

            if not nombre or not precio or not categoria:
                messagebox.showwarning("Campos incompletos", "Completa todos los datos del producto.")
                return

            try:
                precio = float(precio)
            except ValueError:
                messagebox.showwarning("Precio inválido", "Ingresa un precio numérico válido.")
                return
            ingredientes_seleccionados = []

            for i, var in enumerate(ingredientes_vars):
                id_ing = ingredientes[i][0]       
                entry = ingredientes_entries[i]   
                if var.get() == id_ing:           
                    cantidad = entry.get().strip()

                    if not cantidad.isdigit() or int(cantidad) <= 0:
                        messagebox.showwarning("Cantidad inválida",f"La cantidad del ingrediente ID {id_ing} debe ser un número mayor a 0.")
                        return

                    ingredientes_seleccionados.append((id_ing, int(cantidad)))
            # Registrar producto
            producto_id = metodos_productos.Productos_acciones.agregar(nombre, precio, categoria)

            if not producto_id:
                messagebox.showerror("Error", "No se pudo registrar el producto.")
                return

            # Registrar ingredientes del producto
            if ingredientes_seleccionados:
                ok = metodos_productos.Productos_acciones.agregar_ingredientes_detalle(
                    producto_id,
                    ingredientes_seleccionados  
                )
                if not ok:
                    messagebox.showwarning("Advertencia", "El producto se registró, pero algunos ingredientes no se pudieron guardar.")
            messagebox.showinfo("Éxito", "Producto registrado correctamente.")
        marco = Frame(inner, bg="white")
        # === INGREDIENTES DESDE BD ===
        ingredientes = metodos_productos.Productos_acciones.obtener_ingredientes()

        ingredientes_vars = []       
        ingredientes_entries = []    

        lbl_ingredientes = Label(inner, text="Ingredientes", font=("Inter", 24), bg="white")
        lbl_ingredientes.pack(padx=20, pady=10)

        marco = Frame(inner, bg="white")
        marco.pack(padx=20, pady=10)

        columnas = 3

        for i, (id_ing, nombre) in enumerate(ingredientes):
            
            var = IntVar(value=0)  
            chk = Checkbutton(marco,text=nombre,variable=var,onvalue=id_ing,offvalue=0,font=("Inter", 18),bg="white")
            lbl_cantidad = Label(marco, text="Cantidad:", font=("Inter", 14), bg="white")
            etr = Entry(marco, width=5, font=("Inter", 14))

            fila = i // columnas
            col_base = (i % columnas) * 3

            chk.grid(row=fila, column=col_base, padx=10, pady=5, sticky="w")
            lbl_cantidad.grid(row=fila, column=col_base + 1, padx=5, pady=5)
            etr.grid(row=fila, column=col_base + 2, padx=5, pady=5)

            ingredientes_vars.append(var)
            ingredientes_entries.append(etr)

        marco.pack(padx=20, pady=10)

        btn_agregar = Button(inner, text="Agregar", font=("Inter", 24), bg="#F1C045", command=on_agregar)
        btn_agregar.pack(padx=20, pady=10)
        btn_regresar = Button(inner, text="Regresar", font=("Inter", 14), bg="#F1C045", command=lambda: self.menu_producto(nuevo_producto))
        btn_regresar.pack(padx=10, pady=50)

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

        pid = None
        initial_name = ""
        initial_price = ""
        if producto:
            try:
                pid = producto[0]
                initial_name = producto[1]
                initial_price = str(producto[3])
            except Exception:
                pid = None

        desired_width = 1200
        fondo3 = Frame(fondo2, bg='white', width=desired_width, height=700)
        fondo3.pack_propagate(False)
        fondo3.pack(padx=20, pady=10)

        canvas_mod = Canvas(fondo3, bg='white', highlightthickness=0)
        v_scroll_mod = ttk.Scrollbar(fondo3, orient='vertical', command=canvas_mod.yview)
        canvas_mod.configure(yscrollcommand=v_scroll_mod.set)
        v_scroll_mod.pack(side=RIGHT, fill=Y)
        canvas_mod.pack(side=LEFT, fill=BOTH, expand=True)

        inner_mod = Frame(canvas_mod, bg='white')
        inner_mod_window = canvas_mod.create_window((0, 0), window=inner_mod, anchor='nw')

        def _on_inner_mod_configure(event=None):
            canvas_mod.configure(scrollregion=canvas_mod.bbox('all'))
            try:
                canvas_mod.itemconfig(inner_mod_window, width=canvas_mod.winfo_width())
            except Exception:
                pass

        inner_mod.bind('<Configure>', _on_inner_mod_configure)

        def _bind_to_mousewheel_mod(event):
            canvas_mod.bind_all('<MouseWheel>', _on_mousewheel_mod)

        def _unbind_from_mousewheel_mod(event):
            canvas_mod.unbind_all('<MouseWheel>')

        def _on_mousewheel_mod(event):
            canvas_mod.yview_scroll(int(-1 * (event.delta / 120)), 'units')

        canvas_mod.bind('<Enter>', _bind_to_mousewheel_mod)
        canvas_mod.bind('<Leave>', _unbind_from_mousewheel_mod)

        def _on_canvas_mod_configure(event):
            try:
                canvas_mod.itemconfig(inner_mod_window, width=event.width)
            except Exception:
                pass

        canvas_mod.bind('<Configure>', _on_canvas_mod_configure)

        def _adjust_fondo3_mod_height():
            try:
                total = fondo2.winfo_height()
                title_h = lbl_titulo.winfo_height()
                new_h = max(300, total - title_h - 80)
                fondo3.configure(height=new_h)
                canvas_mod.update_idletasks()
                _on_inner_mod_configure()
            except Exception:
                pass

        fondo2.after(100, _adjust_fondo3_mod_height)


        initial_category = ""
        try:
            if producto and len(producto) > 2:
                initial_category = producto[2] or ""
        except Exception:
            initial_category = ""

        lbl_nombre = Label(inner_mod, text="Nombre del producto", font=("Inter", 24), bg="white")
        lbl_nombre.pack(padx=20, pady=10)

        nombre_entry = Entry(inner_mod, font=("Inter", 24), bg="white")
        nombre_entry.insert(0, initial_name)
        nombre_entry.pack(padx=20, pady=10)

        lbl_precio = Label(inner_mod, text="Precio unitario", font=("Inter", 24), bg="white")
        lbl_precio.pack(padx=20, pady=10)

        precio_entry = Entry(inner_mod, font=("Inter", 24), bg="white")
        precio_entry.insert(0, initial_price)
        precio_entry.pack(padx=20, pady=10)

        lbl_categoria_mod = Label(inner_mod, text="Categoría", font=("Inter", 24), bg="white")
        lbl_categoria_mod.pack(padx=20, pady=10)
        categories = ["Alimentos", "Bebida", "Especiales"]
        combobox_categoria_mod = ttk.Combobox(inner_mod, values=categories, font=("Inter", 20), state='readonly')
        combobox_categoria_mod.set(initial_category if initial_category in categories else categories[0])
        combobox_categoria_mod.pack(padx=20, pady=10)

        ingredientes_actuales = []
        if pid:
            ingredientes_actuales = metodos_productos.Productos_acciones.obtener_ingredientes_producto(pid)

        ingredientes = metodos_productos.Productos_acciones.obtener_ingredientes()

        ingredientes_vars = []

        lbl_ingredientes = Label(inner_mod, text="Ingredientes", font=("Inter", 24), bg="white")
        lbl_ingredientes.pack(padx=20, pady=10)

        marco = Frame(inner_mod, bg="white")
        marco.pack(padx=20, pady=10)
        columnas = 3
        for i, (id_ing, nombre) in enumerate(ingredientes):
            valor_inicial = id_ing if id_ing in ingredientes_actuales else 0

            var = IntVar(value=valor_inicial)
            chk = Checkbutton(marco,text=nombre,variable=var,onvalue=id_ing,offvalue=0,font=("Inter", 18),bg="white")
            lbl_cantidad = Label(marco,text="Cantidad:",font=("Inter", 14),bg="white")
            # Entry para la cantidad
            etr = Entry(marco, width=5, font=("Inter", 14))

            fila = i // columnas
            col_base = (i % columnas) * 3  

            chk.grid(row=fila, column=col_base, padx=10, pady=5, sticky="w")
            lbl_cantidad.grid(row=fila, column=col_base + 1, padx=5, pady=5)
            etr.grid(row=fila, column=col_base + 2, padx=5, pady=5)

            ingredientes_vars.append(var)
        def on_modificar():
            print(ingredientes_vars)#Problema aqui-----------------------
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

            selected_category_mod = None
            try:
                selected_category_mod = combobox_categoria_mod.get()
            except Exception:
                selected_category_mod = None
            modificado = metodos_productos.Productos_acciones.modificar_producto(nuevo_nombre, nuevo_precio, pid, selected_category_mod)
            nuevos_ingredientes = [v.get() for v in ingredientes_vars if v.get() != 0]
            
            modificado2=metodos_productos.Productos_acciones.actualizar_ingredientes(pid, nuevos_ingredientes)

            if modificado and modificado2:
                messagebox.showinfo("Éxito", "Producto modificado correctamente.")
                self.menu_producto(modificar_producto)
            else:
                messagebox.showerror("Error", "No se pudo modificar el producto. Verifique la conexión o los datos.")

        btn_agregar = Button(inner_mod, text="Guardar", font=("Inter", 24), bg="#F1C045", command=on_modificar)
        btn_agregar.pack(padx=20, pady=10)

        btn_regresar = Button(inner_mod, text="Regresar", font=("Inter", 14), bg="#F1C045", command=lambda: self.menu_producto(modificar_producto))
        btn_regresar.pack(padx=20, pady=10)

    def regresar(self,menu_usuarios):
        menu_principal.interfacesMenu(menu_usuarios)

        