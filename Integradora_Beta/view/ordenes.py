from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from view import menu_principal
from model import metodos_productos,metodos_ordenes
from controller import funciones
from datetime import datetime
#Falta eliminar y el modificar de este CRUD
class interfacesOrdenes():
    def __init__(self,ventana_ordenes):
        ventana_ordenes.title("Menu ordenes")
        ventana_ordenes.geometry("1920x1080")
        ventana_ordenes.state("zoomed")
        self.menu_ordenes(ventana_ordenes)

    def borrarPantalla(self,ventana_login):
        for widget in ventana_login.winfo_children():
            widget.destroy()

    def menu_ordenes(self, ventana_ordenes):
        self.borrarPantalla(ventana_ordenes)

        # -------------------------------
        # Fondo general gris claro
        # -------------------------------
        fondo = Frame(ventana_ordenes, bg="#F4F4F4")
        fondo.pack(fill="both", expand=True)

        # -------------------------------
        # Contenedor rojo centrado
        # -------------------------------
        fondo2 = Frame(
            fondo,
            bg="#A6171C",
            highlightbackground="#610E11",
            highlightthickness=4
        )
        fondo2.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.85, relheight=0.85)

        # -------------------------------
        # Título
        # -------------------------------
        titulo_frame = Frame(fondo2, bg="#A6171C")
        titulo_frame.place(relx=0.5, y=50, anchor="center")

        lbl_titulo = Label(
            titulo_frame,
            text="Órdenes",
            font=("Orelega One", 52),
            fg="white",
            bg="#A6171C"
        )
        lbl_titulo.pack()

        # -------------------------------
        # Tarjeta blanca (contenedor tabla)
        # -------------------------------
        tabla_card = Frame(
            fondo2,
            bg="white",
            highlightbackground="#C0C0C0",
            highlightthickness=2
        )
        tabla_card.place(relx=0.5, rely=0.52, anchor="center",
                        relwidth=0.90, relheight=0.70)

        contenedor_tabla = Frame(tabla_card, bg="white")
        contenedor_tabla.pack(fill="both", expand=True, padx=20, pady=20)

        # -------------------------------
        # Estilo Treeview (idéntico a ingredientes)
        # -------------------------------
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

        # -------------------------------
        # Encabezado personalizado
        # -------------------------------
        columns = ('N_orden', 'Cliente', 'Total')

        header_frame = Frame(contenedor_tabla, bg="#A6171C")
        header_frame.pack(fill='x')

        header_cfg = dict(bg="#A6171C", fg="white", font=('Orelega One', 15))

        Label(header_frame, text='No.', anchor='center', **header_cfg).grid(row=0, column=0, sticky='we')
        Label(header_frame, text='Cliente', anchor='w', **header_cfg).grid(row=0, column=1, sticky='we')
        Label(header_frame, text='Total', anchor='center', **header_cfg).grid(row=0, column=2, sticky='we')

        # Proporciones igual estilo ingredientes
        header_frame.columnconfigure(0, weight=10)
        header_frame.columnconfigure(1, weight=55)
        header_frame.columnconfigure(2, weight=25)

        # -------------------------------
        # Treeview como cuerpo
        # -------------------------------
        tabla = ttk.Treeview(
            contenedor_tabla,
            columns=columns,
            show='',
            selectmode='browse'
        )

        tabla.update_idletasks()
        total_width = tabla_card.winfo_width() or 1500

        tabla.column('N_orden', width=int(total_width * 0.10), anchor=CENTER)
        tabla.column('Cliente', width=int(total_width * 0.55), anchor=W)
        tabla.column('Total', width=int(total_width * 0.25), anchor=CENTER)

        vsb = ttk.Scrollbar(contenedor_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=vsb.set)

        tabla.pack(fill=BOTH, expand=True, side=LEFT)
        vsb.pack(side=RIGHT, fill=Y)

        tabla.tag_configure('odd', background='#FFFFFF')
        tabla.tag_configure('even', background='#F8F8F8')

        # -------------------------------
        # Cargar datos
        # -------------------------------
        todas_ordenes = metodos_ordenes.Ordenes_acciones.obtener_ordenes()
        hoy = datetime.now().date()
        ordenes_hoy = []

        for o in todas_ordenes:
            try:
                fecha = o[1]
                fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date() if isinstance(fecha, str) else fecha
                if fecha_obj == hoy:
                    ordenes_hoy.append(o)
            except:
                pass

        self._orders_data = {}

        for i, orden in enumerate(ordenes_hoy, 1):
            id_order, fecha, total, cliente = orden
            tag = 'even' if i % 2 == 0 else 'odd'

            try:
                total_txt = f"${float(total):.2f} MXN"
            except:
                total_txt = str(total)

            tabla.insert('', 'end', values=(i, cliente, total_txt), tags=(tag,), iid=str(id_order))

            self._orders_data[str(id_order)] = orden

        # -------------------------------
        # Botones inferiores estilo ingredientes
        # -------------------------------
        botones_frame = Frame(fondo2, bg="#A6171C")
        botones_frame.place(relx=0.5, rely=0.92, anchor="center")

        def _btn(texto, comando):
            return Button(
                botones_frame,
                text=texto,
                font=("Inter", 16),
                fg="white",
                bg="#A6171C",
                relief="flat",
                padx=16,
                pady=6,
                width=14,   # <<< REDUCIDO PARA QUE QUEPA
                command=comando
            )

        _btn("Agregar orden", lambda: self.nuevaOrden(ventana_ordenes)).grid(row=0, column=0, padx=12)
        _btn("Modificar orden", lambda: self.editarOrden(ventana_ordenes, tabla)).grid(row=0, column=1, padx=12)
        _btn("Eliminar orden", lambda: self.eliminarOrden(ventana_ordenes, tabla)).grid(row=0, column=2, padx=12)
        _btn("Detalladas", lambda: self.ordenes_detalladas(ventana_ordenes)).grid(row=0, column=3, padx=12)

        Button(
            botones_frame,
            text="Regresar",
            font=("Inter", 16),
            fg="#A6171C",
            bg="white",
            relief="flat",
            padx=16,
            pady=6,
            width=14,   # <<< MISMO ANCHO REDUCIDO
            command=lambda: self.regresar(ventana_ordenes)
        ).grid(row=0, column=4, padx=12)
  
    def nuevaOrden(self,nueva_orden):
        self.borrarPantalla(nueva_orden)
        nueva_orden.title("Nueva orden")
        nueva_orden.geometry("1920x1080")
        nueva_orden.state("zoomed")
        nueva_orden.config(bg="#FFFFFF")

        # ===== FONDO GENERAL =====
        fondo = Frame(nueva_orden, bg="#FFFFFF")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        # ===== HEADER =====
        header = Frame(fondo, bg="#A6171C", height=170)
        header.pack(side=TOP, fill=X)

        # ===== NUEVO ESTILO DE BOTONES HEADER =====
        estilo_btn_header = {
            "font": ("Inter", 26, "bold"),
            "fg": "white",
            "bg": "#C4373D",               # 🔴 nuevo color
            "activebackground": "#A32E33",
            "activeforeground": "white",
            "bd": 0,
            "relief": "flat",
            "cursor": "hand2",
            "width": 12,                   # 🔥 más grandes y proporcionados
            "height": 2,
        }

        # ---- Botón Regresar
        btn_regresar = Button(
            header,
            text="Regresar",
            command=lambda: self.menu_ordenes(nueva_orden),
            **estilo_btn_header
        )
        btn_regresar.pack(padx=25, pady=25, side=LEFT)

        # ---- Botón Alimentos
        btn_alimentos = Button(
            header,
            text="Alimentos",
            command=lambda: self.botonesAlimentos(contenedor_botones_Ordens, self.pedido_widget),
            **estilo_btn_header
        )
        btn_alimentos.pack(padx=25, pady=25, side=LEFT, expand=True)

        # ---- Botón Especiales
        btn_especiales = Button(
            header,
            text="Especiales",
            command=lambda: self.botonesEspeciales(contenedor_botones_Ordens, self.pedido_widget),
            **estilo_btn_header
        )
        btn_especiales.pack(padx=25, pady=25, side=LEFT, expand=True)

        # ---- Botón Bebidas
        btn_bebidas = Button(
            header,
            text="Bebidas",
            command=lambda: self.botonesBebidas(contenedor_botones_Ordens, self.pedido_widget),
            **estilo_btn_header
        )
        btn_bebidas.pack(padx=25, pady=25, side=LEFT, expand=True)

        # ---- Botón Confirmar
        btn_confirmar = Button(
            header,
            text="Confirmar",
            command=lambda: self.confirmar_pedido(),
            **estilo_btn_header
        )
        btn_confirmar.pack(padx=25, pady=25, side=LEFT, expand=True)

        # ===== CONTENEDOR PRODUCTOS =====
        contenedor_botones_Ordens = Frame(fondo, bg="#D6D0C5")
        contenedor_botones_Ordens.pack(pady=10, padx=10, fill="both", expand=True, side=LEFT)

        # ===== PANEL DE ORDEN =====
        contenedor_orden = Frame(
            fondo,
            bg="#EAEAE9",
            width=350,
            highlightbackground="#A6171C",
            highlightthickness=3
        )
        contenedor_orden.pack_propagate(False)
        contenedor_orden.pack(pady=10, padx=10, fill="y", side=RIGHT)

        Label(
            contenedor_orden,
            bg="#EAEAE9",
            fg="#A6171C",
            font=("Inter", 22, "bold"),
            text="Orden"
        ).pack(pady=10)

        Label(
            contenedor_orden,
            bg="#EAEAE9",
            font=("Inter", 14),
            text="Nombre del Cliente:"
        ).pack(pady=5)

        self.nombre_entry = Entry(
            contenedor_orden,
            bg="white",
            fg="#333",
            font=("Inter", 14),
            relief="flat"
        )
        self.nombre_entry.pack(fill="x", padx=10, pady=5)

        # Pedido (bloqueado)
        self.pedido_widget = Text(
            contenedor_orden,
            background="white",
            pady=10,
            font=("Inter", 14),
            relief="flat",
        )
        try:
            self.pedido_widget.config(state=DISABLED)
        except Exception:
            pass

        self.pedido_widget.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Total
        self.lbl_total_pedido = Label(
            contenedor_orden,
            text="Total: $0.00",
            font=("Inter", 18, 'bold'),
            bg="#EAEAE9",
            fg="#A6171C"
        )
        self.lbl_total_pedido.pack(pady=10)

        # Lógica intacta
        self._order_items = {}
        self._editing_order_id = None



    def editarOrden(self, ventana, tabla):
        """Abre la pantalla de nueva orden pero cargando los datos de la orden seleccionada para editarla."""
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione una orden para modificar.")
            return

        id_orden = seleccionado[0]
        # abrir la pantalla de nueva orden
        self.nuevaOrden(ventana)
        try:
            # asignar id de edición
            self._editing_order_id = int(id_orden)
        except Exception:
            self._editing_order_id = None

        # cargar nombre del cliente si está en el mapa local
        orden_data = getattr(self, '_orders_data', {}).get(str(id_orden))
        if orden_data:
            try:
                cliente = orden_data[3]
                self.nombre_entry.delete(0, END)
                self.nombre_entry.insert(0, cliente)
            except Exception:
                pass
        # Borrar cualquier pedido cargado y dejar el empleado construir desde cero
        self._order_items = {}
        try:
            self.pedido_widget.delete("1.0", END)
        except Exception:
            pass

    def eliminarOrden(self, ventana, tabla):
        """Elimina la orden seleccionada en la tabla tras confirmación."""
        seleccionado = tabla.selection()
        if not seleccionado:
            messagebox.showwarning("Atención", "Seleccione una orden para eliminar.")
            return

        id_orden = seleccionado[0]
        confirmar = messagebox.askyesno("Confirmar eliminación", f"¿Eliminar la orden {id_orden}? Esta acción no se puede deshacer.")
        if not confirmar:
            return

        try:
            ok = metodos_ordenes.Ordenes_acciones.eliminar_orden(id_orden)
            if ok:
                try:
                    tabla.delete(id_orden)
                except Exception:
                    # fallback si el iid no coincide exactamente
                    for iid in seleccionado:
                        try:
                            tabla.delete(iid)
                        except Exception:
                            pass
                # remover del cache local si existe
                if hasattr(self, '_orders_data') and str(id_orden) in self._orders_data:
                    del self._orders_data[str(id_orden)]
                messagebox.showinfo("Éxito", "Orden eliminada correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo eliminar la orden. Revisa la consola para más detalles.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar la orden: {e}")

    def botonesAlimentos(self,contenedor_botones_Ordens,pedido):
            self.borrarPantalla(contenedor_botones_Ordens)
            contenedor_botones_Ordens.config(bg="#FFFFFF")
            Ordens=metodos_productos.Productos_acciones.obtener_productos()
            maximo=3
            for c in range(maximo):
                contenedor_botones_Ordens.grid_columnconfigure(c, weight=1)
            filas=(len(Ordens)+maximo-1)//maximo
            for r in range(filas):
                contenedor_botones_Ordens.grid_rowconfigure(r, weight=1)
            for i,Orden in enumerate(Ordens):
                fila=i//maximo
                columna=i%maximo
                # al presionar, agregar Orden al pedido (maneja cantidades y formato)
                boton=Button(contenedor_botones_Ordens, text=f"{Orden[1]}",     
                            font=("Inter", 22, "bold"),
                            fg="white",
                            bg="#A6171C",
                            activebackground="#8F1318",
                            activeforeground="white",
                            relief="flat",
                            bd=0,
                            cursor="hand2",
                            command=lambda p=Orden: self._add_to_pedido(pedido, p))
                def on_enter(e, b=boton):
                    b.configure(bg="#8F1318")

                def on_leave(e, b=boton):
                    b.configure(bg="#A6171C")

                boton.bind("<Enter>", on_enter)
                boton.bind("<Leave>", on_leave)
                boton.grid(row=fila,column=columna, pady=5, padx=5, sticky="NSEW")

    def botonesEspeciales(self,contenedor_botones_Ordens,pedido):
            self.borrarPantalla(contenedor_botones_Ordens)
            contenedor_botones_Ordens.config(bg="#FFFFFF")
            Ordens=metodos_productos.Productos_acciones.obtener_especiales()
            maximo=3
            for c in range(maximo):
                contenedor_botones_Ordens.grid_columnconfigure(c, weight=1)
            filas=(len(Ordens)+maximo-1)//maximo
            for r in range(filas):
                contenedor_botones_Ordens.grid_rowconfigure(r, weight=1)
            
            for i,Orden in enumerate(Ordens):
                fila=i//maximo
                columna=i%maximo
                boton=Button(contenedor_botones_Ordens, text=f"{Orden[1]}", 
                            fg="white",
                            font=("Inter", 22, "bold"),
                            bg="#A6171C",
                            activebackground="#8F1318",
                            activeforeground="white",
                            relief="flat",
                            bd=0,
                            cursor="hand2",
                            command=lambda e=Orden: self._add_to_pedido(pedido, e))
                def on_enter(e, b=boton):
                    b.configure(bg="#8F1318")

                def on_leave(e, b=boton):
                    b.configure(bg="#A6171C")

                boton.bind("<Enter>", on_enter)
                boton.bind("<Leave>", on_leave)
                boton.grid(row=fila,column=columna, pady=5, padx=5, sticky="NSEW")

    def botonesBebidas(self,contenedor_botones_Ordens,pedido):
            self.borrarPantalla(contenedor_botones_Ordens)
            contenedor_botones_Ordens.config(bg="#FFFFFF")
            Ordens=metodos_productos.Productos_acciones.obtener_bebidas()
            maximo=3
            for c in range(maximo):
                contenedor_botones_Ordens.grid_columnconfigure(c, weight=1)
            filas=(len(Ordens)+maximo-1)//maximo
            for r in range(filas):
                contenedor_botones_Ordens.grid_rowconfigure(r, weight=1)
            
            for i,Orden in enumerate(Ordens):
                fila=i//maximo
                columna=i%maximo
                boton=Button(contenedor_botones_Ordens, text=f"{Orden[1]}",
                            fg="white",
                            font=("Inter", 22, "bold"),
                            bg="#A6171C",
                            activebackground="#8F1318",
                            activeforeground="white",
                            relief="flat",
                            bd=0,
                            cursor="hand2",
                            command=lambda b=Orden: self._add_to_pedido(pedido, b))
                def on_enter(e, b=boton):
                    b.configure(bg="#8F1318")

                def on_leave(e, b=boton):
                    b.configure(bg="#A6171C")

                boton.bind("<Enter>", on_enter)
                boton.bind("<Leave>", on_leave)
                boton.grid(row=fila,column=columna, pady=5, padx=5, sticky="NSEW")

    def _add_to_pedido(self, pedido, Orden):
            """Agregar Orden al Text `pedido` usando un diccionario interno.
            Mantiene cantidades por `id_product` y re-renderiza el `Text` sin perder otras entradas.
            """
            try:
                prod_id = Orden[0]
                nombre = str(Orden[1])
                precio_unit = float(Orden[3])
            except Exception:
                # fallback si la tupla tiene estructura desconocida
                prod_id = str(Orden)
                nombre = str(Orden)
                precio_unit = 0.0

            # usar id como clave si está disponible
            key = prod_id
            entry = self._order_items.get(key)
            if entry is None:
                # nueva entrada
                self._order_items[key] = {"name": nombre, "qty": 1, "unit": precio_unit}
            else:
                # incrementar cantidad
                entry["qty"] += 1

            # re-renderizar el pedido desde el dict (preserva todo lo agregado)
            self._render_pedido(pedido)

    def _render_pedido(self, pedido):
            """Escribe en el widget Text `pedido` todas las líneas desde `self._order_items`.
            Formato: 'Nx Nombre -- $TT.TT'
            """
            lines = []
            total_sum = 0.0
            for key, v in self._order_items.items():
                try:
                    total = v["qty"] * float(v["unit"])
                except Exception:
                    total = 0.0
                total_sum += total
                lines.append(f"{v['qty']}x {v['name']} -- ${total:.2f}")

            # actualizar el text: habilitar temporalmente, escribir y deshabilitar
            try:
                pedido.config(state=NORMAL)
                pedido.delete("1.0", END)
                if lines:
                    pedido.insert(END, "\n".join(lines) + "\n")
                pedido.config(state=DISABLED)
            except Exception:
                # fallback directo
                try:
                    pedido.delete("1.0", END)
                    if lines:
                        pedido.insert(END, "\n".join(lines) + "\n")
                except Exception:
                    pass

            # actualizar label de total si existe
            try:
                self.lbl_total_pedido.config(text=f"Total: ${total_sum:.2f}")
            except Exception:
                pass

    def confirmar_pedido(self):
            """Calcula total, valida cliente, inserta orden y sus detalles en la BD."""
            if not self._order_items:
                messagebox.showwarning("Atención", "No hay Ordens en el pedido.")
                return

            # calcular total
            total = 0.0
            for v in self._order_items.values():
                try:
                    total += v["qty"] * float(v["unit"])
                except Exception:
                    pass

            cliente = self.nombre_entry.get().strip()
            if not cliente:
                messagebox.showwarning("Atención", "Ingrese el nombre del cliente.")
                return

            # si estamos editando una orden existente -> actualizar
            editing_id = getattr(self, '_editing_order_id', None)
            if editing_id:
                ok_upd = metodos_ordenes.Ordenes_acciones.actualizar_orden(editing_id, total, cliente)
                ok_det = metodos_ordenes.Ordenes_acciones.reemplazar_detalles(editing_id, self._order_items)
                if ok_upd:
                    messagebox.showinfo("Éxito", f"Orden {editing_id} actualizada correctamente.")
                else:
                    messagebox.showerror("Error", "No se pudo actualizar la orden en la base de datos.")
                # limpiar bandera de edición
                self._editing_order_id = None
            else:
                # insertar orden nuevo
                order_id = metodos_ordenes.Ordenes_acciones.agregar(total, cliente)
                if not order_id:
                    messagebox.showerror("Error", "No se pudo crear la orden en la base de datos.")
                    return

                # insertar detalles
                ok = metodos_ordenes.Ordenes_acciones.agregar_detalles(order_id, self._order_items)
                if not ok:
                    messagebox.showwarning("Advertencia", f"Orden creada (id {order_id}) pero no se pudieron guardar todos los detalles.")
                else:
                    messagebox.showinfo("Éxito", f"Orden creada correctamente. ID: {order_id}")

            # limpiar vista
            self._order_items = {}
            try:
                self.pedido_widget.delete("1.0", END)
                self.nombre_entry.delete(0, END)
            except Exception:
                pass

    def regresar(self,menu_usuarios):
        menu_principal.interfacesMenu(menu_usuarios)
    
    def ordenes_detalladas(self, ventana_ordenes):
        """Muestra las órdenes detalladas con selector de fecha."""
        self.borrarPantalla(ventana_ordenes)
        ventana_ordenes.title("Órdenes Detalladas")
        ventana_ordenes.geometry("1920x1080")
        ventana_ordenes.state("zoomed")

        # -------------------------------------------------------------
        # FONDO GENERAL (gris claro)
        # -------------------------------------------------------------
        fondo = Frame(ventana_ordenes, bg="#F4F4F4")
        fondo.pack(fill="both", expand=True)

        # -------------------------------------------------------------
        # CONTENEDOR ROJO PRINCIPAL (ESTILO menu_ordenes)
        # -------------------------------------------------------------
        fondo_rojo = Frame(
            fondo,
            bg="#A6171C",
            highlightbackground="#610E11",
            highlightthickness=4
        )
        fondo_rojo.place(relx=0.5, rely=0.5, anchor="center",
                        relwidth=0.88, relheight=0.88)

        # -------------------------------------------------------------
        # TÍTULO
        # -------------------------------------------------------------
        titulo_frame = Frame(fondo_rojo, bg="#A6171C")
        titulo_frame.place(relx=0.5, rely=0.08, anchor="center")

        titulo = Label(
            titulo_frame,
            text="Órdenes Detalladas",
            font=("Orelega One", 48),
            fg="white",
            bg="#A6171C"
        )
        titulo.pack()

        # -------------------------------------------------------------
        # HEADER FECHA + BOTÓN BUSCAR (alineado estilo menú)
        # -------------------------------------------------------------
        header = Frame(fondo_rojo, bg="#A6171C")
        header.place(relx=0.5, rely=0.18, anchor="center")

        lbl_fecha = Label(header, text="Seleccionar fecha:",
                        font=("Inter", 18), fg="white", bg="#A6171C")
        lbl_fecha.grid(row=0, column=0, padx=10)

        # Año
        ano_actual = datetime.now().year
        lbl_ano = Label(header, text="Año:", font=("Inter", 14),
                        fg="white", bg="#A6171C")
        lbl_ano.grid(row=0, column=1, padx=5)
        spinbox_ano = Spinbox(header, from_=ano_actual-5, to=ano_actual+5,
                            width=5, font=("Inter", 14), justify=CENTER)
        spinbox_ano.delete(0, END)
        spinbox_ano.insert(0, str(ano_actual))
        spinbox_ano.grid(row=0, column=2, padx=5)

        # Mes
        mes_actual = datetime.now().month
        lbl_mes = Label(header, text="Mes:", font=("Inter", 14),
                        fg="white", bg="#A6171C")
        lbl_mes.grid(row=0, column=3, padx=5)
        spinbox_mes = Spinbox(header, from_=1, to=12, width=3,
                            font=("Inter", 14), justify=CENTER)
        spinbox_mes.delete(0, END)
        spinbox_mes.insert(0, str(mes_actual))
        spinbox_mes.grid(row=0, column=4, padx=5)

        # Día
        dia_actual = datetime.now().day
        lbl_dia = Label(header, text="Día:", font=("Inter", 14),
                        fg="white", bg="#A6171C")
        lbl_dia.grid(row=0, column=5, padx=5)
        spinbox_dia = Spinbox(header, from_=1, to=31, width=3,
                            font=("Inter", 14), justify=CENTER)
        spinbox_dia.delete(0, END)
        spinbox_dia.insert(0, str(dia_actual))
        spinbox_dia.grid(row=0, column=6, padx=5)

        # BOTÓN BUSCAR (estilo menú)
        btn_buscar = Button(
            header, text="Buscar", font=("Inter", 14),
            fg="#A6171C",
            bg="white",
            relief="flat",
            padx=10,
            pady=4,
            width=10,
            command=lambda: cargar_ordenes_por_fecha()
        )
        btn_buscar.grid(row=0, column=7, padx=12)

        # -------------------------------------------------------------
        # TARJETA BLANCA PARA AMBAS TABLAS
        # -------------------------------------------------------------
        card_tablas = Frame(
            fondo_rojo,
            bg="white",
            highlightbackground="#C0C0C0",
            highlightthickness=2
        )
        card_tablas.place(relx=0.5, rely=0.59, anchor="center",
                        relwidth=0.93, relheight=0.68)

        # Contenedor interior
        cont_tablas = Frame(card_tablas, bg="white")
        cont_tablas.pack(fill="both", expand=True, padx=25, pady=25)

        # -------------------------------------------------------------
        # TREEVIEW ESTILO
        # -------------------------------------------------------------
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Treeview', foreground='black', rowheight=26, font=('Inter', 13))
        style.configure('Treeview.Heading', background='#A6171C',
                        foreground='white', font=('Orelega One', 14))
        style.map('Treeview', background=[('selected', '#F1C045')],
                foreground=[('selected', 'black')])

        # -------------------------------------------------------------
        # TABLA IZQUIERDA (40%)
        # -------------------------------------------------------------
        frame_ordenes = Frame(cont_tablas, bg="white")
        frame_ordenes.pack(side=LEFT, fill="both", expand=True)

        lbl_ordenes = Label(frame_ordenes, text="Órdenes:", fg="#A6171C",
                            bg="white", font=("Inter", 16))
        lbl_ordenes.pack(anchor="w", pady=(0, 8))

        columns_ordenes = ('N_orden', 'ID', 'Fecha', 'Cliente', 'Total')
        tabla_ordenes = ttk.Treeview(
            frame_ordenes, columns=columns_ordenes,
            show='headings', selectmode='browse', height=20
        )

        tabla_ordenes.heading('N_orden', text='N.')
        tabla_ordenes.heading('ID', text='ID')
        tabla_ordenes.heading('Fecha', text='Fecha')
        tabla_ordenes.heading('Cliente', text='Cliente')
        tabla_ordenes.heading('Total', text='Total')

        tabla_ordenes.column('N_orden', width=70, anchor=CENTER)
        tabla_ordenes.column('ID', width=60, anchor=CENTER)
        tabla_ordenes.column('Fecha', width=100, anchor=CENTER)
        tabla_ordenes.column('Cliente', width=160, anchor=W)
        tabla_ordenes.column('Total', width=100, anchor=CENTER)

        vsb1 = ttk.Scrollbar(frame_ordenes, orient="vertical",
                            command=tabla_ordenes.yview)
        tabla_ordenes.configure(yscrollcommand=vsb1.set)

        tabla_ordenes.pack(side=LEFT, fill=BOTH, expand=True)
        vsb1.pack(side=LEFT, fill=Y)

        # -------------------------------------------------------------
        # TABLA DERECHA (60%)
        # -------------------------------------------------------------
        frame_detalles = Frame(cont_tablas, bg="white")
        frame_detalles.pack(side=RIGHT, fill="both", expand=True, padx=(20, 0))

        lbl_detalles = Label(frame_detalles, text="Detalles:",
                            fg="#A6171C", bg="white", font=("Inter", 16))
        lbl_detalles.pack(anchor="w", pady=(0, 8))

        columns_detalles = ('Cantidad', 'Producto', 'Precio Unit.', 'Subtotal')
        tabla_detalles = ttk.Treeview(
            frame_detalles,
            columns=columns_detalles,
            show='headings', height=20
        )

        tabla_detalles.heading('Cantidad', text='Cant.')
        tabla_detalles.heading('Producto', text='Producto')
        tabla_detalles.heading('Precio Unit.', text='Precio U.')
        tabla_detalles.heading('Subtotal', text='Subtotal')

        tabla_detalles.column('Cantidad', width=80, anchor=CENTER)
        tabla_detalles.column('Producto', width=260, anchor=W)
        tabla_detalles.column('Precio Unit.', width=120, anchor=CENTER)
        tabla_detalles.column('Subtotal', width=120, anchor=CENTER)

        vsb2 = ttk.Scrollbar(frame_detalles, orient="vertical",
                            command=tabla_detalles.yview)
        tabla_detalles.configure(yscrollcommand=vsb2.set)

        tabla_detalles.pack(side=LEFT, fill=BOTH, expand=True)
        vsb2.pack(side=LEFT, fill=Y)

        # -------------------------------------------------------------
        # BOTÓN REGRESAR (REUBICADO Y REDIMENSIONADO)
        # -------------------------------------------------------------
        botones_frame = Frame(fondo_rojo, bg="#A6171C")
        botones_frame.place(relx=0.5, rely=0.965, anchor="center")

        Button(
            botones_frame,
            text="Regresar",
            font=("Inter", 14),
            fg="#A6171C",
            bg="white",
            relief="flat",
            padx=10,
            pady=4,
            width=10,
            command=lambda: self.menu_ordenes(ventana_ordenes)
        ).pack()


        # -------------------------------------------------------------
        # LÓGICA ORIGINAL (NO MODIFICADA)
        # -------------------------------------------------------------
        def cargar_ordenes_por_fecha():
            try:
                ano = int(spinbox_ano.get())
                mes = int(spinbox_mes.get())
                dia = int(spinbox_dia.get())
                fecha = datetime(ano, mes, dia).date()

                # Limpiar ambas tablas
                for i in tabla_ordenes.get_children():
                    tabla_ordenes.delete(i)
                for i in tabla_detalles.get_children():
                    tabla_detalles.delete(i)

                ordenes = metodos_ordenes.Ordenes_acciones.obtener_ordenes_por_fecha(fecha)

                if not ordenes:
                    messagebox.showinfo("Información", f"No hay órdenes para {fecha}")
                    return

                for num, orden in enumerate(ordenes, 1):
                    id_orden, fecha_orden, total, cliente = orden
                    try:
                        total_text = f"${float(total):.2f}"
                    except:
                        total_text = str(total)

                    tag = 'even' if num % 2 == 0 else 'odd'
                    tabla_ordenes.insert('', 'end',
                                        values=(num, id_orden, fecha_orden, cliente, total_text),
                                        tags=(tag,), iid=id_orden)

            except:
                messagebox.showerror("Error", "Por favor ingrese una fecha válida")

        def mostrar_detalles_orden(event=None):
            seleccionado = tabla_ordenes.selection()
            if not seleccionado:
                return

            id_orden = seleccionado[0]

            for i in tabla_detalles.get_children():
                tabla_detalles.delete(i)

            try:
                detalles = metodos_ordenes.Ordenes_acciones.obtener_detalles_orden(id_orden)

                if not detalles:
                    messagebox.showinfo("Información", "Esta orden no tiene detalles registrados")
                    return

                for n, detalle in enumerate(detalles, 1):
                    cantidad = detalle[0]
                    producto = detalle[2] if len(detalle) > 2 else detalle[1]
                    precio = detalle[3] if len(detalle) > 3 else 0
                    subtotal = detalle[4] if len(detalle) > 4 else 0

                    try:
                        precio_t = f"${float(precio):.2f}"
                        subt_t = f"${float(subtotal):.2f}"
                    except:
                        precio_t = str(precio)
                        subt_t = str(subtotal)

                    tag = "even" if n % 2 == 0 else "odd"
                    tabla_detalles.insert('', 'end',
                                        values=(cantidad, producto, precio_t, subt_t),
                                        tags=(tag,))
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar detalles: {e}")

        tabla_ordenes.bind("<<TreeviewSelect>>", mostrar_detalles_orden)

        # Cargar fecha actual al abrir
        cargar_ordenes_por_fecha()



    
