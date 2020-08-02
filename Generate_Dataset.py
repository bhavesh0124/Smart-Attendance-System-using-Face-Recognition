import os
import pymongo
import cv2
import numpy as np
import pandas as pd
import warnings
import tkinter as tk
warnings.filterwarnings("ignore")


def Generate_Data(Name,Roll_no):


    def pushmongo(key,value):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        dblist = myclient.list_database_names()
       
        mydb = myclient["students"]

        hindi_subject = mydb["Hindi"]
        english_subject= mydb["English"]

        mydict = [{"Name":key,"Roll_number":value,"Attendance":0}]
        x = hindi_subject.insert_many(mydict)
        y = english_subject.insert_many(mydict)

        print("Student Enrolled Successfully in Hindi and English Subjects")


    def input_information():
        name=Name
        roll_no=Roll_no
        parent_dir="people/"
        final_path=roll_no+name
        path=os.path.join(parent_dir,final_path)
        enter_CSV(name,roll_no)   ## pushing in CSV File
        pushmongo(name,roll_no)   ## Pushing in mongoDB database
        return path
        

    def enter_CSV(name,roll_no):
        df=pd.read_csv("Students_Enrollment.csv")
        df=df.append({'Name':name, 'Roll Number': roll_no},ignore_index=True)
        df.to_csv("Students_Enrollment.csv",index=False)
        return

    ######## Entering the required details#################
    path=input_information()

    os.makedirs(path)   ##Creating the path
    #########################Joining the paths#######################

    pic_no=0

    #####################Loading the harcascade classifier#################
    fa=cv2.CascadeClassifier('FaceDetection/faces.xml')
    cap=cv2.VideoCapture(0)

    ret=True

    while ret:
        ret,frame=cap.read()
        #######Detecting the Faces##################
        frame=cv2.flip(frame,1)
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces=fa.detectMultiScale(gray,1.3,5)

        #
        for (x,y,w,h) in faces:
            cropped=frame[y:y+h,x:x+w]
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2,cv2.LINE_AA)
            #face_aligned = face_aligner.align(frame, frame_gray, face)
            pic_no=pic_no+1
            cv2.imwrite(path+'/'+str(pic_no)+'.jpg',cropped)
        cv2.imshow('frame',frame)
        cv2.waitKey(100)

        if( (pic_no>30) | (0XFF==ord('a'))):
            break

    cap.release()
    cv2.destroyAllWindows()
    return
