from tkinter import *
from tkinter import ttk
from view import menu_principal
from model import metodos_ordenes
from controller import funciones
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
        columns = ('Id_orden', 'Fecha', 'Total', 'Cliente','Acciones')
        tabla = ttk.Treeview(contenedor_tabla, columns=columns, show='headings', selectmode='browse')
        tabla.heading('Id_orden', text='Id_orden')
        tabla.heading('Fecha', text='Fecha')
        tabla.heading('Total', text='Total')
        tabla.heading('Cliente', text='Cliente')
        tabla.heading('Acciones', text='Acciones')
        tabla.column('Id_orden', width=120, anchor=CENTER)
        tabla.column('Fecha', width=160, anchor=CENTER)
        tabla.column('Total', width=160, anchor=CENTER)
        tabla.column('Cliente', width=160, anchor=W)
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
        ordenes = metodos_ordenes.Ordenes_acciones.obtener_ordenes()
        # contenedor para guardar referencias a botones por fila
        _row_buttons = {}

        for i, orden in enumerate(ordenes):
            # producto es una tupla (id_prduct, prduct_name, unit_price)
            total = orden[2]
            try:
                total_text = f"{float(total):.2f} MXN"
            except Exception:
                total_text = str(total)
            tag = 'even' if i % 2 == 0 else 'odd'
            # Insertar fila en la tabla (sin funciones)
            item_id = tabla.insert('', 'end', values=(orden[0], orden[1], total_text,orden[3], ''), tags=(tag,))

            # Crear botones visibles sobre la Treeview en la columna 'Acciones'
            # Los botones no tienen comando (no funcionales)
            btn_editar = Button(tabla, text='Editar', font=("Inter", 11), fg='#A6171C', bg='#F1F0EE', relief=RAISED, bd=1, padx=6, pady=2)
            btn_borrar = Button(tabla, text='Borrar', font=("Inter", 11), fg='#FFFFFF', bg='#A6171C', relief=RAISED, bd=1, padx=6, pady=2)
            _row_buttons[item_id] = (btn_editar, btn_borrar)

        # Forzar dibujo y posicionar los botones sobre cada celda 'Acciones'
        ventana_ordenes.update_idletasks()

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

        btn_agregarProducto=Button(contenedor_tabla, text="Agregar producto", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: self.nuevaOrden(ventana_ordenes), width=22)
        btn_agregarProducto.pack(padx=20, pady=10, fill="x", side=LEFT)

        btn_regresar=Button(contenedor_tabla, text="Regresar", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=lambda: self.regresar(ventana_ordenes), width=22)
        btn_regresar.pack(padx=20, pady=10, fill="x", side=RIGHT)
    
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
        
        btn_alimentos=Button(header, text="Alimentos", font=("Inter", 24), fg="#A6171C", bg="#F1C045")
        btn_alimentos.pack(padx=20, pady=10, fill="x", side=LEFT, expand=True)
        
        btn_especiales=Button(header, text="Especiales", font=("Inter", 24), fg="#A6171C", bg="#F1C045")
        btn_especiales.pack(padx=20, pady=10, fill="x", side=LEFT, expand=True)

        btn_bebidas=Button(header, text="Bebidas", font=("Inter", 24), fg="#A6171C", bg="#F1C045")
        btn_bebidas.pack(padx=20, pady=10, fill="x", side=LEFT, expand=True)
        
        btn_confirmar=Button(header, text="Confirmar", font=("Inter", 24), fg="#A6171C", bg="#F1C045")
        btn_confirmar.pack(padx=20, pady=10, fill="x", side=LEFT, expand=True)

        contenedor_botones_productos=Frame(fondo, bg="#D6D0C5")
        contenedor_botones_productos.grid()

    def verOrdenes(self,ver_ordenes):
        self.borrarPantalla(ver_ordenes)
        ver_ordenes.title("Ver ordenes")
        ver_ordenes.geometry("1920x1080")
        ver_ordenes.state("zoomed")

        fondo=Frame(ver_ordenes, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        contenedor_botones=Frame(fondo2, bg="#A6171C", width=550, height=790)
        contenedor_botones.pack_propagate(False)
        contenedor_botones.pack(padx=300, pady=20)

        lbl_titulo=Label(contenedor_botones, text="Ver ordenes",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
        lbl_titulo.pack(padx=20, pady=20)
        
        lbl_fecha=Label(contenedor_botones, text="Fecha", font=("Inter", 24), bg="white")
        lbl_fecha.pack(padx=20, pady=10)

        fecha_entry=Entry(contenedor_botones, font=("Inter", 24), bg="white")
        fecha_entry.pack(padx=20, pady=10)

        btn_regresar=Button(contenedor_botones, text="Regresar", font=("Inter", 24), bg="#F1C045", command=lambda: self.menu_ordenes(ver_ordenes))
        btn_regresar.pack(padx=20, pady=10)

    def regresar(self,menu_usuarios):
        menu_principal.interfacesMenu(menu_usuarios)

    