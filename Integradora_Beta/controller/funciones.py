from tkinter import messagebox
class Controladores():
    @staticmethod
    def respuesta_sql(titulo,respuesta):
        if respuesta:
            messagebox.showinfo(title=titulo,message="La accion se ha realizado con exito")
        else:
            messagebox.showinfo(title="Algo ha salido mal",message="La accion no se ha podido realizar",icon="warning")