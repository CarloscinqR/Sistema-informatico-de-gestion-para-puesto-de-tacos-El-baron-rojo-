import conexionBD
from tkinter import *
from tkinter import messagebox


class Productos_acciones():
    @staticmethod
    def agregar(prduct_name,unit_price,id_product):
        try:
            conexionBD.cursor.execute(
                "insert into products (id_prduct,prduct_name,unit_price) values (%s,%s, %s)",
                (id_product,prduct_name, unit_price,)
            )
            conexionBD.conexion.commit()
            return True
        except:
            return False
        
    @staticmethod
    def mostrar_productos():
        try:
            conexionBD.cursor.execute("SELECT * FROM products")
            productos = conexionBD.cursor.fetchall()

            texto_productos = ""
            for producto in productos:
                texto_productos += f"ID: {producto[0]}, Nombre: {producto[1]}, Precio Unitario: {producto[2]}\n"
            etiqueta_productos = Label(productos.contenedor_botones, text=texto_productos, font=("Inter", 16), bg="white", justify=LEFT)
            etiqueta_productos.pack(padx=20, pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener productos: {e}")

    @staticmethod
    def obtener_productos():
        try:
            conexionBD.cursor.execute("SELECT * FROM products")
            productos = conexionBD.cursor.fetchall()
            return productos
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener productos: {e}")
            return []

    @staticmethod
    def modificar_producto(id_product, nuevo_nombre, nuevo_precio):
        try:
            conexionBD.cursor.execute(
                "UPDATE products SET prduct_name=%s, unit_price=%s WHERE id_prduct=%s",
                (nuevo_nombre, nuevo_precio, id_product)
            )
            conexionBD.conexion.commit()
            return True
        except:
            return False