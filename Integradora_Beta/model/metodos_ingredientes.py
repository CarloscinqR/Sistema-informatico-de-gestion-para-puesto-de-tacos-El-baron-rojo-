import conexionBD
from tkinter import *
from tkinter import messagebox

class Ingredientes_acciones:
    @staticmethod
    def agregar(name, measurement_unit):
        try:
            # name, measurement_unit, id_product and quantity are required
            if not name or not measurement_unit:
                messagebox.showerror("Error", "Nombre y unidad de medida son requeridos.")
                return False

            
            # Insert into ingredients table (only has: id_ingredients, name, measurement_unit)
            conexionBD.cursor.execute(
                "INSERT INTO ingredients (name, measurement_unit) VALUES (%s, %s)",
                (name, measurement_unit)
            )
            ing_id = conexionBD.cursor.lastrowid
            
            
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
                    f"Unidad: {ingrediente[2]}\n"
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
            # Get ingredients with their quantity from ingredients_details
            conexionBD.cursor.execute("""
                SELECT * from ingredients
            """)
            ingredientes = conexionBD.cursor.fetchall()
            return ingredientes
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener ingredientes: {e}")
            return []

    
    @staticmethod
    def modificar(name, measurement_unit, id_ingredient, id_product, quantity):
        try:
            # Validate id_ingredient exists
            conexionBD.cursor.execute("SELECT id_ingredients FROM ingredients WHERE id_ingredients=%s", (id_ingredient,))
            if not conexionBD.cursor.fetchone():
                msg = "Ingrediente no existe en la base de datos"
                messagebox.showerror("Error", msg)
                return False, msg

            # Validate product and quantity are provided
            if id_product is None:
                msg = "Producto es requerido."
                messagebox.showerror("Error", msg)
                return False, msg
            
            # Validate provided product id exists in products table (FK constraint)
            try:
                idp = int(id_product)
            except Exception:
                msg = "ID de producto inválido."
                messagebox.showerror("Error", msg)
                return False, msg
            
            conexionBD.cursor.execute("SELECT id_product FROM products WHERE id_product=%s", (idp,))
            if not conexionBD.cursor.fetchone():
                msg = "No existe product con el ID proporcionado."
                messagebox.showerror("Error", msg)
                return False, msg
            
            # Ensure quantity is numeric and provided
            try:
                qty_int = int(quantity) if quantity else 0
            except Exception:
                msg = "Cantidad inválida."
                messagebox.showerror("Error", msg)
                return False, msg

            # Update ingredient (only has: id_ingredients, name, measurement_unit)
            conexionBD.cursor.execute(
                "UPDATE ingredients SET name=%s, measurement_unit=%s WHERE id_ingredients=%s",
                (name, measurement_unit, id_ingredient)
            )
            rows_updated = conexionBD.cursor.rowcount

            # Update or insert ingredients_details
            conexionBD.cursor.execute(
                "UPDATE ingredients_details SET id_product=%s, quntity=%s WHERE id_ingredients=%s",
                (idp, qty_int, id_ingredient)
            )
            if conexionBD.cursor.rowcount == 0:
                # No existing detail row: insert one
                conexionBD.cursor.execute(
                    "INSERT INTO ingredients_details (id_ingredients, id_product, quntity) VALUES (%s, %s, %s)",
                    (id_ingredient, idp, qty_int)
                )

            conexionBD.conexion.commit()
            return True, None
        except Exception as e:
            # Provide detailed error to help debugging
            try:
                conexionBD.conexion.rollback()
            except Exception:
                pass
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
