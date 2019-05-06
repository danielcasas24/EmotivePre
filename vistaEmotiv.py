# -*- coding: utf-8 -*-
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import Tkinter as Tk
import matplotlib.pyplot as plt
from PIL import ImageTk, Image
import saveData as sd
import tkMessageBox

global campoIdentificador
global listTipoEstudio
global buttonGrabar
global buttonDetener
global id


def generarGraficos():
    fig, ax1 = plt.subplots(1,1, figsize=(7, 3))
    fig.subplots_adjust(left=0.2, bottom=0.15, top=0.86)
    fig1, ax2 = plt.subplots(1,1, figsize=(7, 3))
    fig1.subplots_adjust(left=0.2, bottom=0.15, top=0.86)
    ax2.set_ylim(0,50)
    ax1.set_ylim(0, 1)
    ax1.set_xlim(0, 5)
    ax1.set_title(u'Representación Análisis Emocional')
    ax2.set_title(u'Banda de Poder Lóbulo Frontal')
    ax1.set_facecolor('#fcfcfc')
    ax2.set_facecolor('#fcfcfc')
    ax2.set_ylim(0, 50)
    ax2.yaxis.grid(linestyle='--',zorder=0)
    ax1.yaxis.grid(linestyle='--',zorder=0)
    # get rid of the frame
    for spine in fig.gca().spines.values():
        spine.set_visible(False)
    ax1.tick_params(top=False, bottom=False, left=False, right=False, labelleft=True, labelbottom=True)

    # get rid of the frame
    for spine in fig1.gca().spines.values():
        spine.set_visible(False)
    ax2.tick_params(top=False, bottom=False, left=False, right=False, labelleft=True, labelbottom=True)

    # intialize two line objects (one in each axes)
    line1, = ax1.plot([], [], lw=1.3, color='#d8b359',zorder=3)
    line2, = ax1.plot([], [], lw=1.3, color='#9966cc',zorder=3)#9290db
    line3, = ax1.plot([], [], lw=1.3, color='#c01d1d',zorder=3)
    line4, = ax1.plot([], [], lw=1.3, color='#4488d4',zorder=3)
    line5, = ax1.plot([], [], lw=1.3, color='#00944d',zorder=3)
    line = [line1, line2, line3, line4, line5]

    # the same axes initalizations as before (just now we do it for both of them)
    #for ax in [ax1, ax2, ax3, ax4]:
    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel(u'Valor normalizado de emoción')
    ax2.set_ylabel('Decibeles')
    return line, fig, fig1, ax1, ax2

def definirRaiz():
    root = Tk.Tk()
    root.state('zoomed')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    size = (screen_width, screen_height)
    return root, size

def definirFondo(root, size):
    fname = Image.open("fondo15.png").resize(size)
    bg_image = ImageTk.PhotoImage(fname, master=root)
    bg_label = Tk.Label(root, image=bg_image)
    bg_label.photo = bg_image
    w = bg_image.width()
    h = bg_image.height()
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    return bg_label, w, h

def zonaAnalisis(bg_label, fig, fig1):
    image_title_1=ImageTk.PhotoImage(Image.open("Titulo1-1.png"), master=bg_label)
    label_title = Tk.Label(bg_label,image=image_title_1,bg="blue",height=50,width=260)
    label_title.photo = image_title_1
    label_title.place(x=115,y=125)
    canvasPerformance = FigureCanvasTkAgg(fig, master=bg_label)
    canvasPerformance.get_tk_widget().place(x=520, y=150)
    canvasBandpower = FigureCanvasTkAgg(fig1, master=bg_label)
    canvasBandpower.get_tk_widget().place(x=520, y=470)
    scaleFocus = Tk.Scale(bg_label, from_ = 0.0, to = 1.0,orient='horizontal',resolution=-1, troughcolor='#9966cc',sliderlength=10, length=400 ,label='                                                                   Concentración', showvalue=0, font=('Oswald','16'))
    scaleFocus.place(x=45,y=255)
    scaleInteres = Tk.Scale(bg_label, from_ = 0.0, to = 1.0,orient='horizontal',resolution=-1, troughcolor='#c01d1d',sliderlength=10, length=400 ,label='                                                                                  Interés', showvalue=0, font=('Oswald','16'))
    scaleInteres.place(x=45,y=360)
    scaleRelax = Tk.Scale(bg_label, from_ = 0.0, to = 1.0,orient='horizontal',resolution=-1, troughcolor='#4488d4',sliderlength=10, length=400 ,label='                                                                           Relajación', showvalue=0, font=('Oswald','16'))
    scaleRelax.place(x=45,y=465)
    scaleStress = Tk.Scale(bg_label, from_ = 0.0, to = 1.0,orient='horizontal',resolution=-1, troughcolor='#d8b359',sliderlength=10, length=400 ,label='                                                                                    Estrés', showvalue=0, font=('Oswald','16'))
    scaleStress.place(x=45,y=570)
    scaleEngagment = Tk.Scale(bg_label, from_ = 0.0, to = 1.0,orient='horizontal',resolution=-1, troughcolor='#00944d',sliderlength=10, length=400 ,label='Aburrimiento                                            Compromiso', showvalue=0, font=('Oswald','16'))
    scaleEngagment.place(x=45,y=675)
    scalesArray = [scaleFocus, scaleInteres, scaleRelax, scaleStress, scaleEngagment]
    return scalesArray

