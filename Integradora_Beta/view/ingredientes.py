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

        fondo2 = Frame(fondo, bg="#A6171C", width=1200, height=700)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=40, pady=40)

        lbl_titulo = Label(fondo2, text="Ingredientes", font=("Orelega One", 36), fg="#F1C045", bg="#A6171C")
        lbl_titulo.pack(padx=20, pady=20)

        contenedor = Frame(fondo2, bg="white", width=1000, height=450)
        contenedor.pack_propagate(False)
        contenedor.pack(padx=20, pady=10)

        columns = ('ID', 'Nombre', 'Cantidad', 'Unidad', 'ID_Product')
        tree = ttk.Treeview(contenedor, columns=columns, show='headings', height=10)
        for col in columns:
            tree.heading(col, text=col)
            if col == 'Nombre':
                tree.column(col, width=400)
            else:
                tree.column(col, width=100, anchor=CENTER)

        vsb = ttk.Scrollbar(contenedor, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side=LEFT, fill=BOTH, expand=True, padx=(10,0), pady=10)
        vsb.pack(side=RIGHT, fill=Y, padx=(0,10), pady=10)

        # container for action buttons
        btn_frame = Frame(fondo2, bg="#A6171C")
        btn_frame.pack(padx=20, pady=10, fill='x')

        btn_agregar = Button(btn_frame, text="Agregar ingrediente", font=("Inter", 14), bg="#F1C045", fg="#A6171C", command=lambda: self.nuevoIngrediente(menu_ingredientes))
        btn_agregar.pack(side=LEFT, padx=10)
        btn_editar = Button(btn_frame, text="Editar seleccionado", font=("Inter", 14), bg="#F1C045", fg="#A6171C", command=lambda: on_editar_selected())
        btn_editar.pack(side=LEFT, padx=10)
        btn_borrar = Button(btn_frame, text="Borrar seleccionado", font=("Inter", 14), bg="#F1C045", fg="#A6171C", command=lambda: on_borrar_selected())
        btn_borrar.pack(side=LEFT, padx=10)
        btn_regresar = Button(btn_frame, text="Regresar", font=("Inter", 14), bg="#F1C045", fg="#A6171C", command=lambda: self.regresar(menu_ingredientes))
        btn_regresar.pack(side=RIGHT, padx=10)

        def load_items():
            # Clear tree
            for n in tree.get_children():
                tree.delete(n)
            try:
                items = metodos_ingredientes.Ingredientes_acciones.obtener_ingredientes()
                for ing in items:
                    # expected order: id_ingredient, name, quantity, measurement_unit, id_product
                    iid = ing[0]
                    name = ing[1]
                    qty = ing[2]
                    unit = ing[3]
                    id_prod = ing[4] if len(ing) > 4 else ''
                    tree.insert('', 'end', values=(iid, name, qty, unit, id_prod))
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar ingredientes: {e}")

        def on_borrar_selected():
            try:
                sel = tree.selection()
                if not sel:
                    messagebox.showwarning("Advertencia", "Seleccione un ingrediente a borrar.")
                    return
                iid = sel[0]
                vals = tree.item(iid, 'values')
                id_ing = vals[0]
                confirm = messagebox.askyesno("Confirmar", f"¿Desea eliminar el ingrediente ID {id_ing}?" )
                if not confirm:
                    return
                pwd = simpledialog.askstring("Autorización", "Ingrese la contraseña para eliminar:", show='*', parent=menu_ingredientes)
                if pwd is None:
                    return
                if pwd != ADMIN_PASSWORD:
                    messagebox.showerror("Error", "Contraseña incorrecta.")
                    return
                ok = metodos_ingredientes.Ingredientes_acciones.borrar(id_ing)
                if ok:
                    messagebox.showinfo("Éxito", "Ingrediente eliminado.")
                    load_items()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el ingrediente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {e}")

        def on_editar_selected():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Advertencia", "Seleccione un ingrediente a editar.")
                return
            iid = sel[0]
            vals = tree.item(iid, 'values')
            id_ing = vals[0]
            self.modificarIngrediente(menu_ingredientes, id_ing)

        load_items()

    def nuevoIngrediente(self, nuevo_ingrediente):
        """Add a new ingredient via a small form."""
        self.borrarPantalla(nuevo_ingrediente)
        nuevo_ingrediente.title("Nuevo ingrediente")
        nuevo_ingrediente.geometry("800x600")
        nuevo_ingrediente.state("normal")

        fondo = Frame(nuevo_ingrediente, bg="#D6D0C5")
        fondo.pack(fill='both', expand=True)

        fondo2 = Frame(fondo, bg="#A6171C")
        fondo2.pack(padx=40, pady=40, fill='both', expand=True)

        lbl_nombre = Label(fondo2, text="Nombre", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_nombre.pack(padx=20, pady=10)
        ent_nombre = Entry(fondo2, font=("Inter", 14))
        ent_nombre.pack(padx=20, pady=10)

        lbl_cant = Label(fondo2, text="Cantidad", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_cant.pack(padx=20, pady=10)
        ent_cant = Entry(fondo2, font=("Inter", 14))
        ent_cant.pack(padx=20, pady=10)

        lbl_unit = Label(fondo2, text="Unidad de medida", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_unit.pack(padx=20, pady=10)
        ent_unit = Entry(fondo2, font=("Inter", 14))
        ent_unit.pack(padx=20, pady=10)

        # Optional: link to product
        lbl_id_prod = Label(fondo2, text="ID Producto (opcional)", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_id_prod.pack(padx=20, pady=10)
        # Load product ids for convenience (if available)
        products = metodos_productos.Productos_acciones.obtener_productos() if hasattr(metodos_productos.Productos_acciones, 'obtener_productos') else []
        prod_vals = [''] + [str(p[0]) for p in products]
        cb_prod = ttk.Combobox(fondo2, values=prod_vals, state='readonly')
        cb_prod.set(prod_vals[0])
        cb_prod.pack(padx=20, pady=10)

        def on_save():
            name = ent_nombre.get().strip()
            qty = ent_cant.get().strip()
            unit = ent_unit.get().strip()
            id_prod = cb_prod.get().strip() or None
            if not name:
                messagebox.showerror("Error", "El nombre es requerido.")
                return
            try:
                if qty:
                    # allow decimal but cast to float for validations
                    x = float(qty)
            except Exception:
                messagebox.showerror("Error", "Cantidad inválida.")
                return

            new_id = metodos_ingredientes.Ingredientes_acciones.agregar(name, qty or 0, unit or '', id_prod)
            if not new_id:
                messagebox.showerror("Error", "No se pudo agregar ingrediente.")
                return
            messagebox.showinfo("Éxito", "Ingrediente agregado correctamente.")
            self.menu_ingrediente(nuevo_ingrediente)

        btn_save = Button(fondo2, text='Guardar', command=on_save, bg='#F1C045')
        btn_save.pack(padx=20, pady=20)
        btn_cancel = Button(fondo2, text='Cancelar', command=lambda: self.menu_ingrediente(nuevo_ingrediente), bg='#F1C045')
        btn_cancel.pack(padx=20, pady=10)

    def modificarIngrediente(self, modificar_ingrediente, id_ingredient):
        """Modify an existing ingredient by id."""
        self.borrarPantalla(modificar_ingrediente)
        modificar_ingrediente.title("Modificar ingrediente")
        modificar_ingrediente.geometry("800x600")
        modificar_ingrediente.state("normal")

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
            # id, name, qty, unit, id_product
            _, name, qty, unit, id_prod = sel
        except Exception:
            messagebox.showerror("Error", "No se pudo cargar ingrediente.")
            self.menu_ingrediente(modificar_ingrediente)
            return

        lbl_nombre = Label(fondo2, text="Nombre", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_nombre.pack(padx=20, pady=10)
        ent_nombre = Entry(fondo2, font=("Inter", 14))
        ent_nombre.insert(0, name)
        ent_nombre.pack(padx=20, pady=10)

        lbl_cant = Label(fondo2, text="Cantidad", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_cant.pack(padx=20, pady=10)
        ent_cant = Entry(fondo2, font=("Inter", 14))
        ent_cant.insert(0, qty)
        ent_cant.pack(padx=20, pady=10)

        lbl_unit = Label(fondo2, text="Unidad de medida", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_unit.pack(padx=20, pady=10)
        ent_unit = Entry(fondo2, font=("Inter", 14))
        ent_unit.insert(0, unit)
        ent_unit.pack(padx=20, pady=10)

        lbl_id_prod = Label(fondo2, text="ID Producto (opcional)", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_id_prod.pack(padx=20, pady=10)
        products = metodos_productos.Productos_acciones.obtener_productos() if hasattr(metodos_productos.Productos_acciones, 'obtener_productos') else []
        prod_vals = [''] + [str(p[0]) for p in products]
        cb_prod = ttk.Combobox(fondo2, values=prod_vals, state='readonly')
        cb_prod.set(str(id_prod) if id_prod else prod_vals[0])
        cb_prod.pack(padx=20, pady=10)

        def on_update():
            new_name = ent_nombre.get().strip()
            new_qty = ent_cant.get().strip()
            new_unit = ent_unit.get().strip()
            new_prod = cb_prod.get().strip() or None
            if not new_name:
                messagebox.showerror("Error", "El nombre es requerido.")
                return
            try:
                if new_qty:
                    _ = float(new_qty)
            except Exception:
                messagebox.showerror("Error", "Cantidad inválida.")
                return
            pwd = simpledialog.askstring("Autorización", "Ingrese la contraseña para modificar:", show='*', parent=modificar_ingrediente)
            if pwd is None:
                return
            if pwd != ADMIN_PASSWORD:
                messagebox.showerror("Error", "Contraseña incorrecta.")
                return
            ok = metodos_ingredientes.Ingredientes_acciones.modificar(new_name, new_qty or 0, new_unit or '', new_prod, id_ingredient)
            if ok:
                messagebox.showinfo("Éxito", "Ingrediente modificado.")
                self.menu_ingrediente(modificar_ingrediente)
            else:
                messagebox.showerror("Error", "No se pudo modificar el ingrediente.")

        btn_save = Button(fondo2, text='Guardar', command=on_update, bg='#F1C045')
        btn_save.pack(padx=20, pady=10)
        btn_cancel = Button(fondo2, text='Cancelar', command=lambda: self.menu_ingrediente(modificar_ingrediente), bg='#F1C045')
        btn_cancel.pack(padx=20, pady=10)

    def regresar(self, menu_usuarios):
        menu_principal.interfacesMenu(menu_usuarios)
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

        fondo2 = Frame(fondo, bg="#A6171C", width=1200, height=700)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=40, pady=40)

        lbl_titulo = Label(fondo2, text="Ingredientes", font=("Orelega One", 36), fg="#F1C045", bg="#A6171C")
        lbl_titulo.pack(padx=20, pady=20)

        contenedor = Frame(fondo2, bg="white", width=1000, height=450)
        contenedor.pack_propagate(False)
        contenedor.pack(padx=20, pady=10)

        columns = ('ID', 'Nombre', 'Cantidad', 'Unidad', 'ID_Product')
        tree = ttk.Treeview(contenedor, columns=columns, show='headings', height=10)
        for col in columns:
            tree.heading(col, text=col)
            if col == 'Nombre':
                tree.column(col, width=400)
            else:
                tree.column(col, width=100, anchor=CENTER)

        vsb = ttk.Scrollbar(contenedor, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side=LEFT, fill=BOTH, expand=True, padx=(10,0), pady=10)
        vsb.pack(side=RIGHT, fill=Y, padx=(0,10), pady=10)

        # container for action buttons
        btn_frame = Frame(fondo2, bg="#A6171C")
        btn_frame.pack(padx=20, pady=10, fill='x')

        btn_agregar = Button(btn_frame, text="Agregar ingrediente", font=("Inter", 14), bg="#F1C045", fg="#A6171C", command=lambda: self.nuevoIngrediente(menu_ingredientes))
        btn_agregar.pack(side=LEFT, padx=10)
        btn_editar = Button(btn_frame, text="Editar seleccionado", font=("Inter", 14), bg="#F1C045", fg="#A6171C", command=lambda: on_editar_selected())
        btn_editar.pack(side=LEFT, padx=10)
        btn_borrar = Button(btn_frame, text="Borrar seleccionado", font=("Inter", 14), bg="#F1C045", fg="#A6171C", command=lambda: on_borrar_selected())
        btn_borrar.pack(side=LEFT, padx=10)
        btn_regresar = Button(btn_frame, text="Regresar", font=("Inter", 14), bg="#F1C045", fg="#A6171C", command=lambda: self.regresar(menu_ingredientes))
        btn_regresar.pack(side=RIGHT, padx=10)

        def load_items():
            # Clear tree
            for n in tree.get_children():
                tree.delete(n)
            try:
                items = metodos_ingredientes.Ingredientes_acciones.obtener_ingredientes()
                for ing in items:
                    # expected order: id_ingredient, name, quantity, measurement_unit, id_product
                    iid = ing[0]
                    name = ing[1]
                    qty = ing[2]
                    unit = ing[3]
                    id_prod = ing[4] if len(ing) > 4 else ''
                    tree.insert('', 'end', values=(iid, name, qty, unit, id_prod))
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar ingredientes: {e}")

        def on_borrar_selected():
            try:
                sel = tree.selection()
                if not sel:
                    messagebox.showwarning("Advertencia", "Seleccione un ingrediente a borrar.")
                    return
                iid = sel[0]
                vals = tree.item(iid, 'values')
                id_ing = vals[0]
                confirm = messagebox.askyesno("Confirmar", f"¿Desea eliminar el ingrediente ID {id_ing}?" )
                if not confirm:
                    return
                pwd = simpledialog.askstring("Autorización", "Ingrese la contraseña para eliminar:", show='*', parent=menu_ingredientes)
                if pwd is None:
                    return
                if pwd != ADMIN_PASSWORD:
                    messagebox.showerror("Error", "Contraseña incorrecta.")
                    return
                ok = metodos_ingredientes.Ingredientes_acciones.borrar(id_ing)
                if ok:
                    messagebox.showinfo("Éxito", "Ingrediente eliminado.")
                    load_items()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el ingrediente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {e}")

        def on_editar_selected():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Advertencia", "Seleccione un ingrediente a editar.")
                return
            iid = sel[0]
            vals = tree.item(iid, 'values')
            id_ing = vals[0]
            self.modificarIngrediente(menu_ingredientes, id_ing)

        load_items()

    def nuevoIngrediente(self, nuevo_ingrediente):
        """Add a new ingredient via a small form."""
        self.borrarPantalla(nuevo_ingrediente)
        nuevo_ingrediente.title("Nuevo ingrediente")
        nuevo_ingrediente.geometry("800x600")
        nuevo_ingrediente.state("normal")

        fondo = Frame(nuevo_ingrediente, bg="#D6D0C5")
        fondo.pack(fill='both', expand=True)

        fondo2 = Frame(fondo, bg="#A6171C")
        fondo2.pack(padx=40, pady=40, fill='both', expand=True)

        lbl_nombre = Label(fondo2, text="Nombre", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_nombre.pack(padx=20, pady=10)
        ent_nombre = Entry(fondo2, font=("Inter", 14))
        ent_nombre.pack(padx=20, pady=10)

        lbl_cant = Label(fondo2, text="Cantidad", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_cant.pack(padx=20, pady=10)
        ent_cant = Entry(fondo2, font=("Inter", 14))
        ent_cant.pack(padx=20, pady=10)

        lbl_unit = Label(fondo2, text="Unidad de medida", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_unit.pack(padx=20, pady=10)
        ent_unit = Entry(fondo2, font=("Inter", 14))
        ent_unit.pack(padx=20, pady=10)

        # Optional: link to product
        lbl_id_prod = Label(fondo2, text="ID Producto (opcional)", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_id_prod.pack(padx=20, pady=10)
        # Load product ids for convenience (if available)
        products = metodos_productos.Productos_acciones.obtener_productos() if hasattr(metodos_productos.Productos_acciones, 'obtener_productos') else []
        prod_vals = [''] + [str(p[0]) for p in products]
        cb_prod = ttk.Combobox(fondo2, values=prod_vals, state='readonly')
        cb_prod.set(prod_vals[0])
        cb_prod.pack(padx=20, pady=10)

        def on_save():
            name = ent_nombre.get().strip()
            qty = ent_cant.get().strip()
            unit = ent_unit.get().strip()
            id_prod = cb_prod.get().strip() or None
            if not name:
                messagebox.showerror("Error", "El nombre es requerido.")
                return
            try:
                if qty:
                    # allow decimal but cast to float for validations
                    x = float(qty)
            except Exception:
                messagebox.showerror("Error", "Cantidad inválida.")
                return

            new_id = metodos_ingredientes.Ingredientes_acciones.agregar(name, qty or 0, unit or '', id_prod)
            if not new_id:
                messagebox.showerror("Error", "No se pudo agregar ingrediente.")
                return
            messagebox.showinfo("Éxito", "Ingrediente agregado correctamente.")
            self.menu_ingrediente(nuevo_ingrediente)

        btn_save = Button(fondo2, text='Guardar', command=on_save, bg='#F1C045')
        btn_save.pack(padx=20, pady=20)
        btn_cancel = Button(fondo2, text='Cancelar', command=lambda: self.menu_ingrediente(nuevo_ingrediente), bg='#F1C045')
        btn_cancel.pack(padx=20, pady=10)

    def modificarIngrediente(self, modificar_ingrediente, id_ingredient):
        """Modify an existing ingredient by id."""
        self.borrarPantalla(modificar_ingrediente)
        modificar_ingrediente.title("Modificar ingrediente")
        modificar_ingrediente.geometry("800x600")
        modificar_ingrediente.state("normal")

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
            # id, name, qty, unit, id_product
            _, name, qty, unit, id_prod = sel
        except Exception:
            messagebox.showerror("Error", "No se pudo cargar ingrediente.")
            self.menu_ingrediente(modificar_ingrediente)
            return

        lbl_nombre = Label(fondo2, text="Nombre", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_nombre.pack(padx=20, pady=10)
        ent_nombre = Entry(fondo2, font=("Inter", 14))
        ent_nombre.insert(0, name)
        ent_nombre.pack(padx=20, pady=10)

        lbl_cant = Label(fondo2, text="Cantidad", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_cant.pack(padx=20, pady=10)
        ent_cant = Entry(fondo2, font=("Inter", 14))
        ent_cant.insert(0, qty)
        ent_cant.pack(padx=20, pady=10)

        lbl_unit = Label(fondo2, text="Unidad de medida", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_unit.pack(padx=20, pady=10)
        ent_unit = Entry(fondo2, font=("Inter", 14))
        ent_unit.insert(0, unit)
        ent_unit.pack(padx=20, pady=10)

        lbl_id_prod = Label(fondo2, text="ID Producto (opcional)", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_id_prod.pack(padx=20, pady=10)
        products = metodos_productos.Productos_acciones.obtener_productos() if hasattr(metodos_productos.Productos_acciones, 'obtener_productos') else []
        prod_vals = [''] + [str(p[0]) for p in products]
        cb_prod = ttk.Combobox(fondo2, values=prod_vals, state='readonly')
        cb_prod.set(str(id_prod) if id_prod else prod_vals[0])
        cb_prod.pack(padx=20, pady=10)

        def on_update():
            new_name = ent_nombre.get().strip()
            new_qty = ent_cant.get().strip()
            new_unit = ent_unit.get().strip()
            new_prod = cb_prod.get().strip() or None
            if not new_name:
                messagebox.showerror("Error", "El nombre es requerido.")
                return
            try:
                if new_qty:
                    _ = float(new_qty)
            except Exception:
                messagebox.showerror("Error", "Cantidad inválida.")
                return
            pwd = simpledialog.askstring("Autorización", "Ingrese la contraseña para modificar:", show='*', parent=modificar_ingrediente)
            if pwd is None:
                return
            if pwd != ADMIN_PASSWORD:
                messagebox.showerror("Error", "Contraseña incorrecta.")
                return
            ok = metodos_ingredientes.Ingredientes_acciones.modificar(new_name, new_qty or 0, new_unit or '', new_prod, id_ingredient)
            if ok:
                messagebox.showinfo("Éxito", "Ingrediente modificado.")
                self.menu_ingrediente(modificar_ingrediente)
            else:
                messagebox.showerror("Error", "No se pudo modificar el ingrediente.")

        btn_save = Button(fondo2, text='Guardar', command=on_update, bg='#F1C045')
        btn_save.pack(padx=20, pady=10)
        btn_cancel = Button(fondo2, text='Cancelar', command=lambda: self.menu_ingrediente(modificar_ingrediente), bg='#F1C045')
        btn_cancel.pack(padx=20, pady=10)

    def regresar(self, menu_usuarios):
        menu_principal.interfacesMenu(menu_usuarios)
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

        fondo2 = Frame(fondo, bg="#A6171C", width=1200, height=700)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=40, pady=40)

        lbl_titulo = Label(fondo2, text="Ingredientes", font=("Orelega One", 36), fg="#F1C045", bg="#A6171C")
        lbl_titulo.pack(padx=20, pady=20)

        contenedor = Frame(fondo2, bg="white", width=1000, height=450)
        contenedor.pack_propagate(False)
        contenedor.pack(padx=20, pady=10)

        columns = ('ID', 'Nombre', 'Cantidad', 'Unidad', 'ID_Product')
        tree = ttk.Treeview(contenedor, columns=columns, show='headings', height=10)
        for col in columns:
            tree.heading(col, text=col)
            if col == 'Nombre':
                tree.column(col, width=400)
            else:
                tree.column(col, width=100, anchor=CENTER)

        vsb = ttk.Scrollbar(contenedor, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side=LEFT, fill=BOTH, expand=True, padx=(10,0), pady=10)
        vsb.pack(side=RIGHT, fill=Y, padx=(0,10), pady=10)

        # container for action buttons
        btn_frame = Frame(fondo2, bg="#A6171C")
        btn_frame.pack(padx=20, pady=10, fill='x')

        btn_agregar = Button(btn_frame, text="Agregar ingrediente", font=("Inter", 14), bg="#F1C045", fg="#A6171C", command=lambda: self.nuevoIngrediente(menu_ingredientes))
        btn_agregar.pack(side=LEFT, padx=10)
        btn_editar = Button(btn_frame, text="Editar seleccionado", font=("Inter", 14), bg="#F1C045", fg="#A6171C", command=lambda: on_editar_selected())
        btn_editar.pack(side=LEFT, padx=10)
        btn_borrar = Button(btn_frame, text="Borrar seleccionado", font=("Inter", 14), bg="#F1C045", fg="#A6171C", command=lambda: on_borrar_selected())
        btn_borrar.pack(side=LEFT, padx=10)
        btn_regresar = Button(btn_frame, text="Regresar", font=("Inter", 14), bg="#F1C045", fg="#A6171C", command=lambda: self.regresar(menu_ingredientes))
        btn_regresar.pack(side=RIGHT, padx=10)

        def load_items():
            # Clear tree
            for n in tree.get_children():
                tree.delete(n)
            try:
                items = metodos_ingredientes.Ingredientes_acciones.obtener_ingredientes()
                for ing in items:
                    # expected order: id_ingredient, name, quantity, measurement_unit, id_product
                    iid = ing[0]
                    name = ing[1]
                    qty = ing[2]
                    unit = ing[3]
                    id_prod = ing[4] if len(ing) > 4 else ''
                    tree.insert('', 'end', values=(iid, name, qty, unit, id_prod))
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar ingredientes: {e}")

        def on_borrar_selected():
            try:
                sel = tree.selection()
                if not sel:
                    messagebox.showwarning("Advertencia", "Seleccione un ingrediente a borrar.")
                    return
                iid = sel[0]
                vals = tree.item(iid, 'values')
                id_ing = vals[0]
                confirm = messagebox.askyesno("Confirmar", f"¿Desea eliminar el ingrediente ID {id_ing}?" )
                if not confirm:
                    return
                pwd = simpledialog.askstring("Autorización", "Ingrese la contraseña para eliminar:", show='*', parent=menu_ingredientes)
                if pwd is None:
                    return
                if pwd != ADMIN_PASSWORD:
                    messagebox.showerror("Error", "Contraseña incorrecta.")
                    return
                ok = metodos_ingredientes.Ingredientes_acciones.borrar(id_ing)
                if ok:
                    messagebox.showinfo("Éxito", "Ingrediente eliminado.")
                    load_items()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el ingrediente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {e}")

        def on_editar_selected():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Advertencia", "Seleccione un ingrediente a editar.")
                return
            iid = sel[0]
            vals = tree.item(iid, 'values')
            id_ing = vals[0]
            self.modificarIngrediente(menu_ingredientes, id_ing)

        load_items()

    def nuevoIngrediente(self, nuevo_ingrediente):
        """Add a new ingredient via a small form."""
        self.borrarPantalla(nuevo_ingrediente)
        nuevo_ingrediente.title("Nuevo ingrediente")
        nuevo_ingrediente.geometry("800x600")
        nuevo_ingrediente.state("normal")

        fondo = Frame(nuevo_ingrediente, bg="#D6D0C5")
        fondo.pack(fill='both', expand=True)

        fondo2 = Frame(fondo, bg="#A6171C")
        fondo2.pack(padx=40, pady=40, fill='both', expand=True)

        lbl_nombre = Label(fondo2, text="Nombre", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_nombre.pack(padx=20, pady=10)
        ent_nombre = Entry(fondo2, font=("Inter", 14))
        ent_nombre.pack(padx=20, pady=10)

        lbl_cant = Label(fondo2, text="Cantidad", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_cant.pack(padx=20, pady=10)
        ent_cant = Entry(fondo2, font=("Inter", 14))
        ent_cant.pack(padx=20, pady=10)

        lbl_unit = Label(fondo2, text="Unidad de medida", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_unit.pack(padx=20, pady=10)
        ent_unit = Entry(fondo2, font=("Inter", 14))
        ent_unit.pack(padx=20, pady=10)

        # Optional: link to product
        lbl_id_prod = Label(fondo2, text="ID Producto (opcional)", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_id_prod.pack(padx=20, pady=10)
        # Load product ids for convenience (if available)
        products = metodos_productos.Productos_acciones.obtener_productos() if hasattr(metodos_productos.Productos_acciones, 'obtener_productos') else []
        prod_vals = [''] + [str(p[0]) for p in products]
        cb_prod = ttk.Combobox(fondo2, values=prod_vals, state='readonly')
        cb_prod.set(prod_vals[0])
        cb_prod.pack(padx=20, pady=10)

        def on_save():
            name = ent_nombre.get().strip()
            qty = ent_cant.get().strip()
            unit = ent_unit.get().strip()
            id_prod = cb_prod.get().strip() or None
            if not name:
                messagebox.showerror("Error", "El nombre es requerido.")
                return
            try:
                if qty:
                    # allow decimal but cast to float for validations
                    x = float(qty)
            except Exception:
                messagebox.showerror("Error", "Cantidad inválida.")
                return

            new_id = metodos_ingredientes.Ingredientes_acciones.agregar(name, qty or 0, unit or '', id_prod)
            if not new_id:
                messagebox.showerror("Error", "No se pudo agregar ingrediente.")
                return
            messagebox.showinfo("Éxito", "Ingrediente agregado correctamente.")
            self.menu_ingrediente(nuevo_ingrediente)

        btn_save = Button(fondo2, text='Guardar', command=on_save, bg='#F1C045')
        btn_save.pack(padx=20, pady=20)
        btn_cancel = Button(fondo2, text='Cancelar', command=lambda: self.menu_ingrediente(nuevo_ingrediente), bg='#F1C045')
        btn_cancel.pack(padx=20, pady=10)

    def modificarIngrediente(self, modificar_ingrediente, id_ingredient):
        """Modify an existing ingredient by id."""
        self.borrarPantalla(modificar_ingrediente)
        modificar_ingrediente.title("Modificar ingrediente")
        modificar_ingrediente.geometry("800x600")
        modificar_ingrediente.state("normal")

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
            # id, name, qty, unit, id_product
            _, name, qty, unit, id_prod = sel
        except Exception:
            messagebox.showerror("Error", "No se pudo cargar ingrediente.")
            self.menu_ingrediente(modificar_ingrediente)
            return

        lbl_nombre = Label(fondo2, text="Nombre", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_nombre.pack(padx=20, pady=10)
        ent_nombre = Entry(fondo2, font=("Inter", 14))
        ent_nombre.insert(0, name)
        ent_nombre.pack(padx=20, pady=10)

        lbl_cant = Label(fondo2, text="Cantidad", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_cant.pack(padx=20, pady=10)
        ent_cant = Entry(fondo2, font=("Inter", 14))
        ent_cant.insert(0, qty)
        ent_cant.pack(padx=20, pady=10)

        lbl_unit = Label(fondo2, text="Unidad de medida", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_unit.pack(padx=20, pady=10)
        ent_unit = Entry(fondo2, font=("Inter", 14))
        ent_unit.insert(0, unit)
        ent_unit.pack(padx=20, pady=10)

        lbl_id_prod = Label(fondo2, text="ID Producto (opcional)", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_id_prod.pack(padx=20, pady=10)
        products = metodos_productos.Productos_acciones.obtener_productos() if hasattr(metodos_productos.Productos_acciones, 'obtener_productos') else []
        prod_vals = [''] + [str(p[0]) for p in products]
        cb_prod = ttk.Combobox(fondo2, values=prod_vals, state='readonly')
        cb_prod.set(str(id_prod) if id_prod else prod_vals[0])
        cb_prod.pack(padx=20, pady=10)

        def on_update():
            new_name = ent_nombre.get().strip()
            new_qty = ent_cant.get().strip()
            new_unit = ent_unit.get().strip()
            new_prod = cb_prod.get().strip() or None
            if not new_name:
                messagebox.showerror("Error", "El nombre es requerido.")
                return
            try:
                if new_qty:
                    _ = float(new_qty)
            except Exception:
                messagebox.showerror("Error", "Cantidad inválida.")
                return
            pwd = simpledialog.askstring("Autorización", "Ingrese la contraseña para modificar:", show='*', parent=modificar_ingrediente)
            if pwd is None:
                return
            if pwd != ADMIN_PASSWORD:
                messagebox.showerror("Error", "Contraseña incorrecta.")
                return
            ok = metodos_ingredientes.Ingredientes_acciones.modificar(new_name, new_qty or 0, new_unit or '', new_prod, id_ingredient)
            if ok:
                messagebox.showinfo("Éxito", "Ingrediente modificado.")
                self.menu_ingrediente(modificar_ingrediente)
            else:
                messagebox.showerror("Error", "No se pudo modificar el ingrediente.")

        btn_save = Button(fondo2, text='Guardar', command=on_update, bg='#F1C045')
        btn_save.pack(padx=20, pady=10)
        btn_cancel = Button(fondo2, text='Cancelar', command=lambda: self.menu_ingrediente(modificar_ingrediente), bg='#F1C045')
        btn_cancel.pack(padx=20, pady=10)

    def regresar(self, menu_usuarios):
        menu_principal.interfacesMenu(menu_usuarios)
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

        fondo2 = Frame(fondo, bg="#A6171C", width=1200, height=700)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=40, pady=40)

        lbl_titulo = Label(fondo2, text="Ingredientes", font=("Orelega One", 36), fg="#F1C045", bg="#A6171C")
        lbl_titulo.pack(padx=20, pady=20)

        contenedor = Frame(fondo2, bg="white", width=1000, height=450)
        contenedor.pack_propagate(False)
        contenedor.pack(padx=20, pady=10)

        columns = ('ID', 'Nombre', 'Cantidad', 'Unidad', 'ID_Product')
        tree = ttk.Treeview(contenedor, columns=columns, show='headings', height=10)
        for col in columns:
            tree.heading(col, text=col)
            if col == 'Nombre':
                tree.column(col, width=400)
            else:
                tree.column(col, width=100, anchor=CENTER)

        vsb = ttk.Scrollbar(contenedor, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        tree.pack(side=LEFT, fill=BOTH, expand=True, padx=(10,0), pady=10)
        vsb.pack(side=RIGHT, fill=Y, padx=(0,10), pady=10)

        # container for action buttons
        btn_frame = Frame(fondo2, bg="#A6171C")
        btn_frame.pack(padx=20, pady=10, fill='x')

        btn_agregar = Button(btn_frame, text="Agregar ingrediente", font=("Inter", 14), bg="#F1C045", fg="#A6171C", command=lambda: self.nuevoIngrediente(menu_ingredientes))
        btn_agregar.pack(side=LEFT, padx=10)
        btn_editar = Button(btn_frame, text="Editar seleccionado", font=("Inter", 14), bg="#F1C045", fg="#A6171C", command=lambda: on_editar_selected())
        btn_editar.pack(side=LEFT, padx=10)
        btn_borrar = Button(btn_frame, text="Borrar seleccionado", font=("Inter", 14), bg="#F1C045", fg="#A6171C", command=lambda: on_borrar_selected())
        btn_borrar.pack(side=LEFT, padx=10)
        btn_regresar = Button(btn_frame, text="Regresar", font=("Inter", 14), bg="#F1C045", fg="#A6171C", command=lambda: self.regresar(menu_ingredientes))
        btn_regresar.pack(side=RIGHT, padx=10)

        def load_items():
            # Clear tree
            for n in tree.get_children():
                tree.delete(n)
            try:
                items = metodos_ingredientes.Ingredientes_acciones.obtener_ingredientes()
                for ing in items:
                    # expected order: id_ingredient, name, quantity, measurement_unit, id_product
                    iid = ing[0]
                    name = ing[1]
                    qty = ing[2]
                    unit = ing[3]
                    id_prod = ing[4] if len(ing) > 4 else ''
                    tree.insert('', 'end', values=(iid, name, qty, unit, id_prod))
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar ingredientes: {e}")

        def on_borrar_selected():
            try:
                sel = tree.selection()
                if not sel:
                    messagebox.showwarning("Advertencia", "Seleccione un ingrediente a borrar.")
                    return
                iid = sel[0]
                vals = tree.item(iid, 'values')
                id_ing = vals[0]
                confirm = messagebox.askyesno("Confirmar", f"¿Desea eliminar el ingrediente ID {id_ing}?" )
                if not confirm:
                    return
                pwd = simpledialog.askstring("Autorización", "Ingrese la contraseña para eliminar:", show='*', parent=menu_ingredientes)
                if pwd is None:
                    return
                if pwd != ADMIN_PASSWORD:
                    messagebox.showerror("Error", "Contraseña incorrecta.")
                    return
                ok = metodos_ingredientes.Ingredientes_acciones.borrar(id_ing)
                if ok:
                    messagebox.showinfo("Éxito", "Ingrediente eliminado.")
                    load_items()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el ingrediente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {e}")

        def on_editar_selected():
            sel = tree.selection()
            if not sel:
                messagebox.showwarning("Advertencia", "Seleccione un ingrediente a editar.")
                return
            iid = sel[0]
            vals = tree.item(iid, 'values')
            id_ing = vals[0]
            self.modificarIngrediente(menu_ingredientes, id_ing)

        load_items()

    def nuevoIngrediente(self, nuevo_ingrediente):
        """Add a new ingredient via a small form."""
        self.borrarPantalla(nuevo_ingrediente)
        nuevo_ingrediente.title("Nuevo ingrediente")
        nuevo_ingrediente.geometry("800x600")
        nuevo_ingrediente.state("normal")

        fondo = Frame(nuevo_ingrediente, bg="#D6D0C5")
        fondo.pack(fill='both', expand=True)

        fondo2 = Frame(fondo, bg="#A6171C")
        fondo2.pack(padx=40, pady=40, fill='both', expand=True)

        lbl_nombre = Label(fondo2, text="Nombre", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_nombre.pack(padx=20, pady=10)
        ent_nombre = Entry(fondo2, font=("Inter", 14))
        ent_nombre.pack(padx=20, pady=10)

        lbl_cant = Label(fondo2, text="Cantidad", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_cant.pack(padx=20, pady=10)
        ent_cant = Entry(fondo2, font=("Inter", 14))
        ent_cant.pack(padx=20, pady=10)

        lbl_unit = Label(fondo2, text="Unidad de medida", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_unit.pack(padx=20, pady=10)
        ent_unit = Entry(fondo2, font=("Inter", 14))
        ent_unit.pack(padx=20, pady=10)

        # Optional: link to product
        lbl_id_prod = Label(fondo2, text="ID Producto (opcional)", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_id_prod.pack(padx=20, pady=10)
        # Load product ids for convenience (if available)
        products = metodos_productos.Productos_acciones.obtener_productos() if hasattr(metodos_productos.Productos_acciones, 'obtener_productos') else []
        prod_vals = [''] + [str(p[0]) for p in products]
        cb_prod = ttk.Combobox(fondo2, values=prod_vals, state='readonly')
        cb_prod.set(prod_vals[0])
        cb_prod.pack(padx=20, pady=10)

        def on_save():
            name = ent_nombre.get().strip()
            qty = ent_cant.get().strip()
            unit = ent_unit.get().strip()
            id_prod = cb_prod.get().strip() or None
            if not name:
                messagebox.showerror("Error", "El nombre es requerido.")
                return
            try:
                if qty:
                    # allow decimal but cast to float for validations
                    x = float(qty)
            except Exception:
                messagebox.showerror("Error", "Cantidad inválida.")
                return

            new_id = metodos_ingredientes.Ingredientes_acciones.agregar(name, qty or 0, unit or '', id_prod)
            if not new_id:
                messagebox.showerror("Error", "No se pudo agregar ingrediente.")
                return
            messagebox.showinfo("Éxito", "Ingrediente agregado correctamente.")
            self.menu_ingrediente(nuevo_ingrediente)

        btn_save = Button(fondo2, text='Guardar', command=on_save, bg='#F1C045')
        btn_save.pack(padx=20, pady=20)
        btn_cancel = Button(fondo2, text='Cancelar', command=lambda: self.menu_ingrediente(nuevo_ingrediente), bg='#F1C045')
        btn_cancel.pack(padx=20, pady=10)

    def modificarIngrediente(self, modificar_ingrediente, id_ingredient):
        """Modify an existing ingredient by id."""
        self.borrarPantalla(modificar_ingrediente)
        modificar_ingrediente.title("Modificar ingrediente")
        modificar_ingrediente.geometry("800x600")
        modificar_ingrediente.state("normal")

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
            # id, name, qty, unit, id_product
            _, name, qty, unit, id_prod = sel
        except Exception:
            messagebox.showerror("Error", "No se pudo cargar ingrediente.")
            self.menu_ingrediente(modificar_ingrediente)
            return

        lbl_nombre = Label(fondo2, text="Nombre", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_nombre.pack(padx=20, pady=10)
        ent_nombre = Entry(fondo2, font=("Inter", 14))
        ent_nombre.insert(0, name)
        ent_nombre.pack(padx=20, pady=10)

        lbl_cant = Label(fondo2, text="Cantidad", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_cant.pack(padx=20, pady=10)
        ent_cant = Entry(fondo2, font=("Inter", 14))
        ent_cant.insert(0, qty)
        ent_cant.pack(padx=20, pady=10)

        lbl_unit = Label(fondo2, text="Unidad de medida", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_unit.pack(padx=20, pady=10)
        ent_unit = Entry(fondo2, font=("Inter", 14))
        ent_unit.insert(0, unit)
        ent_unit.pack(padx=20, pady=10)

        lbl_id_prod = Label(fondo2, text="ID Producto (opcional)", font=("Inter", 16), bg="#A6171C", fg="#F1C045")
        lbl_id_prod.pack(padx=20, pady=10)
        products = metodos_productos.Productos_acciones.obtener_productos() if hasattr(metodos_productos.Productos_acciones, 'obtener_productos') else []
        prod_vals = [''] + [str(p[0]) for p in products]
        cb_prod = ttk.Combobox(fondo2, values=prod_vals, state='readonly')
        cb_prod.set(str(id_prod) if id_prod else prod_vals[0])
        cb_prod.pack(padx=20, pady=10)

        def on_update():
            new_name = ent_nombre.get().strip()
            new_qty = ent_cant.get().strip()
            new_unit = ent_unit.get().strip()
            new_prod = cb_prod.get().strip() or None
            if not new_name:
                messagebox.showerror("Error", "El nombre es requerido.")
                return
            try:
                if new_qty:
                    _ = float(new_qty)
            except Exception:
                messagebox.showerror("Error", "Cantidad inválida.")
                return
            pwd = simpledialog.askstring("Autorización", "Ingrese la contraseña para modificar:", show='*', parent=modificar_ingrediente)
            if pwd is None:
                return
            if pwd != ADMIN_PASSWORD:
                messagebox.showerror("Error", "Contraseña incorrecta.")
                return
            ok = metodos_ingredientes.Ingredientes_acciones.modificar(new_name, new_qty or 0, new_unit or '', new_prod, id_ingredient)
            if ok:
                messagebox.showinfo("Éxito", "Ingrediente modificado.")
                self.menu_ingrediente(modificar_ingrediente)
            else:
                messagebox.showerror("Error", "No se pudo modificar el ingrediente.")

        btn_save = Button(fondo2, text='Guardar', command=on_update, bg='#F1C045')
        btn_save.pack(padx=20, pady=10)
        btn_cancel = Button(fondo2, text='Cancelar', command=lambda: self.menu_ingrediente(modificar_ingrediente), bg='#F1C045')
        btn_cancel.pack(padx=20, pady=10)

    def regresar(self, menu_usuarios):
        menu_principal.interfacesMenu(menu_usuarios)

    def regresar(self,menu_usuarios):

        menu_principal.interfacesMenu(menu_usuarios)
