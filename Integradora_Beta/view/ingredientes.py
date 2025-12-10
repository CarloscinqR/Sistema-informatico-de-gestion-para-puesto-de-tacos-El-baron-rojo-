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
        """Main ingredients GUI: list, create, edit, delete. (Diseño igual a menu_usuario, opción A)"""
        self.borrarPantalla(menu_ingredientes)

        # -------------------------------------------
        # Fondo general y contenedor central (85%)
        # -------------------------------------------
        fondo = Frame(menu_ingredientes, bg="#F4F4F4")
        fondo.pack(fill="both", expand=True)

        fondo2 = Frame(
            fondo,
            bg="#A6171C",
            highlightbackground="#610E11",
            highlightthickness=4
        )
        fondo2.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.85)

        # -------------------------------------------
        # Título
        # -------------------------------------------
        titulo_frame = Frame(fondo2, bg="#A6171C")
        titulo_frame.place(relx=0.5, y=50, anchor="center")

        lbl_titulo = Label(
            titulo_frame,
            text="Ingredientes",
            font=("Orelega One", 52),
            fg="white",
            bg="#A6171C"
        )
        lbl_titulo.pack()

        # -------------------------------------------
        # Tarjeta blanca que contiene la tabla
        # -------------------------------------------
        tabla_card = Frame(
            fondo2,
            bg="white",
            highlightbackground="#C0C0C0",
            highlightthickness=2
        )
        tabla_card.place(relx=0.5, rely=0.52, anchor="center", relwidth=0.90, relheight=0.70)

        # Contenedor interno tabla
        contenedor_tabla = Frame(tabla_card, bg="white")
        contenedor_tabla.pack(fill="both", expand=True, padx=20, pady=20)

        # -------------------------------------------
        # Estilos Treeview (igual que menu_usuario)
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
        style.map("Treeview", background=[('selected', '#F1C045')], foreground=[('selected', 'black')])

        # -------------------------------------------
        # Encabezado (barra roja)
        # -------------------------------------------
        columns = ('Id_ingrediente', 'Nombre', 'Unidad', 'Acciones')

        header_frame = Frame(contenedor_tabla, bg="#A6171C")
        header_frame.pack(fill='x')

        header_cfg = dict(bg="#A6171C", fg="white", font=('Orelega One', 15))

        Label(header_frame, text='Id', anchor='center', **header_cfg).grid(row=0, column=0, sticky='we')
        Label(header_frame, text='Nombre', anchor='w', **header_cfg).grid(row=0, column=1, sticky='we')
        Label(header_frame, text='Unidad', anchor='center', **header_cfg).grid(row=0, column=2, sticky='we')
        Label(header_frame, text='Acciones', anchor='center', **header_cfg).grid(row=0, column=3, sticky='we')

        # Proporciones (igual que menu_usuario pattern)
        header_frame.columnconfigure(0, weight=8)    # ID
        header_frame.columnconfigure(1, weight=45)   # Nombre (menos ancho)
        header_frame.columnconfigure(2, weight=10)   # Unidad
        header_frame.columnconfigure(3, weight=37)   # Acciones (más ancho para botones)

        # -------------------------------------------
        # Treeview
        # -------------------------------------------
        tabla = ttk.Treeview(contenedor_tabla, columns=columns, show='', selectmode='browse')

            # determinar anchos en base al contenedor (proporcional a 1920x1080)
        tabla.update_idletasks()
        total_width = tabla_card.winfo_width() or int(menu_ingredientes.winfo_screenwidth() * 0.85)
        if total_width <= 0:
            total_width = 1400

        # Nuevas proporciones más equilibradas
        tabla.column('Id_ingrediente', width=max(60, int(total_width * 0.08)), anchor=CENTER)
        tabla.column('Nombre',          width=max(250, int(total_width * 0.45)), anchor=W)
        tabla.column('Unidad',          width=max(80, int(total_width * 0.10)), anchor=CENTER)
        tabla.column('Acciones', width=int(total_width * 0.23), anchor=CENTER)



        # Scrollbar vertical
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

        # -------------------------------------------
        # Cargar datos y crear botones por fila
        # -------------------------------------------
        _row_buttons = {}

        def on_borrar(iid, id_ing, name):
            confirm = messagebox.askyesno("Confirmar eliminación", f"¿Desea eliminar el ingrediente?\nID: {id_ing}\nNombre: {name}")
            if not confirm:
                return
            eliminado = metodos_ingredientes.Ingredientes_acciones.borrar(id_ing)
            if eliminado:
                messagebox.showinfo("Éxito", "Ingrediente eliminado correctamente.")
                try:
                    b_ed, b_del = _row_buttons.pop(iid, (None, None))
                    if b_ed: b_ed.destroy()
                    if b_del: b_del.destroy()
                    tabla.delete(iid)
                    reposition_buttons()
                except:
                    pass
            else:
                messagebox.showerror("Error", "No se pudo eliminar el ingrediente. Verifique la conexión o los datos.")

        def on_editar(iid, ing_tuple):
            try:
                # mantener la lógica: pasar id real para edición
                self.modificarIngrediente(menu_ingredientes, ing_tuple[0])
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir la ventana de modificación: {e}")

        # función que carga los registros mostrando contador en la columna ID
        def load_items():
            # limpiar tabla y botones previos
            for n in tabla.get_children():
                tabla.delete(n)
            for b_ed, b_del in list(_row_buttons.values()):
                try:
                    if b_ed: b_ed.destroy()
                except:
                    pass
                try:
                    if b_del: b_del.destroy()
                except:
                    pass
            _row_buttons.clear()

            try:
                items = metodos_ingredientes.Ingredientes_acciones.obtener_ingredientes()
                contador = 1
                for i, ing in enumerate(items):
                    # ing = (id_real, name, measurement_unit, ...)
                    tag = 'even' if i % 2 == 0 else 'odd'
                    # mostramos contador en columna ID (opción 1)
                    iid = tabla.insert('', 'end', values=(contador, ing[1], ing[2], ''), tags=(tag,))

                    # crear botones (manteniendo comandos que usan id_real)
                    btn_editar = Button(
                        tabla,
                        text='Editar',
                        font=("Inter", 9),
                        bg="white",
                        fg="#A6171C",
                        relief="solid",
                        bd=1,
                        highlightthickness=0,
                        command=lambda iid=iid, ing=ing: on_editar(iid, ing)
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
                        command=lambda iid=iid, id_ing=ing[0], name=ing[1]: on_borrar(iid, id_ing, name)
                    )


                    _row_buttons[iid] = (btn_editar, btn_borrar)
                    contador += 1

                # intentar posicionar botones tras carga
                try:
                    reposition_buttons()
                except:
                    pass

            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar ingredientes: {e}")

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
                    try:
                        b_ed.place_forget()
                        b_del.place_forget()
                    except:
                        pass
                    continue

                x, y, width, height = bbox

                # MISMA LÓGICA QUE MENU_USUARIO
                btn_width = int((width - 16) / 2)

                try:
                    b_ed.place(
                        x=x + 2,
                        y=y + 4,
                        width=btn_width,
                        height=height - 8
                    )
                    b_del.place(
                        x=x + btn_width + 6,
                        y=y + 4,
                        width=btn_width,
                        height=height - 8
                    )
                except:
                    pass


        tabla.bind('<Configure>', lambda e: reposition_buttons())
        tabla.bind('<ButtonRelease-1>', lambda e: reposition_buttons())
        tabla.bind_all('<MouseWheel>', lambda e: reposition_buttons())

        # cargar inicialmente
        load_items()


        # -------------------------------------------
        # Botones inferiores (pequeños) - Add / Regresar
        # -------------------------------------------
        botones_frame = Frame(fondo2, bg="#A6171C")
        botones_frame.place(relx=0.5, rely=0.92, anchor="center")

        btn_agregar_bottom = Button(
            botones_frame,
            text="Agregar ingrediente",
            font=("Inter", 16),
            fg="white",
            bg="#A6171C",
            relief="flat",
            padx=20,
            pady=6,
            width=20,
            command=lambda: self.nuevoIngrediente(menu_ingredientes)
        )
        btn_agregar_bottom.grid(row=0, column=0, padx=16)

        btn_regresar_bottom = Button(
            botones_frame,
            text="Regresar",
            font=("Inter", 16),
            fg="#A6171C",
            bg="white",
            relief="flat",
            padx=20,
            pady=6,
            width=20,
            command=lambda: self.regresar(menu_ingredientes)
        )
        btn_regresar_bottom.grid(row=0, column=1, padx=16)


    def nuevoIngrediente(self, nuevo_ingrediente):
        self.borrarPantalla(nuevo_ingrediente)
        nuevo_ingrediente.title("Agregar ingrediente")
        nuevo_ingrediente.geometry("1920x1080")
        nuevo_ingrediente.state("zoomed")

        # =====================================
        # 🔴 Fondo rojo global
        # =====================================
        fondo = Frame(nuevo_ingrediente, bg="#A6171C")
        fondo.pack(fill="both", expand=True)

        # =====================================
        # 📦 Tarjeta blanca con borde dorado
        # =====================================
        container = Frame(
            fondo,
            bg="white",
            width=750,
            height=650,
            highlightbackground="#F1C045",
            highlightthickness=4
        )
        container.place(relx=0.5, rely=0.5, anchor="center")

        # =====================================
        # 🏷 Título
        # =====================================
        lbl_titulo = Label(
            container,
            text="Agregar Ingrediente",
            font=("Orelega One", 42),
            fg="#A6171C",
            bg="white"
        )
        lbl_titulo.pack(pady=(40, 20))

        # =====================================
        # 📋 Contenedor del formulario
        # =====================================
        form_frame = Frame(container, bg="white")
        form_frame.pack(pady=10)

        # =====================================
        # 🧾 Campo: Nombre del ingrediente
        # =====================================
        Label(
            form_frame,
            text="Ingrediente",
            font=("Inter", 20),
            bg="white"
        ).pack(anchor="w", padx=40)

        nomb = StringVar()
        ent_nombre = Entry(
            form_frame,
            font=("Inter", 20),
            bg="#F7F7F7",
            relief="flat",
            textvariable=nomb
        )
        ent_nombre.pack(padx=40, pady=(0, 20), ipady=5, fill="x")

        # =====================================
        # 🧾 Campo: Unidad de medida/pesaje
        # =====================================
        Label(
            form_frame,
            text="Unidad de pesaje/medida",
            font=("Inter", 20),
            bg="white"
        ).pack(anchor="w", padx=40)

        unit = StringVar()
        ent_unit = Entry(
            form_frame,
            font=("Inter", 20),
            bg="#F7F7F7",
            relief="flat",
            textvariable=unit
        )
        ent_unit.pack(padx=40, pady=(0, 25), ipady=5, fill="x")

        # =====================================
        # 💾 Función Guardar
        # =====================================
        def on_save():
            name = ent_nombre.get().strip()
            unit_text = ent_unit.get().strip()

            if not name:
                messagebox.showerror("Error", "El nombre es requerido.")
                return
            if not unit_text:
                messagebox.showerror("Error", "La unidad de medida es requerida.")
                return

            new_id = metodos_ingredientes.Ingredientes_acciones.agregar(name, unit_text)
            if not new_id:
                messagebox.showerror("Error", "No se pudo agregar ingrediente.")
                return

            messagebox.showinfo("Éxito", "Ingrediente agregado correctamente.")
            self.menu_ingrediente(nuevo_ingrediente)

        # =====================================
        # 🎛 Botones inferiores
        # =====================================
        botones_frame = Frame(container, bg="white")
        botones_frame.pack(pady=30)

        btn_save = Button(
            botones_frame,
            text="Guardar",
            font=("Inter", 20),
            bg="#A6171C",
            fg="white",
            activebackground="#8F1318",
            relief="flat",
            width=12,
            command=on_save
        )
        btn_save.grid(row=0, column=0, padx=20)

        btn_cancel = Button(
            botones_frame,
            text="Cancelar",
            font=("Inter", 20),
            bg="#F1C045",
            fg="black",
            activebackground="#D9A935",
            relief="flat",
            width=12,
            command=lambda: self.menu_ingrediente(nuevo_ingrediente)
        )
        btn_cancel.grid(row=0, column=1, padx=20)


    def modificarIngrediente(self, modificar_ingrediente, id_ingredient):
        self.borrarPantalla(modificar_ingrediente)
        modificar_ingrediente.title("Modificar ingrediente")

        try:
            modificar_ingrediente.state("zoomed")
        except:
            pass

        # =====================================================
        # 🔴 Fondo rojo global
        # =====================================================
        fondo = Frame(modificar_ingrediente, bg="#A6171C")
        fondo.pack(fill="both", expand=True)

        # =====================================================
        # 📦 Tarjeta blanca con borde dorado centrada
        # =====================================================
        container = Frame(
            fondo,
            bg="white",
            width=750,
            height=650,
            highlightbackground="#F1C045",
            highlightthickness=4
        )
        container.place(relx=0.5, rely=0.5, anchor="center")

        # =====================================================
        # 📥 Cargar ingrediente
        # =====================================================
        try:
            ingredientes = metodos_ingredientes.Ingredientes_acciones.obtener_ingredientes()
            sel = next((i for i in ingredientes if str(i[0]) == str(id_ingredient)), None)

            if not sel:
                messagebox.showerror("Error", "Ingrediente no encontrado.")
                self.menu_ingrediente(modificar_ingrediente)
                return
            
            _, name, unit = sel

        except Exception:
            messagebox.showerror("Error", "No se pudo cargar ingrediente.")
            self.menu_ingrediente(modificar_ingrediente)
            return

        # =====================================================
        # 🏷 Título
        # =====================================================
        lbl_titulo = Label(
            container,
            text="Modificar Ingrediente",
            font=("Orelega One", 42),
            fg="#A6171C",
            bg="white"
        )
        lbl_titulo.pack(pady=(40, 20))

        # =====================================================
        # 📋 Formulario
        # =====================================================
        form_frame = Frame(container, bg="white")
        form_frame.pack(pady=10)

        # Nombre
        Label(
            form_frame,
            text="Nombre",
            font=("Inter", 20),
            bg="white"
        ).pack(anchor="w", padx=40)

        ent_nombre = Entry(
            form_frame,
            font=("Inter", 20),
            bg="#F7F7F7",
            relief="flat"
        )
        ent_nombre.insert(0, name)
        ent_nombre.pack(padx=40, pady=(0, 20), ipady=5, fill="x")

        # Unidad
        Label(
            form_frame,
            text="Unidad de medida",
            font=("Inter", 20),
            bg="white"
        ).pack(anchor="w", padx=40)

        ent_unit = Entry(
            form_frame,
            font=("Inter", 20),
            bg="#F7F7F7",
            relief="flat"
        )
        ent_unit.insert(0, unit)
        ent_unit.pack(padx=40, pady=(0, 25), ipady=5, fill="x")

        # =====================================================
        # 💾 Acción actualizar
        # =====================================================
        def on_update():
            new_name = ent_nombre.get().strip()
            new_unit = ent_unit.get().strip()

            if not new_name:
                messagebox.showerror("Error", "El nombre es requerido.")
                return
            if not new_unit:
                messagebox.showerror("Error", "La unidad de medida es requerida.")
                return

            res = metodos_ingredientes.Ingredientes_acciones.modificar(new_name, new_unit, id_ingredient)

            if isinstance(res, tuple):
                ok, err = res
            else:
                ok = bool(res)
                err = None

            if ok:
                messagebox.showinfo("Éxito", "Ingrediente modificado correctamente.")
                self.menu_ingrediente(modificar_ingrediente)
            else:
                messagebox.showerror("Error", err if err else "No se pudo modificar el ingrediente.")

        # =====================================================
        # 🎛 Botones inferiores
        # =====================================================
        botones_frame = Frame(container, bg="white")
        botones_frame.pack(pady=30)

        btn_save = Button(
            botones_frame,
            text="Guardar",
            font=("Inter", 20),
            bg="#A6171C",
            fg="white",
            activebackground="#8F1318",
            relief="flat",
            width=12,
            command=on_update
        )
        btn_save.grid(row=0, column=0, padx=20)

        btn_cancel = Button(
            botones_frame,
            text="Cancelar",
            font=("Inter", 20),
            bg="#F1C045",
            fg="black",
            activebackground="#D9A935",
            relief="flat",
            width=12,
            command=lambda: self.menu_ingrediente(modificar_ingrediente)
        )
        btn_cancel.grid(row=0, column=1, padx=20)


    def regresar(self, menu_usuarios):
        menu_principal.interfacesMenu(menu_usuarios)




