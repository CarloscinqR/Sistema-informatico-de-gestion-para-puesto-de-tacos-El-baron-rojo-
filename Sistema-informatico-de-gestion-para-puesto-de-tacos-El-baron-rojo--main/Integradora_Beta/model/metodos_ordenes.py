import conexionBD
from tkinter import *
from tkinter import messagebox


class Ordenes_acciones():
    @staticmethod
    def agregar(total,cliente):
        try:
            conexionBD.cursor.execute(
                "insert into user (id_order,date,total,costumer_name) values (null,NOW(),%s, %s,)",
                (total,cliente)
            )
            conexionBD.conexion.commit()
            return True
        except:
            return False
        

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
    @staticmethod
    def agregar_ingredientes(id_producto, ingredientes_dict):
        """
        Inserta ingredientes ligados a un producto.
        ingredientes_dict debe ser un diccionario {nombre: cantidad}
        """
        try:
            for nombre, cantidad in ingredientes_dict.items():
                unidad = "u"  # puedes cambiar a "g", "ml", etc. según tu modelo
                conexionBD.cursor.execute(
                    "INSERT INTO ingredients (name, quantity, measurement_unit, id_product) VALUES (%s, %s, %s, %s)",
                    (nombre, cantidad, unidad, id_producto)
                )
            conexionBD.conexion.commit()
            return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron agregar los ingredientes: {e}")
            return False
