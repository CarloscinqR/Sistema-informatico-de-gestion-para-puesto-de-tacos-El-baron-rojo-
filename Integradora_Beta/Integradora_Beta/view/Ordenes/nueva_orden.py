from tkinter import *

class nuevaorden():
    @staticmethod
    def nueva_orden_(menu_ordenes):
        menu_ordenes.destroy()
        nueva_orden=Tk()
        nueva_orden.title("Nueva orden")
        nueva_orden.geometry("1920x1080")
        nueva_orden.state("zoomed")

        fondo=Frame(nueva_orden, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        header=Frame(fondo, bg="#A6171C", height=180)
        header.pack(side=TOP, fill=X)

        def volver_a_menu():
            from view.Ordenes.menu_ordenes import menuordenes
            menuordenes.menu_ordenes_(nueva_orden)

        regresar=Button(header, text="Regresar", font=("Inter", 24), fg="#A6171C", bg="#F1C045", command=volver_a_menu)
        regresar.pack(padx=20, pady=10, fill="x", side=LEFT, expand=True)
        
        alimentos=Button(header, text="Alimentos", font=("Inter", 24), fg="#A6171C", bg="#F1C045")
        alimentos.pack(padx=20, pady=10, fill="x", side=LEFT, expand=True)
        
        especiales=Button(header, text="Especiales", font=("Inter", 24), fg="#A6171C", bg="#F1C045")
        especiales.pack(padx=20, pady=10, fill="x", side=LEFT, expand=True)

        bebidas=Button(header, text="Bebidas", font=("Inter", 24), fg="#A6171C", bg="#F1C045")
        bebidas.pack(padx=20, pady=10, fill="x", side=LEFT, expand=True)
        
        confirmar=Button(header, text="Confirmar", font=("Inter", 24), fg="#A6171C", bg="#F1C045")
        confirmar.pack(padx=20, pady=10, fill="x", side=LEFT, expand=True)

        contenedor_botones_productos=Frame(fondo, bg="#D6D0C5")
        contenedor_botones_productos.grid()


