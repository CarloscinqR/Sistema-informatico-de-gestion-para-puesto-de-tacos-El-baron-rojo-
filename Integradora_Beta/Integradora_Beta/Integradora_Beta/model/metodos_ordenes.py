import conexionBD
from tkinter import *
from tkinter import messagebox


class Ordenes_acciones():
    #@staticmethod
    # def agregar(username,password,role):
    #     try:
    #         conexionBD.cursor.execute(
    #             "insert into user (username,password,creation_date,delete_date,status,role) values (null,%s, %s,NOW(),0000-00-00,1,%s)",
    #             (username,password,role,)
    #         )
    #         conexionBD.conexion.commit()
    #         return True
    #     except:
    #         return False
        
    @staticmethod
    def mostrar_ordenes():
        try:
            conexionBD.cursor.execute("SELECT * FROM orders")
            ordenes = conexionBD.cursor.fetchall()

            texto_ordenes = ""
            for orden in ordenes:
                texto_ordenes += f"ID: {orden[0]}, Fecha: {orden[1]}, Precio Total: {orden[2]}, Cliente: {orden[3]}\n"
            etiqueta_ordenes = Label(ordenes.contenedor_botones, text=texto_ordenes, font=("Inter", 16), bg="white", justify=LEFT)
            etiqueta_ordenes.pack(padx=20, pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener ordenes: {e}")

    @staticmethod
    def obtener_ordenes():
        try:
            conexionBD.cursor.execute("SELECT * FROM orders")
            ordenes = conexionBD.cursor.fetchall()
            return ordenes
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener ordenes: {e}")
            return []

    # @staticmethod
    # def modificar_usuario(id_product, nuevo_nombre, nuevo_precio):
    #     try:
    #         conexionBD.cursor.execute(
    #             "UPDATE products SET prduct_name=%s, unit_price=%s WHERE id_prduct=%s",
    #             (nuevo_nombre, nuevo_precio, id_product)
    #         )
    #         conexionBD.conexion.commit()
    #         return True
    #     except:
    #         return False