from tkinter import messagebox
class Controladores():
    @staticmethod
    def respuesta_sql(titulo,respuesta):
        if respuesta:
            messagebox.showinfo(title=titulo,message="La accion se ha realizado con exito")
        else:
            messagebox.showinfo(title="Algo ha salido mal",message="La accion no se ha podido realizar",icon="warning")


# Valor global para mantener el rol del usuario actualmente logueado
current_user_role = None

def set_current_user_role(role):
    global current_user_role
    current_user_role = role

def get_current_user_role():
    return current_user_role


class Validadores:
    """Pequeños validadores usados por las vistas (nombre, unidad de medida)."""

    @staticmethod
    def validar_nombre(nombre: str):
        if nombre is None:
            return False, "Nombre inválido"
        nombre = nombre.strip()
        if nombre == "":
            return False, "El nombre no puede estar vacío"
        if len(nombre) < 2:
            return False, "El nombre es demasiado corto"
        if len(nombre) > 100:
            return False, "El nombre es demasiado largo"
        return True, ""

    @staticmethod
    def validar_unidad_medida(unidad: str):
        if unidad is None:
            return False, "Unidad inválida"
        unidad = unidad.strip()
        if unidad == "":
            return False, "La unidad no puede estar vacía"
        if len(unidad) < 1:
            return False, "Unidad inválida"
        if len(unidad) > 30:
            return False, "Unidad demasiado larga"
        # opcional: permitir solo letras, números y espacios
        return True, ""