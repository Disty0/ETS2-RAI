#Modified code of Sentex Pygta5 balance_data.py

import numpy as np
import cv2
import os
import time
from random import randint
FILE_I_END = -1
data_path = 'balanced_train_data/'

WIDTH = 288
HEIGHT = 162

if FILE_I_END == -1:
    FILE_I_END = 0
    while True:
        file_name = data_path + 'training_data-{}.npy'.format(FILE_I_END)

        if os.path.isfile(file_name):
            print('Loading file exists: ',FILE_I_END)
            FILE_I_END += 1
        else:
            FILE_I_END -= 1
            print('Final loading file: ',FILE_I_END) 
            break

data_order = [i for i in range(0,FILE_I_END+1)]
cv2.startWindowThread()
for count,i in enumerate(data_order):
        
    try:
        file_name = data_path + 'training_data-{}.npy'.format(i)
        train_data = np.load(file_name, allow_pickle=True)
        print('training_data-{}.npy'.format(i),len(train_data))
        count = 1
        """
        for data in train_data:

            #show img on screen
            cv2.namedWindow("preview")
            cv2.imshow('preview', data[0].reshape(270,480,3))
            
            time.sleep(0.2)
            print(count)
            count += 1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
        """
        SAMPLE = len(train_data)
        X = np.array([cv2.resize(i[0].reshape(270,480,3),(WIDTH,HEIGHT)) for i in train_data]).reshape(SAMPLE,WIDTH,HEIGHT,3)
        Y = np.array([i[1] for i in train_data])
        
        for i in range(SAMPLE):
            cv2.namedWindow("preview")
            cv2.imshow('preview', X[i].reshape(HEIGHT,WIDTH,3))
            print(X[0].shape)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()

    except Exception as e:
        print(str(e))

print("FINISHED PREVIEWING DATA!")


