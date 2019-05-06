import numpy as np
import Tkinter as Tk
import emotionMetrics as em
import bandPower as pb
import tkMessageBox
import vistaEmotiv as ve

def changeStateConsolidado(consolidarPerformance,consolidarPowerBand):
    if consolidarPerformance == False:
        consolidarPerformance = True
    else:
        consolidarPerformance = False
    if consolidarPowerBand == False:
        consolidarPowerBand = True
    else:
        consolidarPowerBand = False


def changeStateGuardar(guardarPerformance,guardarPowerBand, idEntry, tipoEstudio, btnGrabar, btnDetener):
    if guardarPerformance == False:
        guardarPerformance = True
    else:
        guardarPerformance = False
    if guardarPowerBand == False:
        guardarPowerBand = True
    else:
        guardarPowerBand = False
    btnDetener.configure(state=Tk.DISABLED)
    btnGrabar.configure(state=Tk.NORMAL)
    tipoEstudio.configure(state=Tk.NORMAL)
    idEntry.configure(state=Tk.NORMAL)

def obtenerValorGeneral(idEntry, tipoEstudio, btnGrabar, btnDetener):
    if (idEntry.get() != '' and len(tipoEstudio.curselection()) != 0):
        identificador = idEntry.get()+'_'+tipoEstudio.get(tipoEstudio.curselection())
        btnDetener.configure(state=Tk.NORMAL)
        btnGrabar.configure(state=Tk.DISABLED)
        tipoEstudio.configure(state=Tk.DISABLED)
        idEntry.configure(state=Tk.DISABLED)
        em.changeStateConsolidadoPerformance()
        pb.changeStateConsolidadoPowerband()
        em.obtenerValorPerformance(identificador)
        pb.obtenerValorPowerband(identificador)
    else:
        ve.mensajeAlertaDatos()

def guardarGeneral(idEntry,tipoEstudio,btnGrabar,btnDetener):
    em.changeStateGuardarPerformance()
    pb.changeStateGuardarPowerband()
    btnDetener.configure(state=Tk.DISABLED)
    btnGrabar.configure(state=Tk.NORMAL)
    tipoEstudio.configure(state=Tk.NORMAL)
    idEntry.configure(state=Tk.NORMAL)

def neWin():
    global c
    global id
    global v
    global Lb1
    global master2
    master2 = Tk.Tk()
    master2.geometry("300x300")
    master2.title("New Window")
    label = Tk.Label(master2, text="Identificador")
    label.pack()
    v = Tk.IntVar()
    id = Tk.StringVar()
    c = Tk.Entry(master2,textvariable=id)
    c.pack()
    label2 = Tk.Label(master2, text="Tipo Estudio")
    label2.pack()
    Lb1 = Tk.Listbox(master2,height=2)
    Lb1.insert(1, "Manual")
    Lb1.insert(2, "Test")
    Lb1.pack()
    y=Tk.Button(master2, text="Enviar", command=obtenerValor).pack()
    master2.mainloop()

def resetMetrics(ax1):
    ax1.set_xlim(0, 5)
    ax1.figure.canvas.draw()

def resetDatos(cEntry):
    cEntry.delete(0,Tk.END)
