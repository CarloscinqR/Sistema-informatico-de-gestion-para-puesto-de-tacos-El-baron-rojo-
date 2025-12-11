import conexionBD
from tkinter import *
from tkinter import messagebox
import hashlib


class Usuarios_acciones():
    @staticmethod
    def agregar(username,password,password2,role):
        print(username)
        if password==password2:
            try:
                password=hashlib.sha256(password.encode()).hexdigest()
                print(password)
                conexionBD.cursor.execute(
                    "insert into user (id_user,username,password,creation_date,delete_date,status,role) values (null,%s, %s,NOW(),0000-00-00,1,%s)",
                    (username,password,role)
                )
                conexionBD.conexion.commit()
                return True
            except:
                return False
        else:
            messagebox.showwarning(message="Las contraseñas deben de ser iguales")
            return
    @staticmethod
    def mostrar_usuarios():
        try:
            conexionBD.cursor.execute("SELECT * FROM products")
            productos = conexionBD.cursor.fetchall()

            texto_productos = ""
            for producto in productos:
                texto_productos += f"ID: {producto[0]}, Nombre: {producto[1]}, Precio Unitario: {producto[2]}\n"
            etiqueta_productos = Label(productos.contenedor_botones, text=texto_productos, font=("Inter", 16), bg="white", justify=LEFT)
            etiqueta_productos.pack(padx=20, pady=10)
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener productos: {e}")

    @staticmethod
    def obtener_usuarios():
        try:
            conexionBD.cursor.execute("SELECT * FROM user")
            usuarios = conexionBD.cursor.fetchall()
            return usuarios
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener usuarios: {e}")
            return []

    @staticmethod
    def modificar_usuario(nuevo_nombre, nueva_pass,nueva_pass2,nuevo_rol,id_user):
        if nueva_pass==nueva_pass2:
            nueva_pass=hashlib.sha256(nueva_pass.encode()).hexdigest()
            try:
                conexionBD.cursor.execute(
                    "UPDATE user SET username=%s, password=%s, role=%s WHERE id_user=%s",
                    (nuevo_nombre, nueva_pass, nuevo_rol,id_user)
                )
                conexionBD.conexion.commit()
                return True
            except:
                return False
        else:
            messagebox.showwarning(message="Las contraseñas deben de ser iguales")
            return
    @staticmethod
    def borrar(id_user):
        try:
            conexionBD.cursor.execute(
                "UPDATE user SET delete_date=NOW(), status=0 where id_user=%s",
                (id_user,)
            )
            conexionBD.conexion.commit()

            return True
        except Exception:
            return False

    @staticmethod
    def verificar_usuario(username,password):
        password=hashlib.sha256(password.encode()).hexdigest()
        try:
            # Buscar por usuario+password y obtener todos los campos
            conexionBD.cursor.execute(
                "SELECT * FROM user WHERE username=%s AND password=%s",
                (username,password)
            )
            fila = conexionBD.cursor.fetchone()
            if fila is None:
                # credenciales incorrectas
                messagebox.showerror("Error", "Usuario o Contraseña incorrectos")
                return False

            # campo 'status' esperado en posición 5
            try:
                status_int = int(fila[5])
            except Exception:
                status_int = 0

            if status_int == 0:
                messagebox.showerror("Error", "Este usuario ha sido eliminado y no puede iniciar sesión.")
                return False

            # Retornar la fila completa para que el llamador conozca el rol
            return fila
        except Exception as e:
            messagebox.showerror("Error",f"Error al verificar: {e}")
            return False