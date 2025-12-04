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
    def obtener_detalles_orden(id_order):
        """Obtiene los detalles de una orden con información del producto."""
        try:
            # Convertir id_order a int por si viene como string
            id_order = int(id_order)
            conexionBD.cursor.execute("""
                SELECT do.amount, p.id_product, p.product_name, p.unit_price, (do.amount * p.unit_price) as subtotal
                FROM detail_order do
                JOIN products p ON do.id_product = p.id_product
                WHERE do.id_order = %s
            """, (id_order,))
            detalles = conexionBD.cursor.fetchall()
            return detalles if detalles else []
        except Exception as e:
            print(f"Error al obtener detalles: {e}")
            return []
    
    @staticmethod
    def obtener_ordenes_por_fecha(fecha):
        """Obtiene todas las órdenes de una fecha específica."""
        try:
            conexionBD.cursor.execute("SELECT * FROM orders WHERE date = %s", (fecha,))
            ordenes = conexionBD.cursor.fetchall()
            return ordenes
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener ordenes: {e}")
            return []
        
    @staticmethod
    def agregar_orden():
        pass

    @staticmethod
    def actualizar_orden(id_order, total, cliente):
        """Actualiza los datos básicos de una orden existente."""
        try:
            conexionBD.cursor.execute(
                "UPDATE orders SET total=%s, costumer_name=%s WHERE id_order=%s",
                (total, cliente, id_order)
            )
            conexionBD.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar orden: {e}")
            return False

    @staticmethod
    def reemplazar_detalles(id_order, items):
        """Reemplaza los detalles de una orden: borra los actuales y agrega los nuevos.
        `items` es un dict {id_product: {"qty": int, "name":..., "unit": ...}}
        """
        try:
            # borrar detalles existentes
            conexionBD.cursor.execute("DELETE FROM detail_order WHERE id_order=%s", (id_order,))
            inserted = False
            for pid, v in items.items():
                try:
                    qty = int(v.get("qty", 0))
                    conexionBD.cursor.execute(
                        "INSERT INTO detail_order (amount, id_product, id_order) VALUES (%s, %s, %s)",
                        (qty, pid, id_order)
                    )
                    inserted = True
                except Exception:
                    pass

            if inserted:
                conexionBD.conexion.commit()
                return True
            else:
                # Si no se insertó nada, igualmente commit para confirmar el DELETE
                conexionBD.conexion.commit()
                return True
        except Exception as e:
            print(f"Error al reemplazar detalles: {e}")
            return False

    @staticmethod
    def eliminar_orden(id_order):
        """Elimina una orden y sus detalles de la base de datos."""
        try:
            id_order = int(id_order)
            # eliminar detalles primero
            conexionBD.cursor.execute("DELETE FROM detail_order WHERE id_order=%s", (id_order,))
            # eliminar orden
            conexionBD.cursor.execute("DELETE FROM orders WHERE id_order=%s", (id_order,))
            conexionBD.conexion.commit()
            return True
        except Exception as e:
            print(f"Error al eliminar orden: {e}")
            return False

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
