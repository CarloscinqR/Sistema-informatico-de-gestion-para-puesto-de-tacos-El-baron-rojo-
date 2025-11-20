from tkinter import *
class verordenes():
    @staticmethod
    def ver_ordenes_(menu_ordenes):
        menu_ordenes.destroy()
        ver_ordenes=Tk()
        ver_ordenes.title("Ver ordenes")
        ver_ordenes.geometry("1920x1080")
        ver_ordenes.state("zoomed")

        fondo=Frame(ver_ordenes, bg="#D6D0C5")
        fondo.pack_propagate(False)
        fondo.pack(fill="both", expand=True)

        fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
        fondo2.pack_propagate(False)
        fondo2.pack(padx=99, pady=50)

        contenedor_botones=Frame(fondo2, bg="#A6171C", width=550, height=790)
        contenedor_botones.pack_propagate(False)
        contenedor_botones.pack(padx=300, pady=20)

        titulo=Label(contenedor_botones, text="Ver ordenes",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
        titulo.pack(padx=20, pady=20)
        
        def volver_a_menu():
            from view.Ordenes.menu_ordenes import menuordenes
            menuordenes.menu_ordenes_(ver_ordenes)

        fecha=Label(contenedor_botones, text="Fecha", font=("Inter", 24), bg="white")
        fecha.pack(padx=20, pady=10)

        fecha_entry=Entry(contenedor_botones, font=("Inter", 24), bg="white")
        fecha_entry.pack(padx=20, pady=10)

        regresar=Button(contenedor_botones, text="Regresar", font=("Inter", 24), bg="#F1C045", command=volver_a_menu)
        regresar.pack(padx=20, pady=10)

