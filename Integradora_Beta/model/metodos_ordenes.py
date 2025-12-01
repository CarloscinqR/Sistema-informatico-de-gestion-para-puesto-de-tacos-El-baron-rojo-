import conexionBD
from tkinter import *
from tkinter import messagebox


class Ordenes_acciones():
    @staticmethod
    def agregar(total, cliente):
        """Inserta una orden en la tabla `orders` y devuelve el `id_order` insertado o False en error."""
        try:
            conexionBD.cursor.execute(
                "INSERT INTO orders (date, total, costumer_name) VALUES (NOW(), %s, %s)",
                (total, cliente)
            )
            conexionBD.conexion.commit()
            try:
                return conexionBD.cursor.lastrowid
            except Exception:
                return False
        except Exception as e:
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
        
    @staticmethod
    def agregar_orden():
        pass

    @staticmethod
    def agregar_detalles(id_order, items):
        """Inserta los detalles de la orden en `detail_order`.
        `items` debe ser un dict con clave=id_product y valor dict {"qty": int}.
        Devuelve True si al menos uno se insertó, False si hubo error.
        """
        try:
            inserted = False
            for pid, v in items.items():
                try:
                    qty = int(v.get("qty", 0))
                    # insertar cada detalle (amount, id_product, id_order)
                    conexionBD.cursor.execute(
                        "INSERT INTO detail_order (amount, id_product, id_order) VALUES (%s, %s, %s)",
                        (qty, pid, id_order)
                    )
                    inserted = True
                except Exception:
                    # ignorar detalle fallido y continuar
                    pass

            if inserted:
                conexionBD.conexion.commit()
                return True
            return False
        except Exception:
            return False

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
