from stat import FILE_ATTRIBUTE_ENCRYPTED
import tkinter.ttk as ttk
import tkinter as tk
from tkinter import *
from tkinter import filedialog,messagebox


import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as mpatches

from sklearn import __version__ as ver
from matplotlib import __version__  as ver2

import numpy as np
import os

from time import sleep
from skimage import io
from skimage.io import imread
#from skimage.transform import resize
#from skimage.exposure import equalize_adapthist
#from skimage import img_as_float
#from skimage.segmentation import morphological_geodesic_active_contour,inverse_gaussian_gradient
#from skimage.filters import threshold_mean,median
#from skimage.morphology import disk
#from skimage.measure import regionprops,label
#from keras.models import Model
#import keras.preprocessing.image


#import tensorflow as tf
#from tensorflow.keras.models import load_model
#from tensorflow.keras.applications.resnet50 import preprocess_input


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

root = tk.Tk()
root.withdraw()
root.title("PneumoCADX")
s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='blue', background='blue')

fig, ax = plt.subplots()
plt.axis('off')
plt.ion()

path=''
c=0


try :
    print ( ver )
except ModuleNotFoundError:
    messagebox . showerror ( " Error " , " No se encuentran las librerias necesarias para iniciar este programa " )
    root . quit ()

try :
    print ( ver2 )
except ModuleNotFoundError:
    messagebox . showerror ( " Error " , " No se encuentran las librerias necesarias para iniciar este programa " )
    root . quit ()


if os.path.isfile(resource_path('modRes.h5')):
    print('The file is present.')
else:
    messagebox.showerror ( " Error " , " No se encuentra el modelo necesarios para iniciar este programa " )
    root . quit ()
    raise SystemExit

def preprocessing(img):

    img2=resize(img,(400,400))
    img3=equalize_adapthist(img2)
    
    return (img3)

def abrir():
    progress['value']=0
    progress.lower()
    global path
    global c
    c=0
    path =  filedialog.askopenfilename(initialdir = "C:\\",title = "Selecciona Imagen",filetypes = (("jpeg files","*.jpeg"),("all files","*.*"))) 
    if len(path) == 0:
        text.delete('1.0', END)
        text.insert(INSERT,'No seleccionaste alguna imagen')
    else:
        plt.clf()
        text.delete('1.0', END)
        text.insert(INSERT,'Imagen:\n'+ path +'\n')
        text.insert(INSERT, "*****************\n")
        img=imread(path)
        plt.imshow(img,cmap='gray')
        plt.axis('off')
        plt.tight_layout()
        

def reset():
    global path
    fig.clf(keep_observers=True)
    progress['value']=0
    text.delete('1.0', END)
    progress.lower()
    path=''

def ask_quit():
    if messagebox.askokcancel("Confirme", "¿Seguro que desea salir?"):
        root.quit()
        root.destroy()
        raise SystemExit

def about():
    messagebox.showinfo("Acerca de", "Programa Desarollado por:\nVictor Hugo Galindo Ramriez\nJose Agustin Almaraz Damian\nVolodymyr Ponomaryov\nRogelio Reyes Reyes\nClara Cruz Ramos\n\nSEPI ESIME Culhuacán\n\nInstituto politecnico Nacional 2022")
    

def run():
    global c
    if c == 0:
        if len(path) == 0:
            text.insert(INSERT,'No seleccionaste alguna imagen')
        else:
            text.insert(INSERT, "Analizando\n")
            text.insert(INSERT, "*****************\n")
            progress.tkraise()
            progress['value']=10
            root.update_idletasks()
            sleep(1)
            img=imread(path,as_gray=True)
            rgb=preprocessing(img)
            io.imsave("BB.png",rgb)
            plt.clf()
            ax1=fig.add_subplot(121)
            ax1.axis('off')
            ax1.set_title('Imagen Original')
            ax1.imshow(img,cmap='gray')
            ax2=fig.add_subplot(122)
            ax2.imshow(rgb,cmap='gray')
            ax2.set_title('Imagen Procesada')
            ax2.axis('off')
            progress['value']=40
            root.update_idletasks()
            sleep(1)

            model = tf.keras.models.load_model(resource_path('modRes.h5'))

            img_size=(224,224)

            img_path=(resource_path('BB.png'))

            def get_img_array(img_path, size):
                img10 = keras.preprocessing.image.load_img(img_path, target_size=size)

                array = keras.preprocessing.image.img_to_array(img10)
   
                array = np.expand_dims(array, axis=0)
                return array

            img_array = preprocess_input(get_img_array(img_path, size=img_size))

            preds = model.predict(img_array)
            ypred=np.round(preds)
        
            progress['value']=60
            root.update_idletasks()
            sleep(1)
        
            progress['value']=80
            root.update_idletasks()
            sleep(1)
            if ypred<=0.5:
                text.insert(INSERT,'Esta Imagen Pertenece a la Clase Normal\n')
            else:
                text.insert(INSERT,'Esta Imagen Pertenece a la Clase Neumonia \n')
            progress['value']=100
            text.insert(INSERT, "*****************\n")
            text.insert(INSERT, "Finalizado\n")
            c=1
    else :
        if messagebox.askokcancel("Confirme", "¿Deseas analizar la misma imagen?"):
            c=0
            progress['value']=0
            text.delete('1.0', END)
            progress.lower()
            text.insert(INSERT,'Imagen:\n'+ path +'\n')
            text.insert(INSERT, "*****************\n")
            run()
        else :
            messagebox.showwarning("Consejo", "Para analizar otra imagen favor de presionar el boton 'Limpiar'")


toplevel_1 = tk.Toplevel(root)
labelframe_1 = ttk.Labelframe(toplevel_1)

canvas = FigureCanvasTkAgg(fig, master=labelframe_1)
plot_widget = canvas.get_tk_widget()
plot_widget.pack(anchor='center', expand='true', fill='both', side='top')

button_1 = ttk.Button(labelframe_1,text='Abrir Imagen',command=abrir).pack(side='left')
button_2 = ttk.Button(labelframe_1,text='Analizar',command=run).pack(side='left')
button_3 = ttk.Button(labelframe_1,text='Limpiar',command=reset).pack(side='left')
button_4 = ttk.Button(labelframe_1,text='Salir',command=ask_quit).pack(side='left')
button_5 = ttk.Button(labelframe_1,text='Acerca de',command=about).pack(side='left')

labelframe_2 = ttk.Labelframe(labelframe_1,height='200', text='Comandos', width='200')
labelframe_2.pack(side='right')

text = tk.Text(labelframe_2)
text.config(autoseparators='false', exportselection='true', height='10', width='50')
text.pack(side='top')     

labelframe_1.config(height='200', text='Image', width='200')
labelframe_1.pack(side='top')

progress = ttk.Progressbar(toplevel_1)
progress.config(style="red.Horizontal.TProgressbar", orient="horizontal", length=800, mode="determinate")
progress.pack(expand='true', fill='x', side='bottom')
progress.lower()

toplevel_1.config(height='800', width='600')
root.protocol("WM_DELETE_WINDOW", ask_quit)
root.mainloop()






