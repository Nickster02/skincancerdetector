#import libraries
from tkinter import *
from tkinter import filedialog,messagebox
from tkinter.ttk import *
from PIL import ImageTk,Image
from SkinCancerDetector import *
from ctypes import windll


#window creation
window=Tk()
windll.shcore.SetProcessDpiAwareness(1)


#icon definition
icon=ImageTk.PhotoImage(Image.open("icon/icon.png"))


#maintain a global variable for prediction
img_path=""
mod_path=""


#functions to handle events
def predict():
    if mod_path!="":
        model=SkinCancerDetector(mod_path)
    else:
        model=SkinCancerDetector("model/model.h5")
    result=model.predict(img_path)
    global prediction,picture
    prediction['text']="Diagnosis : " +result[1]
    img=ImageTk.PhotoImage(Image.open(img_path).resize((400,300)))
    picture['image']=img
    img.image=img


def browse_model():
    messagebox.showinfo("Attention",'''
    The Model must meet the following description:
    
    Input Size : (28,28,3)
    Output Size : (1,7)
    Normalization : /255.0
    Recommended Dataset: HAM10000 SKIN CANCER DATASET

    Output Labels :  
    0: 'actinic keratoses and intraepithelial carcinomae',  
    1: 'basal cell carcinoma', 
    2: 'benign keratosis-like lesions', 
    3: 'dermatofibroma',
    4: 'melanocytic nevi', 
    5: 'pyogenic granulomas and hemorrhage', 
    6: 'melanoma'
    ''')
    path=filedialog.askopenfilename(initialdir="/",
                                           title="Select An Model",
                                           filetypes=[("HDF5 Files", "*.h5")])
    global model_path,mod_path
    if path!="":
        mod_path=path
        model_path['text']=path[0:10]+"...."+path[-10:]
    else:
        mod_path="model/model.h5"


def browse_files():
    path=filedialog.askopenfilename(initialdir="/",
                                           title="Select An Image",
                                           filetypes=[("Image Files", "*.jpg")])
    global file_path,picture,img_path,prediction
    prediction['text']=""
    if path!="":
        img_path=path
        file_path['text']=path[0:10]+"...."+path[-10:]

    img=ImageTk.PhotoImage(Image.open(path).resize((400,300)))
    picture['image']=img
    img.image=img


#window definition
window.title('CON-NET Skin Cancer Detector')
window.iconphoto(False,icon)
window.geometry('900x700')
window.maxsize(1000,700)
window.minsize(1000,700)
for i in range(7):
    window.columnconfigure(i,weight=100)
for i in range(10):
    window.rowconfigure(i,weight=100)


#Stye defintion
style=Style()
style.configure("button.TButton",font=("Calibri",15))


#adding components
title=Label(window,
            text="Skin Cancer Detector",
            font=('Calibri',20,'bold'))
title.grid(row=0,columnspan=9)


file_prompt=Label(window,
             text="Choose Your Image: ",
             font=('Calibri',15,))
file_prompt.grid(row=1,column=1)


file_path=Label(window,
               text="No Image Chosen",
               font=('Calibri',15,'italic'))
file_path.grid(row=1,column=2,columnspan=2)


choose_file=Button(window,
                text="Browse",
                style="button.TButton",
                command=browse_files)
choose_file.grid(row=1,column=4)


model_prompt=Label(window,
             text="Choose Your Model: ",
             font=('Calibri',15,))
model_prompt.grid(row=2,column=1)


model_path=Label(window,
               text="No Model Chosen",
               font=('Calibri',15,'italic'))
model_path.grid(row=2,column=2,columnspan=2)


choose_model=Button(window,
                style="button.TButton",
                text="Browse",
                command=browse_model)
choose_model.grid(row=2,column=4)


optional=Label(window,
               text="[Optional]",
               font=('Calibri',15,'italic'))
optional.grid(row=2,column=5)


picture=Label(window,
              text="No Image Selected",
              font=('Calibri',20,'bold'))
picture.grid(row=3,column=1,rowspan=5,columnspan=4)


predict_img=Button(window,
              text="Diagnose",
              style="button.TButton",
              command=predict)
predict_img.grid(row=5,column=5)


prediction=Label(window,
              text="",
              font=('Calibri',20,'bold'))
prediction.grid(row=8,columnspan=9)

window.mainloop()
#end of window