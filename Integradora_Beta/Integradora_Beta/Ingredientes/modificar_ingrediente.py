from tkinter import *
from tkinter import ttk

def modificar_ingrediente_(menu_ingrediente):
    menu_ingrediente.destroy()
    modificar_ingrediente=Tk()
    modificar_ingrediente.title("Modificar ingrediente")
    modificar_ingrediente.geometry("1920x1080")
    modificar_ingrediente.state("zoomed")

    fondo=Frame(modificar_ingrediente, bg="#D6D0C5")
    fondo.pack_propagate(False)
    fondo.pack(fill="both", expand=True)

    fondo2=Frame(fondo, bg="#A6171C", width=1500, height=880)
    fondo2.pack_propagate(False)
    fondo2.pack(padx=99, pady=50)

    titulo=Label(fondo2, text="Modificar ingredientes",font=("Orelega One", 48), fg="#F1C045", bg="#A6171C")
    titulo.pack(padx=20, pady=20)

    fondo3=Frame(fondo2, bg="white", height=180)
    fondo3.pack(expand=True)

    def volver_a_menu():
        from Ingredientes.menu_ingredientes import menu_ingrediente_
        menu_ingrediente_(modificar_ingrediente)

    ingrediente_modificado=Label(fondo3, text="Selecciona el ingrediente a modificar", font=("Inter", 24), bg="white")
    ingrediente_modificado.pack(padx=20, pady=10)

    ingredientes=[
        "Ingrediente 1",
        "Ingrediente 2",
        "Ingrediente 3",
        "Ingrediente 4"
    ]

    ingrediente_modificado_combo=ttk.Combobox(fondo3, values=ingredientes, font=("Inter", 24))
    ingrediente_modificado_combo.set("Selecciona un ingrediente")
    ingrediente_modificado_combo.pack(padx=20, pady=10)

    def on_select(event):
        print("Producto seleccionado:", ingrediente_modificado_combo.get())
    
    ingrediente_modificado_combo.bind('<<ComboboxSelected>>', on_select)

    nombre=Label(fondo3, text="Nuevo nombre del ingrediente", font=("Inter", 24), bg="white")
    nombre.pack(padx=20, pady=10)
    
    nombre_entry=Entry(fondo3, font=("Inter", 24), bg="white")
    nombre_entry.pack(padx=20, pady=10)

    cantidad=Label(fondo3, text="Nueva cantidad", font=("Inter", 24), bg="white")
    cantidad.pack(padx=20, pady=10)

    cantidad_entry=Entry(fondo3, font=("Inter", 24), bg="white")
    cantidad_entry.pack(padx=20, pady=10)

    unidad=Label(fondo3, text="Cambiar unidad de medida", font=("Inter", 24), bg="white")
    unidad.pack(padx=20, pady=10)

    # Lista de unidades de medida comunes
    unidades_medida = [
        "Kilogramos (kg)",
        "Gramos (g)",
        "Litros (L)",
        "Mililitros (ml)",
        "Piezas (pz)",
        "Unidades (u)",
        "Paquetes (paq)"
    ]

    # Crear el Combobox
    unidad_combo = ttk.Combobox(fondo3, values=unidades_medida, font=("Inter", 24))
    unidad_combo.set("Selecciona un producto")  # Valor por defecto
    unidad_combo.pack(padx=20, pady=10)

    # Función para cuando se selecciona una opción
    def on_select(event):
        print("Producto seleccionad:", unidad_combo.get())
    
    # Vincular la función al evento de selección
    unidad_combo.bind('<<ComboboxSelected>>', on_select)

    producto=Label(fondo3, text="Cambiar producto", font=("Inter", 24), bg="white")
    producto.pack(padx=20, pady=10)

    prodcutos=[
        "Producto 1",
        "Producto 2",
        "Producto 3",
        "Producto 4"
    ]

    prodcutos_combo=ttk.Combobox(fondo3, values=prodcutos, font=("Inter", 24))
    prodcutos_combo.set("Selecciona un producto")
    prodcutos_combo.pack(padx=20, pady=10)

    def on_select(event):
        print("Unidad seleccionada:", prodcutos_combo.get())
    
    prodcutos_combo.bind('<<ComboboxSelected>>', on_select)

    regresar=Button(fondo3, text="Regresar", font=("Inter", 24), bg="#F1C045", command=volver_a_menu)
    regresar.pack(padx=20, pady=10)
    
    agregar=Button(fondo3, text="Modificar", font=("Inter", 24), bg="#F1C045")
    agregar.pack(padx=20, pady=10)