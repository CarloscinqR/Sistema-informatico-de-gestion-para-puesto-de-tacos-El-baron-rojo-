import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog
from view import menu_principal
from model import metodos_ingredientes, metodos_productos

# Admin password
ADMIN_PASSWORD = os.getenv('TACOS_ADMIN_PASSWORD', '1234')


class interfacesIngrediente():
    def __init__(self, menu_ingredientes):
        menu_ingredientes.title("Menu ingredientes")
        menu_ingredientes.geometry("1280x720")
        menu_ingredientes.state("zoomed")
        self.menu_ingrediente(menu_ingredientes)

    def borrarPantalla(self, ventana):
        for widget in ventana.winfo_children():
            widget.destroy()

    def menu_ingrediente(self, menu_ingredientes):
        """Main ingredients GUI: list, create, edit, delete."""
        self.borrarPantalla(menu_ingredientes)
        fondo = Frame(menu_ingredientes, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        # main canvas holds the scrollable red panel

        # Canvas + scrollbar for the whole red panel (so the menu can scroll vertically)
        # Use grid on `fondo` so we can anchor the bottom toolbar outside the scrollable area
        main_canvas = Canvas(fondo, bg="#D6D0C5", highlightthickness=0)
        main_vsb = ttk.Scrollbar(fondo, orient='vertical', command=main_canvas.yview)
        main_canvas.configure(yscrollcommand=main_vsb.set)
        # Configure grid rows/columns for `fondo` to make canvas expand and toolbar stick to bottom
        fondo.grid_rowconfigure(0, weight=1)
        fondo.grid_rowconfigure(1, weight=0)
        fondo.grid_columnconfigure(0, weight=1)
        fondo.grid_columnconfigure(1, weight=0)
        main_canvas.grid(row=0, column=0, sticky='nsew')
        main_vsb.grid(row=0, column=1, sticky='ns')

        scroll_container = Frame(main_canvas, bg="#D6D0C5")
        scroll_window = main_canvas.create_window((0, 0), window=scroll_container, anchor='nw')

        def _on_scroll_configure(event=None):
            try:
                main_canvas.configure(scrollregion=main_canvas.bbox('all'))
                # set width to prevent horizontal scroll
                main_canvas.itemconfig(scroll_window, width=main_canvas.winfo_width())
            except Exception:
                pass

        scroll_container.bind('<Configure>', _on_scroll_configure)
        def _on_canvas_configure(event=None):
            try:
                main_canvas.itemconfig(scroll_window, width=event.width)
            except Exception:
                pass

        main_canvas.bind('<Configure>', _on_canvas_configure)

        # Mousewheel scroll only when pointer is over canvas / scroll_container
        def _on_mousewheel(event):
            try:
                main_canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
            except Exception:
                pass

        def _bind_canvas_mousewheel(event):
            main_canvas.bind_all('<MouseWheel>', _on_mousewheel)

        def _unbind_canvas_mousewheel(event):
            main_canvas.unbind_all('<MouseWheel>')

        main_canvas.bind('<Enter>', _bind_canvas_mousewheel)
        main_canvas.bind('<Leave>', _unbind_canvas_mousewheel)

        # Red panel sits inside scroll_container so it can scroll
        fondo2 = Frame(scroll_container, bg="#A6171C", width=1200, height=700)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=40, pady=40)

        lbl_titulo = Label(fondo2, text="Ingredientes", font=("Orelega One", 36), fg="#F1C045", bg="#A6171C")
        lbl_titulo.pack(padx=20, pady=20)

        contenedor_tabla = Frame(fondo2, bg="white", width=1200, height=450)
        contenedor_tabla.pack_propagate(False)
        contenedor_tabla.pack(side=LEFT, padx=20, pady=10)

        # --- Tabla de ingredientes (Treeview) ---
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

        columns = ('Id_ingrediente', 'Nombre', 'Cantidad', 'Unidad', 'Acciones')

        header_frame = Frame(contenedor_tabla, bg='#A6171C')
        header_frame.pack(fill='x', padx=20, pady=(10, 0))
        header_frame.columnconfigure(0, weight=120)
        header_frame.columnconfigure(1, weight=380)
        header_frame.columnconfigure(2, weight=120)
        header_frame.columnconfigure(3, weight=120)
        header_frame.columnconfigure(4, weight=260)

        lbl_h_id = Label(header_frame, text='Id_ingrediente', bg='#A6171C', fg='#F1C045', font=('Orelega One', 16), anchor='center')
        lbl_h_nombre = Label(header_frame, text='Nombre', bg='#A6171C', fg='#F1C045', font=('Orelega One', 16), anchor='w')
        lbl_h_cant = Label(header_frame, text='Cantidad', bg='#A6171C', fg='#F1C045', font=('Orelega One', 16), anchor='center')
        lbl_h_unidad = Label(header_frame, text='Unidad', bg='#A6171C', fg='#F1C045', font=('Orelega One', 16), anchor='center')
        lbl_h_acciones = Label(header_frame, text='Acciones', bg='#A6171C', fg='#F1C045', font=('Orelega One', 16), anchor='center')

        lbl_h_id.grid(row=0, column=0, sticky='we', padx=(4,2))
        lbl_h_nombre.grid(row=0, column=1, sticky='we', padx=2)
        lbl_h_cant.grid(row=0, column=2, sticky='we', padx=2)
        lbl_h_unidad.grid(row=0, column=3, sticky='we', padx=2)
        lbl_h_acciones.grid(row=0, column=4, sticky='we', padx=(2,4))

        tabla = ttk.Treeview(contenedor_tabla, columns=columns, show='', selectmode='browse')
        tabla.column('Id_ingrediente', width=120, anchor=CENTER)
        tabla.column('Nombre', width=380, anchor=W)
        tabla.column('Cantidad', width=120, anchor=CENTER)
        tabla.column('Unidad', width=120, anchor=CENTER)
        tabla.column('Acciones', width=260, anchor=CENTER)

        vsb = ttk.Scrollbar(contenedor_tabla, orient='vertical')
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

        tabla.tag_configure('odd', background='#FFFFFF')
        tabla.tag_configure('even', background='#F6F0E8')

        _row_buttons = {}

        # container for action buttons inside content: Edit & Delete
        btn_frame = Frame(fondo2, bg="#A6171C")
        btn_frame.pack(padx=20, pady=10, fill='x')
        btn_editar = Button(btn_frame, text="Editar seleccionado", font=("Inter", 24), bg="#F1C045", fg="#A6171C", command=lambda: on_editar_selected(), width=22)
        btn_editar.pack(side=LEFT, padx=10)
        btn_borrar = Button(btn_frame, text="Borrar seleccionado", font=("Inter", 24), bg="#F1C045", fg="#A6171C", command=lambda: on_borrar_selected(), width=22)
        btn_borrar.pack(side=LEFT, padx=10)
        # NOTE: Agregar and Regresar buttons will be placed in a bottom toolbar outside the scrollable content

        def on_borrar(iid, id_ing, name):
            confirm = messagebox.askyesno("Confirmar eliminación", f"¿Desea eliminar el ingrediente?\nID: {id_ing}\nNombre: {name}")
            if not confirm:
                return
            eliminado = metodos_ingredientes.Ingredientes_acciones.borrar(id_ing)
            if eliminado:
                messagebox.showinfo("Éxito", "Ingrediente eliminado correctamente.")
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
                messagebox.showerror("Error", "No se pudo eliminar el ingrediente. Verifique la conexión o los datos.")

        def on_editar(iid, ing_tuple):
            try:
                self.modificarIngrediente(menu_ingredientes, ing_tuple[0])
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir la ventana de modificación: {e}")

        def load_items():
            # Clear tree and destroy buttons
            for n in tabla.get_children():
                tabla.delete(n)
            for b_ed, b_del in list(_row_buttons.values()):
                try:
                    if b_ed:
                        b_ed.destroy()
                except Exception:
                    pass
                try:
                    if b_del:
                        b_del.destroy()
                except Exception:
                    pass
            _row_buttons.clear()
            try:
                items = metodos_ingredientes.Ingredientes_acciones.obtener_ingredientes()
                num_ingredientes=1
                for i, ing in enumerate(items):
                    # ing = (id, name, measurement_unit, quantity)
                    iid = tabla.insert('', 'end', values=(num_ingredientes, ing[1], ing[3], ing[2], ''), tags=('even' if i % 2 == 0 else 'odd',))
                    btn_editar = Button(tabla, text='Editar', font=("Inter", 11), fg='#A6171C', bg='#F1F0EE', relief=RAISED, bd=1, padx=6, pady=2)
                    btn_borrar = Button(tabla, text='Borrar', font=("Inter", 11), fg='#FFFFFF', bg='#A6171C', relief=RAISED, bd=1, padx=6, pady=2)
                    btn_editar.config(command=lambda iid=iid, ing=ing: on_editar(iid, ing))
                    btn_borrar.config(command=lambda iid=iid, id_ing=ing[0], name=ing[1]: on_borrar(iid, id_ing, name))
                    _row_buttons[iid] = (btn_editar, btn_borrar)
                    num_ingredientes+=1
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar ingredientes: {e}")

        def on_borrar_selected():
            sel = tabla.selection()
            if not sel:
                messagebox.showwarning("Advertencia", "Seleccione un ingrediente a borrar.")
                return
            iid = sel[0]
            vals = tabla.item(iid, 'values')
            if not vals:
                return
            on_borrar(iid, vals[0], vals[1])

        def on_editar_selected():
            sel = tabla.selection()
            if not sel:
                messagebox.showwarning("Advertencia", "Seleccione un ingrediente a editar.")
                return
            iid = sel[0]
            vals = tabla.item(iid, 'values')
            id_ing = vals[0]
            self.modificarIngrediente(menu_ingredientes, id_ing)

        tabla.tag_configure('odd', background='#FFFFFF')
        tabla.tag_configure('even', background='#F6F0E8')
        load_items()

        def reposition_buttons():
            for iid, (b_ed, b_del) in _row_buttons.items():
                try:
                    bbox = tabla.bbox(iid, column='Acciones')
                except Exception:
                    bbox = None
                if not bbox:
                    b_ed.place_forget()
                    b_del.place_forget()
                    continue
                x, y, width, height = bbox
                btn_width = int(width * 0.45)
                gap = 6
                b_ed.place(x=x + 4, y=y + 2, width=btn_width - gap, height=height - 4)
                b_del.place(x=x + 4 + btn_width, y=y + 2, width=btn_width - gap, height=height - 4)

        tabla.bind('<Configure>', lambda e: reposition_buttons())
        tabla.bind('<ButtonRelease-1>', lambda e: reposition_buttons())
        tabla.bind_all('<MouseWheel>', lambda e: (reposition_buttons(), None))
        try:
            reposition_buttons()
        except Exception:
            pass

        # Bottom toolbar fixed (outside scrollable main_canvas) so Add/Return stay visible
        bottom_toolbar = Frame(fondo, bg="#A6171C")
        # anchor the bottom toolbar in a grid row under the scrollable canvas
        bottom_toolbar.grid(row=1, column=0, columnspan=2, sticky='ew', padx=40, pady=(0, 20))
        btn_agregar_bottom = Button(bottom_toolbar, text="Agregar ingrediente", font=("Inter", 20), bg="#F1C045", fg="#A6171C", command=lambda: self.nuevoIngrediente(menu_ingredientes), width=22)
        btn_agregar_bottom.pack(side=LEFT, padx=10, pady=10)
        btn_regresar_bottom = Button(bottom_toolbar, text="Regresar", font=("Inter", 20), bg="#F1C045", fg="#A6171C", command=lambda: self.regresar(menu_ingredientes), width=22)
        btn_regresar_bottom.pack(side=RIGHT, padx=10, pady=10)

    def nuevoIngrediente(self, nuevo_ingrediente):
        """Add a new ingredient via a small form."""
        self.borrarPantalla(nuevo_ingrediente)
        nuevo_ingrediente.title("Nuevo ingrediente")
        # Keep same size as main menu (do not shrink)
        try:
            nuevo_ingrediente.state("zoomed")
        except Exception:
            # fallback: keep current geometry
            pass

        fondo = Frame(nuevo_ingrediente, bg="#D6D0C5")
        fondo.pack(fill='both', expand=True)

        fondo2 = Frame(fondo, bg="#A6171C")
        fondo2.pack(padx=40, pady=40, fill='both', expand=True)

        lbl_nombre = Label(fondo2, text="Nombre", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_nombre.pack(padx=20, pady=10)
        ent_nombre = Entry(fondo2, font=("Inter", 14))
        ent_nombre.pack(padx=20, pady=10)

        lbl_unit = Label(fondo2, text="Unidad de medida", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_unit.pack(padx=20, pady=10)
        ent_unit = Entry(fondo2, font=("Inter", 14))
        ent_unit.pack(padx=20, pady=10)

        # Link to product (required)
        lbl_id_prod = Label(fondo2, text="Producto", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_id_prod.pack(padx=20, pady=10)
        # Load product names for convenience (if available)
        products = metodos_productos.Productos_acciones.obtener_productos() if hasattr(metodos_productos.Productos_acciones, 'obtener_productos') else []
        # Build mapping name -> id and id -> name
        prod_id_by_name = {str(p[1]): p[0] for p in products} if products else {}
        prod_name_by_id = {p[0]: str(p[1]) for p in products} if products else {}
        prod_names = list(prod_id_by_name.keys()) if prod_id_by_name else []
        cb_prod = ttk.Combobox(fondo2, values=prod_names, state='readonly')
        if prod_names:
            cb_prod.set(prod_names[0])
        cb_prod.pack(padx=20, pady=10)

        lbl_qty = Label(fondo2, text="Cantidad", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_qty.pack(padx=20, pady=10)
        ent_qty = Entry(fondo2, font=("Inter", 14))
        ent_qty.pack(padx=20, pady=10)

        def on_save():
            name = ent_nombre.get().strip()
            unit = ent_unit.get().strip()
            prod_name = cb_prod.get().strip()
            qty = ent_qty.get().strip()
            
            if not name:
                messagebox.showerror("Error", "El nombre es requerido.")
                return
            if not unit:
                messagebox.showerror("Error", "La unidad de medida es requerida.")
                return
            if not prod_name:
                messagebox.showerror("Error", "El producto es requerido.")
                return
            if not qty:
                messagebox.showerror("Error", "La cantidad es requerida.")
                return
            
            id_prod = prod_id_by_name.get(prod_name)
            if id_prod is None:
                messagebox.showerror("Error", "Producto seleccionado inválido.")
                return
            
            try:
                float(qty)
            except Exception:
                messagebox.showerror("Error", "Cantidad inválida.")
                return

            new_id = metodos_ingredientes.Ingredientes_acciones.agregar(name, unit, id_prod, qty)
            if not new_id:
                messagebox.showerror("Error", "No se pudo agregar ingrediente.")
                return
            messagebox.showinfo("Éxito", "Ingrediente agregado correctamente.")
            self.menu_ingrediente(nuevo_ingrediente)

        # Save directly (no UI length limit for measurement unit; DB may constrain length)
        btn_save = Button(fondo2, text='Guardar', command=on_save, bg='#F1C045')
        btn_save.pack(padx=20, pady=20)
        btn_cancel = Button(fondo2, text='Cancelar', command=lambda: self.menu_ingrediente(nuevo_ingrediente), bg='#F1C045')
        btn_cancel.pack(padx=20, pady=10)

    def modificarIngrediente(self, modificar_ingrediente, id_ingredient):
        """Modify an existing ingredient by id."""
        self.borrarPantalla(modificar_ingrediente)
        modificar_ingrediente.title("Modificar ingrediente")
        # Keep same size as main menu (do not shrink)
        try:
            modificar_ingrediente.state("zoomed")
        except Exception:
            pass

        fondo = Frame(modificar_ingrediente, bg="#D6D0C5")
        fondo.pack(fill='both', expand=True)
        fondo2 = Frame(fondo, bg="#A6171C")
        fondo2.pack(padx=40, pady=40, fill='both', expand=True)

        # load ingredient
        try:
            ings = metodos_ingredientes.Ingredientes_acciones.obtener_ingredientes()
            sel = next((i for i in ings if str(i[0]) == str(id_ingredient)), None)
            if not sel:
                messagebox.showerror("Error", "Ingrediente no encontrado.")
                self.menu_ingrediente(modificar_ingrediente)
                return
            # id, name, measurement_unit, quantity
            _, name, unit, qty = sel
        except Exception:
            messagebox.showerror("Error", "No se pudo cargar ingrediente.")
            self.menu_ingrediente(modificar_ingrediente)
            return

        lbl_nombre = Label(fondo2, text="Nombre", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_nombre.pack(padx=20, pady=10)
        ent_nombre = Entry(fondo2, font=("Inter", 14))
        ent_nombre.insert(0, name)
        ent_nombre.pack(padx=20, pady=10)

        lbl_unit = Label(fondo2, text="Unidad de medida", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_unit.pack(padx=20, pady=10)
        ent_unit = Entry(fondo2, font=("Inter", 14))
        ent_unit.insert(0, unit)
        ent_unit.pack(padx=20, pady=10)

        lbl_id_prod = Label(fondo2, text="Producto", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_id_prod.pack(padx=20, pady=10)
        products = metodos_productos.Productos_acciones.obtener_productos() if hasattr(metodos_productos.Productos_acciones, 'obtener_productos') else []
        prod_id_by_name = {str(p[1]): p[0] for p in products} if products else {}
        prod_name_by_id = {p[0]: str(p[1]) for p in products} if products else {}
        prod_names = list(prod_id_by_name.keys()) if prod_id_by_name else []
        cb_prod = ttk.Combobox(fondo2, values=prod_names, state='readonly')
        if prod_names:
            cb_prod.set(prod_names[0])
        cb_prod.pack(padx=20, pady=10)

        lbl_qty = Label(fondo2, text="Cantidad", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_qty.pack(padx=20, pady=10)
        ent_qty = Entry(fondo2, font=("Inter", 14))
        ent_qty.insert(0, str(qty))
        ent_qty.pack(padx=20, pady=10)

        def on_update():
            new_name = ent_nombre.get().strip()
            new_unit = ent_unit.get().strip()
            new_prod_name = cb_prod.get().strip()
            new_qty = ent_qty.get().strip()
            
            if not new_name:
                messagebox.showerror("Error", "El nombre es requerido.")
                return
            if not new_unit:
                messagebox.showerror("Error", "La unidad de medida es requerida.")
                return
            if not new_prod_name:
                messagebox.showerror("Error", "El producto es requerido.")
                return
            if not new_qty:
                messagebox.showerror("Error", "La cantidad es requerida.")
                return
            
            new_prod = prod_id_by_name.get(new_prod_name)
            if new_prod is None:
                messagebox.showerror("Error", "Producto seleccionado inválido.")
                return
            
            try:
                float(new_qty)
            except Exception:
                messagebox.showerror("Error", "Cantidad inválida.")
                return

            res = metodos_ingredientes.Ingredientes_acciones.modificar(new_name, new_unit, id_ingredient, new_prod, new_qty)
            if isinstance(res, tuple):
                ok, err = res
            else:
                ok = bool(res)
                err = None
            if ok:
                messagebox.showinfo("Éxito", "Ingrediente modificado.")
                self.menu_ingrediente(modificar_ingrediente)
            else:
                message = err if err else "No se pudo modificar el ingrediente."
                messagebox.showerror("Error", message)

        btn_save = Button(fondo2, text='Guardar', command=on_update, bg='#F1C045')
        btn_save.pack(padx=20, pady=10)
        btn_cancel = Button(fondo2, text='Cancelar', command=lambda: self.menu_ingrediente(modificar_ingrediente), bg='#F1C045')
        btn_cancel.pack(padx=20, pady=10)

    def regresar(self, menu_usuarios):
        menu_principal.interfacesMenu(menu_usuarios)




