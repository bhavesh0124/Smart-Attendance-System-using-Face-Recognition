import tkinter as tk
from tkinter import messagebox as mess
import tkinter.simpledialog as tsd
import cv2,os
import csv
import numpy as np
from threading import Thread
from tkinter import * 
from tkinter.ttk import *
from PIL import Image,ImageTk
import pandas as pd
import datetime
import time

from Generate_Dataset import Generate_Data
from Model_train import Model_Training
from Recognizer import Recognition

window = tk.Tk()

class FullScreenApp(object):
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

app=FullScreenApp(window)


class Example(Frame):
    def __init__(self, master, *pargs):
        Frame.__init__(self, master, *pargs)



        self.image = Image.open("landscape.png")
        self.img_copy= self.image.copy()


        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)

    def _resize_image(self,event):

        new_width = event.width
        new_height = event.height

        self.image = self.img_copy.resize((new_width, new_height))

        self.background_image = ImageTk.PhotoImage(self.image)
        self.background.configure(image =  self.background_image)



e = Example(window)
e.pack(fill=BOTH, expand=YES)
C = tk.Canvas(window, height=600, width=600)




ts = time.time()
date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
day,month,year=date.split("-")

mont={'01':'January',
      '02':'February',
      '03':'March',
      '04':'April',
      '05':'May',
      '06':'June',
      '07':'July',
      '08':'August',
      '09':'September',
      '10':'October',
      '11':'November',
      '12':'December'
      }


window.title("Smart Attendance System Using Facial Recognition")

message3 = tk.Label(window, text="Smart Attendance System" ,fg="white",bg="#8a2e7f" ,width=55 ,height=1,font=('Helvetica', 30, ' bold '))
message3.place(relx = 0.5, rely = 0.1, anchor = CENTER)

frame4 = tk.Frame(window, bg="#8a2e7f")
frame4.place(relx=0.5, rely=0.17, relwidth=0.2, relheight=0.05,anchor=CENTER)

datef = tk.Label(frame4, text = day+"-"+mont[month]+"-"+year, fg="white",bg="#262523" ,width=55 ,height=1,font=('Helvetica', 20, ' bold '))
datef.pack(fill='both',expand=1)


frame1 = tk.Frame(window, bg="#ffffff")
frame1.place(relx=0.057, rely=0.21, relwidth=0.35, relheight=0.78)


head1 = tk.Label(frame1, text="                      For Already Registered                       ", fg="white",bg="#8a2e7f" ,font=('Helvetica', 17, ' bold ') )
head1.place(x=0,y=0)

frame2 = tk.Frame(window, bg="#ffffff")
frame2.place(relx=0.59, rely=0.21, relwidth=0.35, relheight=0.78)


head2 = tk.Label(frame2, text="                       For New Enrollment                       ", fg="white",bg="#8a2e7f" ,font=('Helvetica', 17, ' bold ') )
head2.grid(row=0,column=0)




#frame3 = tk.Frame(window, bg="#c4c6ce")
#frame3.place(relx=0.52, rely=0.09, relwidth=0.09, relheight=0.07)




# clock = tk.Label(frame3,fg="orange",bg="#262523" ,width=55 ,height=1,font=('times', 22, ' bold '))
# clock.pack(fill='both',expand=1)
# tick()

##################################################LEFT SIDE###################################################################################################3

lbl = tk.Label(frame2, text="Enter Roll Number",width=20  ,height=1  ,fg="white"  ,bg="#8a2e7f" ,font=('Helvetica', 13, ' bold ') )
lbl.place(relx=0.3, rely=0.1)

txt = tk.Entry(frame2,width=16 ,fg="black",font=('Helvetica', 13 ))
txt.place(relx=0.32, rely=0.16)

lbl2 = tk.Label(frame2, text="Enter Student's Name",width=20,height=1   ,fg="white"  ,bg="#8a2e7f" ,font=('Helvetica', 13, ' bold '))
lbl2.place(relx=0.3, rely=0.27)

txt2 = tk.Entry(frame2,width=20 ,fg="black",font=('Helvetica', 13)  )
txt2.place(relx=0.3, rely=0.33)

#message1 = tk.Label(frame2, text="1)Take Images  >>>  2)Save Profile" ,bg="#00aeff" ,fg="black"  ,width=39 ,height=1, activebackground = "yellow" ,font=('times', 15, ' bold '))
#message1.place(x=7, y=230)


def get_data():
  Name=txt2.get()
  Roll=txt.get()
  Generate_Data(Name,Roll)

takeImg = tk.Button(frame2, text="Take Images",command=get_data ,fg="white"  ,bg="#8a2e7f"  ,width=25  ,height=1, activebackground = "white" ,font=('Helvetica', 13, ' bold '))
takeImg.place(x=100, y=230)


##########################################################Progress Bar###################################################################

def progress_Measure(): 
  import time 
  time.sleep(2)
  progress['value'] = 20
  window.update_idletasks() 
  time.sleep(6) 

  progress['value'] = 40
  window.update_idletasks() 
  time.sleep(6) 

  progress['value'] = 50
  window.update_idletasks() 
  time.sleep(6) 

  progress['value'] = 60
  window.update_idletasks() 
  time.sleep(5) 

  progress['value'] = 100


