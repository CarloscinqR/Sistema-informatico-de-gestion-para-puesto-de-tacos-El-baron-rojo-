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
            conexionBD.cursor.execute("SELECT * FROM products ")
            productos = conexionBD.cursor.fetchall()
            return productos
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener productos: {e}")
            return []
        
    @staticmethod
    def obtener_especiales():
        try:
            conexionBD.cursor.execute("SELECT * FROM products where products_category = 'Especiales' ")
            productos = conexionBD.cursor.fetchall()
            return productos
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener productos: {e}")
            return []
        
    @staticmethod
    def obtener_bebidas():
        try:
            conexionBD.cursor.execute("SELECT * FROM products where products_category = 'Bebida' ")
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
    def obtener_ingredientes():
        try:
            conexionBD.cursor.execute("SELECT id_ingredients, name FROM ingredients")
            return conexionBD.cursor.fetchall()
        except Exception as e:
            print("ERROR OBTENER INGREDIENTES:", e)
            return []

    @staticmethod
    def borrar(id_product):
        try:
            # borrar relaciones con ingredientes
            conexionBD.cursor.execute(
                "DELETE FROM ingredients_details WHERE id_product = %s",
                (id_product,)
            )

            # borrar relaciones con pedidos
            conexionBD.cursor.execute(
                "DELETE FROM detail_order WHERE id_product = %s",
                (id_product,)
            )

            # borrar producto
            conexionBD.cursor.execute(
                "DELETE FROM products WHERE id_product = %s",
                (id_product,)
            )

            conexionBD.conexion.commit()
            return True
        except Exception as e:
            print("ERROR AL BORRAR PRODUCTO:", e)
            return False


    @staticmethod
    def agregar_ingredientes_detalle(id_product, ingredientes):
        try:
            inserted_any = False

            for id_ing, cantidad in ingredientes:
                try:
                    conexionBD.cursor.execute(
                        "INSERT INTO ingredients_details (id_ingredients, id_product, quantity) VALUES (%s, %s, %s)",(id_ing, id_product, cantidad))
                    inserted_any = True
                except Exception as e:
                    print(f"ERROR INGREDIENTE (id={id_ing}):", e)
                    # continúa con los demás
            if inserted_any:
                conexionBD.conexion.commit()
                return True

            return False

        except Exception as e:
            print("ERROR GENERAL:", e)
            return False


    @staticmethod
    def obtener_ingredientes_producto(id_product):
        try:
            conexionBD.cursor.execute("SELECT id_ingredients FROM ingredients_details WHERE id_product = %s", (id_product,))
            data = conexionBD.cursor.fetchall()
            conexionBD.conexion.commit()
            return [int(i[0]) for i in data]
        except:
            return []

    @staticmethod
    def actualizar_ingredientes(id_producto, ingredientes):
        try:
            conexionBD.cursor.execute("DELETE FROM ingredients_details WHERE id_product = %s",(id_producto,))
            for id_ing, cantidad in ingredientes:
                conexionBD.cursor.execute("INSERT INTO ingredients_details (id_product, id_ingredients, quantity) VALUES (%s, %s, %s)",(id_producto, id_ing, cantidad))
            conexionBD.conexion.commit()
            return True

        except Exception as e:
            print("ERROR actualizar_ingredientes:", e)
            return False

    
