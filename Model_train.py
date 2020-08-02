from Model_architecture.modelArch import DenseArchs
import cv2
from keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
import numpy as np
import os
import pandas as pd
from embedding import emb

import warnings
warnings.filterwarnings("ignore")


def Model_Training():

    def get_classes():
    	df=pd.read_csv("Students_Enrollment.csv")
    	n_classes = df.shape[0]
    	return(n_classes)


    n_classes=get_classes()

    e=emb()  ## Calling trained model saved as a pickle file to extract embeddings

    arc=DenseArchs(n_classes) 

    face_model=arc.arch()


    x_data=[]
    y_data=[]

    learning_rate=0.01
    epochs=400
    batch_size=16

    people=sorted(os.listdir('people'))

    for x in people:
        for i in os.listdir('people/'+x):
            img=cv2.imread('people'+'/'+x+'/'+i,1)
            img=cv2.resize(img,(160,160))
            img=img.astype('float')/255.0
            img=np.expand_dims(img,axis=0)
            embs=e.calculate(img)
            x_data.append(embs)
            y_data.append(int(x[0])-1)


    x_data=np.array(x_data,dtype='float')
    y_data=np.array(y_data)
    y_data=y_data.reshape(len(y_data),1)

    X=x_data
    y=to_categorical(y_data,num_classes=n_classes)

    o=Adam(decay=learning_rate/epochs)
    face_model.compile(optimizer=o,loss='categorical_crossentropy')

    face_model.fit(X,y,batch_size=batch_size,epochs=epochs,shuffle='true')
    face_model.save('Model/Face_recognition.MODEL')
    print("Training Completed")
    return

