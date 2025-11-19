import conexionBD
from tkinter import *
from tkinter import messagebox
import ver_usuarios

class Usuarios_acciones:
    def __init__(self,nombre,contrasenia):
        self._nombre=nombre
        self._contrasenia=contrasenia

    @property
    def nombre(self):
        return self._nombre
    @nombre.setter
    def nombre(self, nombre):
        self._nombre = nombre
    @property
    def contrasenia(self):
        return self._contrasenia
    @contrasenia.setter
    def contrasenia(self, contrasenia):
        self._contrasenia = contrasenia

#faltan mas atributos por agregar
    @staticmethod
    def agregar(nombre,contrasenia):
        try:
            conexionBD.cursor.execute(
                "insert into users (nombre, contrasenia) values (%s, %s)",
                (nombre.get(), contrasenia.get())
            )
            conexionBD.conexion.commit()
            return True
        except:
            return False
    @staticmethod
    def mostrar_usuarios():
        try:
            conexionBD.cursor.execute("SELECT id, nombre, contrasenia FROM users")
            usuarios = conexionBD.cursor.fetchall()

            texto_usuarios = ""
            for usuario in usuarios:
                texto_usuarios += f"ID: {usuario[0]}, Nombre: {usuario[1]}, Contraseña: {usuario[2]}\n"

            etiqueta_usuarios = Label(ver_usuarios.contenedor_botones, text=texto_usuarios, font=("Inter", 16), bg="white", justify=LEFT)
            etiqueta_usuarios.pack(padx=20, pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener usuarios: {e}")
    @staticmethod
    def modificar_usuario(id_usuario, nuevo_nombre, nueva_contrasenia):
        try:
            conexionBD.cursor.execute(
                "UPDATE users SET nombre=%s, contrasenia=%s WHERE id=%s",
                (nuevo_nombre, nueva_contrasenia, id_usuario)
            )
            conexionBD.conexion.commit()
            return True
        except:
            return False