def zonaBotones(bg_label, root, ax1):
    frameBotones = Tk.Frame(bg_label,bg='#f0f0f0',height=225,width=225,relief='ridge',bd= 3,highlightbackground='red')
    frameBotones.place(x=1225, y=185)

    image_btn_1=ImageTk.PhotoImage(Image.open("btnGrabar12.png").resize((70,70)), master=frameBotones)
    buttonGrabar = Tk.Button(frameBotones, image=image_btn_1,height=70,width=70,relief='flat',command=lambda: sd.obtenerValorGeneral(campoIdentificador,listTipoEstudio,buttonGrabar,buttonDetener))
    buttonGrabar.photo = image_btn_1
    buttonGrabar.place(x=25, y=25)

    image_btn_2=ImageTk.PhotoImage(Image.open("btnParar1.png").resize((70,70)), master=frameBotones)
    buttonDetener = Tk.Button(frameBotones, image=image_btn_2,height=70,width=70,relief='flat', command=lambda: sd.guardarGeneral(campoIdentificador, listTipoEstudio, buttonGrabar, buttonDetener),state=Tk.DISABLED)
    buttonDetener.photo = image_btn_2
    buttonDetener.place(x=120, y=25)

    image_btn_3=ImageTk.PhotoImage(Image.open("btnReset1.png").resize((70,70)), master=frameBotones)
    buttonLimpiar = Tk.Button(frameBotones, image=image_btn_3,height=70,width=70, activebackground='red',relief='flat',command=lambda: sd.resetDatos(campoIdentificador))
    buttonLimpiar.photo = image_btn_3
    buttonLimpiar.place(x=25, y=120)

    image_btn_4=ImageTk.PhotoImage(Image.open("btnSalir1.png").resize((70,70)), master=frameBotones)
    buttonSalir = Tk.Button(frameBotones, image=image_btn_4,height=70,width=70,relief='flat', command=root.quit)#Con quit termina inusualmente
    buttonSalir.photo = image_btn_4
    buttonSalir.place(x=120, y=120)

def zonaDatos(bg_label):
    global campoIdentificador
    global listTipoEstudio
    global id
    frameDatos = Tk.Frame(bg_label,bg='#f0f0f0',height=150,width=225,relief='ridge',bd= 3,highlightbackground='red')
    frameDatos.place(x=1225, y=480)

    label_Title_Datos = Tk.Label(frameDatos, text="Datos Registro",font=('Oswald','12'))
    label_Title_Datos.place(x=65,y=0)
    label_id = Tk.Label(frameDatos, text="Identificador",font=("Helvetica", '10'))
    label_id.place(x=10,y=40)
    id = Tk.StringVar()
    campoIdentificador = Tk.Entry(frameDatos,textvariable=id,width=15)
    campoIdentificador .place(x=110,y=42)

    label_tipo_estudio = Tk.Label(frameDatos, text="Tipo Estudio",font=("Helvetica", '10'))
    label_tipo_estudio.place(x=10,y=100)

    listTipoEstudio = Tk.Listbox(frameDatos,height=2, width=7,font=("Helvetica", '10'))
    listTipoEstudio.insert(1, "Manual")
    listTipoEstudio.insert(2, "Test")
    listTipoEstudio.place(x=110,y=90)

    image_info=ImageTk.PhotoImage(Image.open("info.png").resize((70,70)), master=bg_label)
    button_info = Tk.Button(bg_label, image=image_info,bg="white",height=70,width=70,relief='flat')
    button_info.photo = image_info
    button_info.place(x=1300,y=680)

def mensajeAlertaDatos():
    tkMessageBox.showinfo('Alerta',"Ingresa los datos")

def mensajeGrabado():
    tkMessageBox.showinfo('Grabación',"Los datos han sido grabados satisfactoriamente")
