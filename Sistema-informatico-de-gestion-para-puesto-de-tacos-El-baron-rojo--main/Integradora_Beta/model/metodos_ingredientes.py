import conexionBD
from tkinter import messagebox

class ingredientes_uwu():
    @staticmethod
    def agregar(prduct_name,unit_price,id_product=None):
        try:
            conexionBD.cursor.execute(
                "insert into products (id_product,product_name,unit_price) values (%s,%s, %s)",
                (id_product,prduct_name, unit_price,)
            )
            conexionBD.conexion.commit()
            return True
        except:
            return False