from tkinter import *
from view import menu_principal
from tkinter import ttk
from model import metodos_productos

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
        tabla = ttk.Treeview(contenedor_tabla, columns=columns, show='headings', selectmode='browse')
        tabla.heading('Id_producto', text='Id_producto')
        tabla.heading('Nombre_producto', text='Nombre_producto')
        tabla.heading('Precio_unitario', text='Precio_unitario')
        tabla.heading('Acciones', text='Acciones')
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

        for i, producto in enumerate(productos):
            # producto es una tupla (id_prduct, prduct_name, unit_price)
            precio = producto[2]
            try:
                precio_text = f"{float(precio):.2f} MXN"
            except Exception:
                precio_text = str(precio)
            tag = 'even' if i % 2 == 0 else 'odd'
            # Insertar fila en la tabla (sin funciones)
            item_id = tabla.insert('', 'end', values=(producto[0], producto[1], precio_text, ''), tags=(tag,))

            # Crear botones visibles sobre la Treeview en la columna 'Acciones'
            # Los botones no tienen comando (no funcionales)
            btn_editar = Button(tabla, text='Editar', font=("Inter", 11), fg='#A6171C', bg='#F1F0EE', relief=RAISED, bd=1, padx=6, pady=2)
            btn_borrar = Button(tabla, text='Borrar', font=("Inter", 11), fg='#FFFFFF', bg='#A6171C', relief=RAISED, bd=1, padx=6, pady=2)
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

        btn_agregarProducto=Button(contenedor_tabla, text="Agregar producto", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: self.regresar(menu_productos), width=22)
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
        
        btn_agregar=Button(fondo3, text="Agregar", font=("Inter", 24), bg="#F1C045")
        btn_agregar.pack(padx=20, pady=10)

    def modificarProducto(self,modificar_producto):
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

        lbl_producto_modificado=Label(fondo3, text="Selecciona el producto a modificar", font=("Inter", 24), bg="white")
        lbl_producto_modificado.pack(padx=20, pady=10)

        prodcutos=[
            "Producto 1",
            "Producto 2",
            "Producto 3",
            "Producto 4"
        ]

        producto_modificado_combo=ttk.Combobox(fondo3, values=prodcutos, font=("Inter", 24))
        producto_modificado_combo.set("Selecciona un producto")
        producto_modificado_combo.pack(padx=20, pady=10)

        def on_select(event):
            print("Producto seleccionado:", producto_modificado_combo.get())
        
        producto_modificado_combo.bind('<<ComboboxSelected>>', on_select)

        lbl_nombre=Label(fondo3, text="Nuevo nombre del producto", font=("Inter", 24), bg="white")
        lbl_nombre.pack(padx=20, pady=10)
        
        nombre_entry=Entry(fondo3, font=("Inter", 24), bg="white")
        nombre_entry.pack(padx=20, pady=10)

        lbl_precio=Label(fondo3, text="Nuevo precio unitario", font=("Inter", 24), bg="white")
        lbl_precio.pack(padx=20, pady=10)

        precio_entry=Entry(fondo3, font=("Inter", 24), bg="white")
        precio_entry.pack(padx=20, pady=10)

        btn_regresar=Button(fondo3, text="Regresar", font=("Inter", 24), bg="#F1C045", command=lambda: self.menu_producto(modificar_producto))
        btn_regresar.pack(padx=20, pady=10)
        
        btn_agregar=Button(fondo3, text="Modificar", font=("Inter", 24), bg="#F1C045")
        btn_agregar.pack(padx=20, pady=10)

    def regresar(self,menu_usuarios):
        menu_principal.interfacesMenu(menu_usuarios)