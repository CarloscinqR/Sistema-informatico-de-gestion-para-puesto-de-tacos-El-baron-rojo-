import conexionBD
from tkinter import *
from tkinter import messagebox

class Ingredientes_acciones:
    @staticmethod
    def agregar(name, quantity, measurement_unit, id_product):
        try:
            # Validate product id exists (to avoid FK error)
            if id_product is None:
                messagebox.showerror("Error", "ID de producto requerido.")
                return False
            try:
                idp = int(id_product)
            except Exception:
                messagebox.showerror("Error", "ID de producto inválido.")
                return False
            conexionBD.cursor.execute("SELECT id_product FROM products WHERE id_product=%s", (idp,))
            if not conexionBD.cursor.fetchone():
                messagebox.showerror("Error", "Producto no existe.")
                return False

            # Begin insert into ingredients then details, commit once
            conexionBD.cursor.execute(
                "INSERT INTO ingredients (name, quantity, measurement_unit, id_product) VALUES (%s, %s, %s, %s)",
                (name, quantity, measurement_unit, idp)
            )
            ing_id = conexionBD.cursor.lastrowid
            # correlate in ingredients_details
            conexionBD.cursor.execute(
                "INSERT INTO ingredients_details (id_ingredients, id_product) VALUES (%s, %s)",
                (ing_id, idp)
            )
            conexionBD.conexion.commit()
            return ing_id
        except Exception as e:
            try:
                conexionBD.conexion.rollback()
            except Exception:
                pass
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
            # Validate id_ingredient exists
            conexionBD.cursor.execute("SELECT id_ingredients FROM ingredients WHERE id_ingredients=%s", (id_ingredient,))
            if not conexionBD.cursor.fetchone():
                messagebox.showerror("Error", "Ingrediente no existe en la base de datos")
                return False

            # Validate provided product id exists in products table (FK constraint)
            if id_product is not None:
                try:
                    idp = int(id_product)
                except Exception:
                    messagebox.showerror("Error", "ID de producto inválido.")
                    return False
                conexionBD.cursor.execute("SELECT id_product FROM products WHERE id_product=%s", (idp,))
                if not conexionBD.cursor.fetchone():
                    messagebox.showerror("Error", "No existe product con el ID proporcionado.")
                    return False
            # Ensure quantity is numeric
            try:
                qty_int = int(float(quantity)) if quantity is not None else 0
            except Exception:
                msg = "Cantidad inválida."
                messagebox.showerror("Error", msg)
                return False, msg

            # No explicit length validation for measurement_unit (DB schema governs actual limits)

            # Update ingredient
            conexionBD.cursor.execute(
                "UPDATE ingredients SET name=%s, quantity=%s, measurement_unit=%s, id_product=%s WHERE id_ingredients=%s",
                (name, qty_int, measurement_unit, idp if id_product is not None else None, id_ingredient)
            )
            rows_updated = conexionBD.cursor.rowcount

            # If a product id was provided, make sure ingredients_details is correlated
            if id_product is not None:
                # Try to update an existing detail entry; otherwise insert a new one
                conexionBD.cursor.execute(
                    "UPDATE ingredients_details SET id_product=%s WHERE id_ingredients=%s",
                    (idp, id_ingredient)
                )
                if conexionBD.cursor.rowcount == 0:
                    # No existing detail row: insert one
                    conexionBD.cursor.execute(
                        "INSERT INTO ingredients_details (id_ingredients, id_product) VALUES (%s, %s)",
                        (id_ingredient, idp)
                    )

            conexionBD.conexion.commit()
            try:
                return rows_updated > 0, None
            except Exception:
                return True, None
        except Exception as e:
            # Provide detailed error to help debugging
            msg = f"No se pudo modificar ingrediente: {e}"
            messagebox.showerror("Error", msg)
            print(f"ERROR modificar ingrediente: {e}")
            return False, msg

    @staticmethod
    def borrar(id_ingredient):
        try:
            # Remove any ingredient detail relations first to avoid FK errors
            try:
                conexionBD.cursor.execute("DELETE FROM ingredients_details WHERE id_ingredients=%s", (id_ingredient,))
                # do not commit here specifically; we will commit after deleting ingredient
            except Exception:
                pass

            # correct column name per schema is `id_ingredients`
            conexionBD.cursor.execute(
                "DELETE FROM ingredients WHERE id_ingredients=%s",
                (id_ingredient,)
            )
            conexionBD.conexion.commit()
            try:
                return conexionBD.cursor.rowcount > 0
            except Exception:
                return True
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo borrar ingrediente: {e}")
            print(f"ERROR borrar ingrediente: {e}")
            return False
