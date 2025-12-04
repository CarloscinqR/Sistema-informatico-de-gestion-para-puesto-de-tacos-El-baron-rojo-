import conexionBD
from tkinter import *
from tkinter import messagebox
import hashlib


class Usuarios_acciones():
    @staticmethod
    def agregar(username,password,role):
        try:
            password=hashlib.sha256(password.encode()).hexdigest()
            conexionBD.cursor.execute(
                "insert into user (id_user,username,password,creation_date,delete_date,status,role) values (null,%s, %s,NOW(),0000-00-00,1,%s)",
                (username,password,role)
            )
            conexionBD.conexion.commit()
            return True
        except:
            return False
        
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
    def modificar_usuario(nuevo_nombre, nueva_pass,nuevo_rol,id_user):
        try:
            conexionBD.cursor.execute(
                "UPDATE user SET username=%s, password=%s, role=%s WHERE id_user=%s",
                (nuevo_nombre, nueva_pass, nuevo_rol,id_user)
            )
            conexionBD.conexion.commit()
            return True
        except:
            return False
            
    @staticmethod
    def borrar(id_user):
        try:
            conexionBD.cursor.execute(
                "delete from user where id_user=%s",
                (id_user,)
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
    def verificar_usuario(username,password):
        try:
            conexionBD.cursor.execute(
                "SELECT * FROM user WHERE username=%s AND password=%s",
                (username,password)
            )
            fila_encontrada = conexionBD.cursor.fetchone()
            if fila_encontrada is not None:
                return True
            else:
                messagebox.showerror("Error",f"Usuario o Contraseña incorrectos")
        except Exception as e:
            messagebox.showerror("Error",f"Error al verificar: {e}")
            return False
