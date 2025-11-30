import conexionBD
from tkinter import *
from tkinter import messagebox


class Productos_acciones():
    @staticmethod
    def agregar(prduct_name,unit_price,products_category=None,id_product=None):
        try:
            # Insert product including optional category. We keep id_product
            # as the first column so backward-compatible calls continue to work
            # if id_product is passed explicitly (or None).
            conexionBD.cursor.execute(
                "INSERT INTO products (id_product, product_name, products_category, unit_price) VALUES (%s, %s, %s, %s)",
                (id_product, prduct_name, products_category, unit_price)
            )
            conexionBD.conexion.commit()
            try:
                return conexionBD.cursor.lastrowid
            except Exception:
                return False
        except:
            return False
        
    @staticmethod
    def mostrar_productos():
        try:
            conexionBD.cursor.execute("SELECT * FROM products")
            productos = conexionBD.cursor.fetchall()

            texto_productos = ""
            for producto in productos:
                # DB order: id_product, product_name, products_category, unit_price
                texto_productos += f"ID: {producto[0]}, Nombre: {producto[1]}, Precio Unitario: {producto[3]}\n"
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
    def modificar_producto(nuevo_nombre, nuevo_precio, id_product=None, products_category=None):
        try:
            # Update product information; category is optional
            if products_category is None:
                conexionBD.cursor.execute(
                    "UPDATE products SET product_name=%s, unit_price=%s WHERE id_product=%s",
                    (nuevo_nombre, nuevo_precio, id_product)
                )
            else:
                # update name, category and price; column name is products_category
                conexionBD.cursor.execute(
                    "UPDATE products SET product_name=%s, products_category=%s, unit_price=%s WHERE id_product=%s",
                    (nuevo_nombre, products_category, nuevo_precio, id_product)
                )
            conexionBD.conexion.commit()
            return True
        except:
            return False
        
    @staticmethod
    def borrar(id_product):
        try:
            conexionBD.cursor.execute(
                "DELETE FROM products WHERE id_product=%s",
                (id_product,)
            )
            conexionBD.conexion.commit()
            # Si rowcount > 0, se eliminó algo
            try:
                return conexionBD.cursor.rowcount > 0
            except Exception:
                return True
        except Exception:
            return False

    @staticmethod
    def agregar_ingredientes_detalle(id_product, ingredient_id):
        try:
            inserted_any = False
            for id_ingredients in ingredient_id:
                try:
                    conexionBD.cursor.execute(
                        "INSERT INTO ingredients_details (id_ingredients, id_product) VALUES (%s, %s)",
                        (id_ingredients, id_product)
                    )
                    inserted_any = True
                except Exception:
                    # seguir intentando con los demás
                    pass
            if inserted_any:
                conexionBD.conexion.commit()
                return True
            return False
        except Exception:
            return False
