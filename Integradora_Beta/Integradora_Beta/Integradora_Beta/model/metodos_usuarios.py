import conexionBD
from tkinter import *
from tkinter import messagebox


class Usuarios_acciones():
    @staticmethod
    def agregar(username,password,role):
        try:
            conexionBD.cursor.execute(
                "insert into user (username,password,creation_date,delete_date,status,role) values (null,%s, %s,NOW(),0000-00-00,1,%s)",
                (username,password,role,)
            )
            conexionBD.conexion.commit()
            return True
        except:
            return False
        
    @staticmethod
    def mostrar_usuarios():
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
    def obtener_usuarios():
        try:
            conexionBD.cursor.execute("SELECT * FROM user")
            usuarios = conexionBD.cursor.fetchall()
            return usuarios
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener usuarios: {e}")
            return []

    @staticmethod
    def modificar_usuario(id_product, nuevo_nombre, nuevo_precio):
        try:
            conexionBD.cursor.execute(
                "UPDATE products SET prduct_name=%s, unit_price=%s WHERE id_prduct=%s",
                (nuevo_nombre, nuevo_precio, id_product)
            )
            conexionBD.conexion.commit()
            return True
        except:
            return False