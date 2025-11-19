from tkinter import *
from tkinter import ttk

class modificarproducto():
    @staticmethod
    def modificar_producto_(menu_producto):
        menu_producto.destroy()
        modificar_producto=Tk()
        modificar_producto.title("Modificar producto")
        modificar_producto.geometry("1920x1080")
        modificar_producto.state("zoomed")

        fondo=Frame(modificar_producto, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        titulo=Label(fondo2, text="Modificar producto",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
        titulo.pack(padx=20, pady=20)

        fondo3=Frame(fondo2, bg="white", height=180)
        fondo3.pack(expand=True)

        def volver_a_menu():
            from view.Productos.menu_productos import menuproducto
            menuproducto.menu_producto_(modificar_producto)

        producto_modificado=Label(fondo3, text="Selecciona el producto a modificar", font=("Inter", 24), bg="white")
        producto_modificado.pack(padx=20, pady=10)

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

        nombre=Label(fondo3, text="Nuevo nombre del producto", font=("Inter", 24), bg="white")
        nombre.pack(padx=20, pady=10)
        
        nombre_entry=Entry(fondo3, font=("Inter", 24), bg="white")
        nombre_entry.pack(padx=20, pady=10)

        precio=Label(fondo3, text="Nuevo precio unitario", font=("Inter", 24), bg="white")
        precio.pack(padx=20, pady=10)

        precio_entry=Entry(fondo3, font=("Inter", 24), bg="white")
        precio_entry.pack(padx=20, pady=10)

        regresar=Button(fondo3, text="Regresar", font=("Inter", 24), bg="#F1C045", command=volver_a_menu)
        regresar.pack(padx=20, pady=10)
        
        agregar=Button(fondo3, text="Modificar", font=("Inter", 24), bg="#F1C045")
        agregar.pack(padx=20, pady=10)