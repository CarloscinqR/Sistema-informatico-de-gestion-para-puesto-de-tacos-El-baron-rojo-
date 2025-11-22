from view import log_in
from tkinter import *
class App():
    def __init__(self,ventana):
        view=log_in.InterfacesLogin(ventana)   
 
if __name__=="__main__":
    ventana=Tk()
    app=App(ventana)
    ventana.mainloop()