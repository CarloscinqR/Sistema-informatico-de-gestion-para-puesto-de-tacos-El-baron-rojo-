import conexionBD
from tkinter import *
from tkinter import messagebox

class Ingredientes_acciones:
    @staticmethod
    def agregar(name, quantity, measurement_unit, id_product):
        try:
            conexionBD.cursor.execute(
                "INSERT INTO ingredients (name, quantity, measurement_unit, id_product) VALUES (%s, %s, %s, %s)",
                (name, quantity, measurement_unit, id_product)
            )
            conexionBD.conexion.commit()
            return conexionBD.cursor.lastrowid
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar ingrediente: {e}")
            return False
                

    @staticmethod
    def mostrar_ingredientes(contenedor_botones):
        try:
            conexionBD.cursor.execute("SELECT * FROM ingredients")
            ingredientes = conexionBD.cursor.fetchall()

            texto_ingrediente = ""
            for ingrediente in ingredientes:
                texto_ingrediente += (
                    f"ID: {ingrediente[0]}, "
                    f"Nombre: {ingrediente[1]}, "
                    f"Cantidad: {ingrediente[2]}, "
                    f"Unidad: {ingrediente[3]}, "
                    f"ID_Product: {ingrediente[4]}\n"
                )

            etiqueta_ingredientes = Label(
                contenedor_botones,
                text=texto_ingrediente,
                font=("Inter", 16),
                bg="white",
                justify=LEFT
            )
            etiqueta_ingredientes.pack(padx=20, pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener ingredientes: {e}")

    @staticmethod
    def obtener_ingredientes():
        try:
            conexionBD.cursor.execute("SELECT * FROM ingredients")
            ingredientes = conexionBD.cursor.fetchall()
            return ingredientes
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener ingredientes: {e}")
            return []

    @staticmethod
    def modificar(name, quantity, measurement_unit, id_product, id_ingredient):
        try:
            conexionBD.cursor.execute(
                "UPDATE ingredients SET name=%s, quantity=%s, measurement_unit=%s, id_product=%s WHERE id_ingredient=%s",
                (name, quantity, measurement_unit, id_product, id_ingredient)
            )
            conexionBD.conexion.commit()
            try:
                return conexionBD.cursor.rowcount > 0
            except Exception:
                return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar ingrediente: {e}")
            return False

    @staticmethod
    def borrar(id_ingredient):
        try:
            conexionBD.cursor.execute(
                "DELETE FROM ingredients WHERE id_ingredient=%s",
                (id_ingredient,)
            )
            conexionBD.conexion.commit()
            try:
                return conexionBD.cursor.rowcount > 0
            except Exception:
                return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo borrar ingrediente: {e}")
            return False