def bar(): 
  Thread(target = Model_Training).start()
  Thread(target = progress_Measure()).start()

  


trainImg = tk.Button(frame2, text="Train The Model",fg="white", command=bar ,bg="#507d2a"  ,width=34  ,height=1, activebackground = "white" ,font=('Helvetica', 15, ' bold '))
trainImg.place(x=37, y=350)

progress = Progressbar(frame2,length=200,orient = HORIZONTAL, mode='determinate')
progress.place(x=150,y=435)

##################RIGHT SIDE################################################################################################
#message = tk.Label(frame2, text="" ,bg="#00aeff" ,fg="black"  ,width=39,height=1, activebackground = "yellow" ,font=('times', 16, ' bold '))
#message.place(x=7, y=450)



lbl3 = tk.Label(frame1, text="Select Class",width=20,fg="white",bg="#8a2e7f"  ,height=1 ,font=('Helvetica', 13, ' bold '))
lbl3.place(x=140, y=50)

# takeImg = tk.Button(frame1, text="Hindi" ,fg="white"  ,bg="#8a2e7f"  ,width=10  ,height=1, activebackground = "white" ,font=('Helvetica', 13, ' bold '))
# takeImg.place(x=70, y=110)

# takeImg = tk.Button(frame1, text="English" ,fg="white"  ,bg="#8a2e7f"  ,width=10  ,height=1, activebackground = "white" ,font=('Helvetica', 13, ' bold '))
# takeImg.place(x=270, y=110)


##############################RADIO BUTTONS##########################################################
v = tk.IntVar()
v.set(1)
selection=0
def ShowChoice():
    global selection
    selection=v.get()
  

first=tk.Radiobutton(frame1, text="Hindi", variable=v, command=ShowChoice,
              value=1,bg="#ffffff",activeforeground="#507d2a",borderwidth=10,font=('Helvetica', 14, ' bold ')).place(x=130, y=110,anchor=CENTER)

second=tk.Radiobutton(frame1, text="English", variable=v, command=ShowChoice,
              value=2,bg="#ffffff",activeforeground="#507d2a",borderwidth=10,font=('Helvetica', 14, ' bold ')).place(x=260, y=88)


###########################################################################################################################


def Recognizer():
  Recognition(selection)

trackImg = tk.Button(frame1, text="Take Attendance",fg="white"  ,bg="#507d2a" ,command=Recognizer, width=35  ,height=1, activebackground = "white" ,font=('Helvetica', 15, ' bold '))
trackImg.place(x=35,y=150)




###############################QUIT###########################################################################################

# res=0











tv= Treeview(frame1,columns =('roll_no','name','attendance'),selectmode='browse',show=["headings"])
tv.column('roll_no',width=155,anchor=tk.CENTER)
tv.column('name',width=155,anchor=tk.CENTER)
tv.column('attendance',width=155,anchor=tk.CENTER)
tv.grid(row=2,column=0,padx=(0,0),pady=(250,0),columnspan=4)


tv.heading('roll_no',text ='Roll Number')
tv.heading('name',text ='Name')
tv.heading('attendance',text ='Attendance')


scroll=Scrollbar(frame1,orient='vertical',command=tv.yview)
scroll.grid(row=2,column=4,padx=(0,100),pady=(250,0),sticky='ns')
tv.configure(yscrollcommand=scroll.set)





def clear_tree():
  x=tv.get_children()
  if x != '()': # checks if there is something in the first row
    for child in x:
      tv.delete(child)
  


def Show_attendance():
  import csv
  if(selection==1):
    subject="Hindi_attendance/Hindi_Attendance.csv"
  else:
    subject="English_attendance/English_Attendance.csv"

  with open(subject, newline = "") as f:
     reader = csv.DictReader(f, delimiter=',')
     for row in reader:
      roll = row['Roll Number']
      Name = row['Name']
      atttendance = row['Attendance']
      tv.insert("", 0, values=(roll, Name, atttendance))
      




Show_button = tk.Button(frame1, text="Show Attendance",fg="white" ,command=Show_attendance ,bg="green", width=15 ,height=1,activebackground = "white" ,font=('Helvetica', 12, ' bold '))
Show_button.place(x=35, y=200)


Show_button1 = tk.Button(frame1, text="Clear",fg="white" ,command=clear_tree ,bg="red", width=15 ,height=1,activebackground = "white" ,font=('Helvetica', 12, ' bold '))

Show_button1.place(x=285, y=200)







#####################################################################################################################

def destroy():
  window.destroy()


quitWindow = tk.Button(frame1, text="Quit",fg="white"  ,bg="red"  ,width=35 ,height=1,command=destroy ,activebackground = "white" ,font=('Helvetica', 15, ' bold '))
quitWindow.place(x=30, y=490)

# # ########################################### END ###################################################################################################











#window.configure(menu=menubar)
window.mainloop()














