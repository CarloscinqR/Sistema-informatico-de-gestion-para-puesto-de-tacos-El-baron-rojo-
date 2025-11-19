from tkinter import *
import conexionBD

class nuevoproducto():
    @staticmethod
    def nuevo_producto_(menu_producto):
        menu_producto.destroy()
        nuevo_producto=Tk()
        nuevo_producto.title("Nnuevo producto")
        nuevo_producto.geometry("1920x1080")
        nuevo_producto.state("zoomed")

        fondo=Frame(nuevo_producto, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        titulo=Label(fondo2, text="Nuevo producto",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
        titulo.pack(padx=20, pady=20)

        fondo3=Frame(fondo2, bg="white", height=180)
        fondo3.pack(expand=True)

        def volver_a_menu():
            from view.Productos.menu_productos import menuproducto
            menuproducto.menu_producto_(nuevo_producto)

        nombre=Label(fondo3, text="Nombre del producto", font=("Inter", 24), bg="white")
        nombre.pack(padx=20, pady=10)
        
        nombre_entry=Entry(fondo3, font=("Inter", 24), bg="white")
        nombre_entry.pack(padx=20, pady=10)

        precio=Label(fondo3, text="Precio unitario", font=("Inter", 24), bg="white")
        precio.pack(padx=20, pady=10)

        precio_entry=Entry(fondo3, font=("Inter", 24), bg="white")
        precio_entry.pack(padx=20, pady=10)

        regresar=Button(fondo3, text="Regresar", font=("Inter", 24), bg="#F1C045", command=volver_a_menu)
        regresar.pack(padx=20, pady=10)
        
        agregar=Button(fondo3, text="Agregar", font=("Inter", 24), bg="#F1C045")
        agregar.pack(padx=20, pady=10)

    class Productos_acciones:
        def __init__(self,nombre,precio):
            self._nombre=nombre
            self._precio=precio

        @property   
        def nombre(self):
            return self._nombre
        @nombre.setter
        def nombre(self, nombre):
            self._nombre = nombre
        @property
        def precio(self):
            return self._precio
        @precio.setter
        def precio(self, precio):
            self._precio = precio

        @staticmethod
        def nuevo_product(product_name,unit_price):
            try:
                conexionBD.cursor.execute(
                    "insert into products values(%s,%s)",
                    (product_name,unit_price)
                )
                conexionBD.conexion.commit()
                return True
            except:
                return False
        @staticmethod
        def ver_productos():
            try:
                conexionBD.cursor.execute("select * from products")
                resultados=conexionBD.cursor.fetchall()
                return resultados
            except:
                return False
        @staticmethod
        def modificar_producto(product_name,unit_price):
            try:
                conexionBD.cursor.execute(
                    "update products set nombre=%s, precio=%s where id_producto=%s",
                    (product_name,unit_price)
                )
                conexionBD.conexion.commit()
                return True
            except:
                return False
    
        
