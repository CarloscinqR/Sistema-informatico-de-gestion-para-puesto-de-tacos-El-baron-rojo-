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

    def menu_ordenes(self,ventana_ordenes):
        self.borrarPantalla(ventana_ordenes)
        fondo=Frame(ventana_ordenes, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        lbl_titulo=Label(fondo2, text="Ordenes",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
        lbl_titulo.pack(padx=20, pady=20)

        contenedor_tabla=Frame(fondo2, width=2000, height=790)
        contenedor_tabla.pack_propagate(False)
        contenedor_tabla.pack(side=LEFT, padx=40, pady=20)

        # --- Tabla de Ordens (Treeview) ---
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

        columns = ('N_orden', 'Cliente', 'Total')
        tabla = ttk.Treeview(contenedor_tabla, columns=columns, show='headings', selectmode='browse')
        tabla.heading('N_orden', text='N. orden')
        tabla.heading('Cliente', text='Cliente')
        tabla.heading('Total', text='Total')
        tabla.column('N_orden', width=120, anchor=CENTER)
        tabla.column('Cliente', width=300, anchor=W)
        tabla.column('Total', width=200, anchor=CENTER)

        vsb = ttk.Scrollbar(contenedor_tabla, orient="vertical")
        vsb.config(command=tabla.yview)
        tabla.configure(yscrollcommand=vsb.set)
        tabla.pack(fill=BOTH, expand=True, padx=20, pady=10)
        vsb.pack(side=RIGHT, fill=Y, pady=10, padx=(0,20))

        # Estilo de filas alternadas
        tabla.tag_configure('odd', background='#FFFFFF')
        tabla.tag_configure('even', background='#F6F0E8')

        # Cargar datos desde la base de datos usando el modelo - Solo órdenes del día actual
        todas_ordenes = metodos_ordenes.Ordenes_acciones.obtener_ordenes()
        hoy = datetime.now().date()
        ordenes_hoy = []
        
        for orden in todas_ordenes:
            try:
                # orden[1] es la fecha (date)
                fecha_orden = orden[1] if isinstance(orden[1], str) else str(orden[1])
                # Convertir a date para comparación
                if isinstance(orden[1], str):
                    fecha_obj = datetime.strptime(fecha_orden, '%Y-%m-%d').date()
                else:
                    fecha_obj = orden[1]
                
                if fecha_obj == hoy:
                    ordenes_hoy.append(orden)
            except Exception:
                pass
        
        # contenedor para guardar referencias a botones por fila
        _row_buttons = {}

        # guardar mapa de ordenes por id para facilitar edición
        self._orders_data = {}
        for contador, orden in enumerate(ordenes_hoy, 1):
            # orden es una tupla (id_order, date, total, costumer_name)
            total = orden[2]
            cliente = orden[3]
            try:
                total_text = f"${float(total):.2f} MXN"
            except Exception:
                total_text = str(total)
            tag = 'even' if contador % 2 == 0 else 'odd'
            # Insertar fila en la tabla con: N. orden, Cliente, Total
            id_order = orden[0]
            tabla.insert('', 'end', values=(contador, cliente, total_text), tags=(tag,), iid=str(id_order))
            # guardar para edición
            self._orders_data[str(id_order)] = orden

        # Forzar dibujo
        ventana_ordenes.update_idletasks()

        # Frame para los botones
        frame_botones = Frame(contenedor_tabla, bg="#D6D0C5")
        frame_botones.pack(padx=20, pady=10, fill="x")

        btn_agregarOrden=Button(frame_botones, text="Agregar orden", font=("Inter", 18), fg="#A6171C", bg="#F1C045", command=lambda: self.nuevaOrden(ventana_ordenes))
        btn_agregarOrden.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        btn_modificarOrden=Button(frame_botones, text="Modificar orden", font=("Inter", 18), fg="#A6171C", bg="#F1C045", command=lambda: self.editarOrden(ventana_ordenes, tabla))
        btn_modificarOrden.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        btn_eliminarOrden=Button(frame_botones, text="Eliminar orden", font=("Inter", 18), fg="#A6171C", bg="#F1C045", command=lambda: self.eliminarOrden(ventana_ordenes, tabla))
        btn_eliminarOrden.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        btn_verDetalladas=Button(frame_botones, text="Ver ordenes detalladas", font=("Inter", 18), fg="#A6171C", bg="#F1C045", command=lambda: self.ordenes_detalladas(ventana_ordenes))
        btn_verDetalladas.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        btn_regresar=Button(frame_botones, text="Regresar", font=("Inter", 18), fg="#A6171C", bg="#F1C045", command=lambda: self.regresar(ventana_ordenes))
        btn_regresar.grid(row=0, column=4, padx=5, pady=5, sticky="ew")

        # Configurar pesos iguales para todas las columnas
        for i in range(5):
            frame_botones.grid_columnconfigure(i, weight=1)
    
    def nuevaOrden(self,nueva_orden):
        self.borrarPantalla(nueva_orden)
        nueva_orden.title("Nueva orden")
        nueva_orden.geometry("1920x1080")
        nueva_orden.state("zoomed")

        fondo=Frame(nueva_orden, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        header=Frame(fondo, bg="#A6171C", height=180)
        header.pack(side=TOP, fill=X)

        btn_regresar=Button(header, text="Regresar", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: self.menu_ordenes(nueva_orden))
        btn_regresar.pack(padx=20, pady=10, fill="x", side=LEFT, expand=True)
        
        btn_alimentos=Button(header, text="Alimentos", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda:self.botonesAlimentos(contenedor_botones_Ordens,self.pedido_widget))
        btn_alimentos.pack(padx=20, pady=10, fill="x", side=LEFT, expand=True)
        
        btn_especiales=Button(header, text="Especiales", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda:self.botonesEspeciales(contenedor_botones_Ordens,self.pedido_widget))
        btn_especiales.pack(padx=20, pady=10, fill="x", side=LEFT, expand=True)

        btn_bebidas=Button(header, text="Bebidas", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda:self.botonesBebidas(contenedor_botones_Ordens,self.pedido_widget))
        btn_bebidas.pack(padx=20, pady=10, fill="x", side=LEFT, expand=True)
        
        btn_confirmar=Button(header, text="Confirmar", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: self.confirmar_pedido())
        btn_confirmar.pack(padx=20, pady=10, fill="x", side=LEFT, expand=True)

        contenedor_botones_Ordens=Frame(fondo, bg="#D6D0C5")
        contenedor_botones_Ordens.pack(pady=10, padx=10, fill="both", expand=True, side=LEFT)

        #Falta que funcione el registro de ordenes
        contenedor_orden=Frame(fondo,bg="#EAEAE9",width=300)
        contenedor_orden.pack_propagate(False)
        contenedor_orden.pack(pady=10, padx=10, fill="y", side=RIGHT)

        titulo_orden=Label(contenedor_orden, bg="#EAEAE9", font=46, text="Orden:")
        titulo_orden.pack(pady=5)
        nombre_comprador=Label(contenedor_orden, bg="#EAEAE9", font=5, text="Nombre del Cliente:")
        nombre_comprador.pack(pady=5)
        self.nombre_entry=Entry(contenedor_orden, bg="#EAEAE9")
        self.nombre_entry.pack(fill="y", padx=5, pady=5)
        # Pedido (no editable por el empleado; se actualiza desde los botones)
        self.pedido_widget=Text(contenedor_orden, background="white",pady=10, font=("Inter", 14))
        # deshabilitar edición directa
        try:
            self.pedido_widget.config(state=DISABLED)
        except Exception:
            pass
        self.pedido_widget.pack(fill=BOTH, expand=True)
        # Label para mostrar el total en tiempo real
        self.lbl_total_pedido = Label(contenedor_orden, text="Total: $0.00", font=("Inter", 14, 'bold'), bg="#EAEAE9", fg="#A6171C")
        self.lbl_total_pedido.pack(pady=6)
        # estructura interna para llevar cantidades por id de Orden
        self._order_items = {}
        # indicador de edición: None => crear nueva, int => editar orden existente
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
                boton=Button(contenedor_botones_Ordens, text=f"{Orden[1]}", relief="solid", font=("Inter", 22), command=lambda p=Orden: self._add_to_pedido(pedido, p))
                boton.grid(row=fila,column=columna, pady=5, padx=5, sticky="NSEW")

    def botonesEspeciales(self,contenedor_botones_Ordens,pedido):
            self.borrarPantalla(contenedor_botones_Ordens)
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
                boton=Button(contenedor_botones_Ordens, text=f"{Orden[1]}", relief="solid", font=("Inter", 22), command=lambda e=Orden: self._add_to_pedido(pedido, e))
                boton.grid(row=fila,column=columna, pady=5, padx=5, sticky="NSEW")

    def botonesBebidas(self,contenedor_botones_Ordens,pedido):
            self.borrarPantalla(contenedor_botones_Ordens)
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
                boton=Button(contenedor_botones_Ordens, text=f"{Orden[1]}", relief="solid", font=("Inter", 22), command=lambda b=Orden: self._add_to_pedido(pedido, b))
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
        
        # Frame principal con grid
        fondo = Frame(ventana_ordenes, bg="#D6D0C5")
        fondo.pack(fill="both", expand=True)
        
        # Header con selector de fecha
        header = Frame(fondo, bg="#A6171C", height=120)
        header.pack(side=TOP, fill=X, padx=50, pady=10)
        
        titulo = Label(header, text="Órdenes Detalladas", font=("Orelega One", 36), fg="#F1C045", bg="#A6171C")
        titulo.pack(pady=5)
        
        # Selector de fecha
        frame_fecha = Frame(header, bg="#A6171C")
        frame_fecha.pack(pady=5)
        
        lbl_fecha = Label(frame_fecha, text="Seleccionar fecha:", font=("Inter", 14), fg="#F1C045", bg="#A6171C")
        lbl_fecha.pack(side=LEFT, padx=10)
        
        # Spinbox para año
        lbl_ano = Label(frame_fecha, text="Año:", font=("Inter", 12), fg="#F1C045", bg="#A6171C")
        lbl_ano.pack(side=LEFT, padx=5)
        ano_actual = datetime.now().year
        spinbox_ano = Spinbox(frame_fecha, from_=ano_actual-5, to=ano_actual+5, width=5, font=("Inter", 12), justify=CENTER)
        spinbox_ano.delete(0, END)
        spinbox_ano.insert(0, str(ano_actual))
        spinbox_ano.pack(side=LEFT, padx=5)
        
        # Spinbox para mes
        lbl_mes = Label(frame_fecha, text="Mes:", font=("Inter", 12), fg="#F1C045", bg="#A6171C")
        lbl_mes.pack(side=LEFT, padx=5)
        mes_actual = datetime.now().month
        spinbox_mes = Spinbox(frame_fecha, from_=1, to=12, width=3, font=("Inter", 12), justify=CENTER)
        spinbox_mes.delete(0, END)
        spinbox_mes.insert(0, str(mes_actual))
        spinbox_mes.pack(side=LEFT, padx=5)
        
        # Spinbox para día
        lbl_dia = Label(frame_fecha, text="Día:", font=("Inter", 12), fg="#F1C045", bg="#A6171C")
        lbl_dia.pack(side=LEFT, padx=5)
        dia_actual = datetime.now().day
        spinbox_dia = Spinbox(frame_fecha, from_=1, to=31, width=3, font=("Inter", 12), justify=CENTER)
        spinbox_dia.delete(0, END)
        spinbox_dia.insert(0, str(dia_actual))
        spinbox_dia.pack(side=LEFT, padx=5)
        
        # Frame contenedor principal con dos columnas
        contenedor_principal = Frame(fondo, bg="#D6D0C5")
        contenedor_principal.pack(pady=10, padx=50, fill="both", expand=True)
        
        # ========== TABLA DE ÓRDENES (IZQUIERDA) ==========
        frame_ordenes_titulo = Frame(contenedor_principal, bg="#D6D0C5")
        frame_ordenes_titulo.pack(side=LEFT, fill="x", expand=False, padx=(0, 10))
        
        lbl_ordenes = Label(frame_ordenes_titulo, text="Órdenes del día:", font=("Inter", 16), fg="#A6171C", bg="#D6D0C5")
        lbl_ordenes.pack()
        
        # Tabla de órdenes
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Treeview', foreground='black', rowheight=25, font=('Inter', 12))
        style.configure('Treeview.Heading', background='#A6171C', foreground='#F1C045', font=('Orelega One', 13))
        style.map('Treeview', background=[('selected', '#F1C045')], foreground=[('selected', 'black')])
        
        columns_ordenes = ('N_orden', 'ID', 'Fecha', 'Cliente', 'Total')
        tabla_ordenes = ttk.Treeview(contenedor_principal, columns=columns_ordenes, show='headings', selectmode='browse', height=20)
        tabla_ordenes.heading('N_orden', text='N. orden')
        tabla_ordenes.heading('ID', text='ID')
        tabla_ordenes.heading('Fecha', text='Fecha')
        tabla_ordenes.heading('Cliente', text='Cliente')
        tabla_ordenes.heading('Total', text='Total')
        tabla_ordenes.column('N_orden', width=80, anchor=CENTER)
        tabla_ordenes.column('ID', width=60, anchor=CENTER)
        tabla_ordenes.column('Fecha', width=100, anchor=CENTER)
        tabla_ordenes.column('Cliente', width=120, anchor=W)
        tabla_ordenes.column('Total', width=100, anchor=CENTER)
        
        vsb_ordenes = ttk.Scrollbar(contenedor_principal, orient="vertical", command=tabla_ordenes.yview)
        tabla_ordenes.configure(yscrollcommand=vsb_ordenes.set)
        tabla_ordenes.pack(side=LEFT, fill="both", expand=True, padx=(0, 10))
        vsb_ordenes.pack(side=LEFT, fill="y")
        
        tabla_ordenes.tag_configure('odd', background='#FFFFFF')
        tabla_ordenes.tag_configure('even', background='#F6F0E8')
        
        # ========== TABLA DE DETALLES (DERECHA) ==========
        frame_detalles_titulo = Frame(contenedor_principal, bg="#D6D0C5")
        frame_detalles_titulo.pack(side=RIGHT, fill="x", expand=False)
        
        lbl_detalles = Label(frame_detalles_titulo, text="Detalles de la orden:", font=("Inter", 16), fg="#A6171C", bg="#D6D0C5")
        lbl_detalles.pack()
        
        # Tabla de detalles
        columns_detalles = ('Cantidad', 'Producto', 'Precio Unit.', 'Subtotal')
        tabla_detalles = ttk.Treeview(contenedor_principal, columns=columns_detalles, show='headings', height=20)
        tabla_detalles.heading('Cantidad', text='Cantidad')
        tabla_detalles.heading('Producto', text='Producto')
        tabla_detalles.heading('Precio Unit.', text='Precio Unit.')
        tabla_detalles.heading('Subtotal', text='Subtotal')
        tabla_detalles.column('Cantidad', width=80, anchor=CENTER)
        tabla_detalles.column('Producto', width=250, anchor=W)
        tabla_detalles.column('Precio Unit.', width=100, anchor=CENTER)
        tabla_detalles.column('Subtotal', width=100, anchor=CENTER)
        
        vsb_detalles = ttk.Scrollbar(contenedor_principal, orient="vertical", command=tabla_detalles.yview)
        tabla_detalles.configure(yscrollcommand=vsb_detalles.set)
        tabla_detalles.pack(side=RIGHT, fill="both", expand=True)
        vsb_detalles.pack(side=RIGHT, fill="y")
        
        tabla_detalles.tag_configure('odd', background='#FFFFFF')
        tabla_detalles.tag_configure('even', background='#F6F0E8')
        
        # Botón para buscar
        btn_buscar = Button(header, text="Buscar", font=("Inter", 14), fg="#A6171C", bg="#F1C045", command=lambda: cargar_ordenes_por_fecha())
        btn_buscar.pack(pady=5)
        
        # Definir funciones locales
        def cargar_ordenes_por_fecha():
            """Carga las órdenes de la fecha seleccionada."""
            try:
                ano = int(spinbox_ano.get())
                mes = int(spinbox_mes.get())
                dia = int(spinbox_dia.get())
                fecha = datetime(ano, mes, dia).date()
                
                # Limpiar tabla de órdenes
                for item in tabla_ordenes.get_children():
                    tabla_ordenes.delete(item)
                
                # Limpiar tabla de detalles
                for item in tabla_detalles.get_children():
                    tabla_detalles.delete(item)
                
                ordenes = metodos_ordenes.Ordenes_acciones.obtener_ordenes_por_fecha(fecha)
                
                if not ordenes:
                    messagebox.showinfo("Información", f"No hay órdenes para la fecha {fecha}")
                    return
                
                for contador, orden in enumerate(ordenes, 1):
                    id_orden = orden[0]
                    fecha_orden = orden[1]
                    total = orden[2]
                    cliente = orden[3]
                    
                    try:
                        total_text = f"${float(total):.2f}"
                    except:
                        total_text = str(total)
                    
                    tag = 'even' if contador % 2 == 0 else 'odd'
                    tabla_ordenes.insert('', 'end', values=(contador, id_orden, fecha_orden, cliente, total_text), tags=(tag,), iid=id_orden)
            except ValueError as e:
                messagebox.showerror("Error", "Por favor ingrese valores válidos para la fecha")
        
        def mostrar_detalles_orden(event=None):
            """Muestra los detalles de la orden seleccionada."""
            seleccionado = tabla_ordenes.selection()
            if not seleccionado:
                return
            
            id_orden = seleccionado[0]
            
            # Limpiar tabla de detalles
            for item in tabla_detalles.get_children():
                tabla_detalles.delete(item)
            
            try:
                detalles = metodos_ordenes.Ordenes_acciones.obtener_detalles_orden(id_orden)
                
                if not detalles:
                    messagebox.showinfo("Información", "Esta orden no tiene detalles registrados")
                    return
                
                for contador, detalle in enumerate(detalles, 1):
                    # detalle: (amount, id_product, product_name, unit_price, subtotal)
                    cantidad = detalle[0]
                    producto = detalle[2] if len(detalle) > 2 else detalle[1]
                    precio = detalle[3] if len(detalle) > 3 else (detalle[2] if len(detalle) > 2 else 0)
                    subtotal = detalle[4] if len(detalle) > 4 else 0
                    
                    try:
                        precio_text = f"${float(precio):.2f}"
                        subtotal_text = f"${float(subtotal):.2f}"
                    except:
                        precio_text = str(precio)
                        subtotal_text = str(subtotal)
                    
                    tag = 'even' if contador % 2 == 0 else 'odd'
                    tabla_detalles.insert('', 'end', values=(cantidad, producto, precio_text, subtotal_text), tags=(tag,))
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar detalles: {e}")
        
        # Ligar evento de selección en tabla de órdenes
        tabla_ordenes.bind('<<TreeviewSelect>>', mostrar_detalles_orden)
        
        # Frame de botones al final
        frame_botones = Frame(fondo, bg="#D6D0C5")
        frame_botones.pack(side=BOTTOM, fill=X, padx=50, pady=10)
        
        btn_regresar_det = Button(frame_botones, text="Regresar", font=("Inter", 18), fg="#A6171C", bg="#F1C045", command=lambda: self.menu_ordenes(ventana_ordenes))
        btn_regresar_det.pack(side=RIGHT, padx=10)
        
        # Cargar órdenes del día actual al abrir
        cargar_ordenes_por_fecha()


    
