#Modified code of Sentex Pygta5 balance_data.py

import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import random
import cv2
import time
import os

balanced_batch_size = 2048
FILE_I_END = -1
saves = 0
unbalanced_path = 'unbalanced_train_data/'
balanced_path= 'balanced_train_data/'

w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]

batches = 0

while True:
    file_name = balanced_path + 'training_data-{}.npy'.format(saves)

    if os.path.isfile(file_name):
        print('Saving File exists: ',saves)
        saves += 1
    else:
        print('Starting to save at: ',saves) 
        break

if FILE_I_END == -1:
    FILE_I_END = 0
    while True:
        file_name = unbalanced_path + 'training_data-{}.npy'.format(FILE_I_END)

        if os.path.isfile(file_name):
            print('Loading file exists: ',FILE_I_END)
            FILE_I_END += 1
        else:
            FILE_I_END -= 1
            print('Final loading file: ',FILE_I_END) 
            break

data_order = [i for i in range(0,FILE_I_END+1)]

forwards = []
reverses = []
lefts = []
rights = []
forwardlefts = []
forwardrights = []
reveselefts = []
reveserights = []
nokeys = []

for count,i in enumerate(data_order):
        
    try:
        file_name = unbalanced_path + 'training_data-{}.npy'.format(i)
        # full file info
        train_data = np.load(file_name, allow_pickle=True)
        print('training_data-{}.npy'.format(i),len(train_data))

        df = pd.DataFrame(train_data)

        shuffle(train_data)

        for data in train_data:
            img = data[0]
            img = img.reshape(480,270,3)
            choice = data[1]

            if choice == w:
                if random.randint(0,4) != 0:
                    forwards.append([img,choice])
                    batches+=1
            elif choice == s:
                reverses.append([img,choice])
                batches+=1
            elif choice == a:
                lefts.append([img,choice])
                batches+=1
            elif choice == d:
                rights.append([img,choice])
                batches+=1
            elif choice == wa:
                forwardlefts.append([img,choice])
                batches+=1
            elif choice == wd:
                forwardrights.append([img,choice])
                batches+=1
            elif choice == sa:
                reveselefts.append([img,choice])
                batches+=1
            elif choice == sd:
                reveserights.append([img,choice])
                batches+=1
            elif choice == nk:
                if random.randint(0,1) == 0:
                    nokeys.append(([img,choice]))
                    batches+=1
            else:
                print('no matches')
            
            print(batches)

            """
            #show img on screen
            cv2.startWindowThread()
            cv2.namedWindow("preview")
            cv2.imshow('preview', img)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
            """    
            
            
            
            if batches == balanced_batch_size:
                final_data = forwards + reverses + lefts + rights + forwardlefts + forwardrights + reveselefts + reveserights + nokeys
                shuffle(final_data)
                print("Saving!!!")
                np.save(balanced_path + 'training_data-{}.npy'.format(saves), final_data)
                saves+= 1
                batches = 0
                forwards = []
                reverses = []
                lefts = []
                rights = []
                forwardlefts = []
                forwardrights = []
                reveselefts = []
                reveserights = []
                nokeys = []


    except Exception as e:
            print(str(e))

if batches != 0:
    final_data = forwards + reverses + lefts + rights + forwardlefts + forwardrights + reveselefts + reveserights + nokeys
    shuffle(final_data)
    print("Saving!!!")
    np.save(balanced_path + 'training_data-{}.npy'.format(saves), final_data)
    print("Final Batches: ", batches)

print("FINISHED BALANCING DATA!")


