import numpy as np
import cv2
import time
import os
import pandas as pd
from collections import deque
from random import shuffle
import pickle
"""
import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0],True)
"""
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

from keras import Input
from keras.applications.inception_v3 import InceptionV3 as network
from keras.optimizers import SGD
from keras.models import load_model
#from keras.callbacks import TensorBoard

BATCH = 20

train_data_path = 'balanced_train_data/'

FILE_I_END = -1 #-1 for auto detect

WIDTH = 480
HEIGHT = 270
EPOCHS = 1000000000000000000000000000000000000000000000000000000000000000000000000000 

MODEL_NAME = 'ETS2RAI-{}'.format('InceptionV3')
LOAD_MODEL = True

if FILE_I_END == -1:
    FILE_I_END = 0
    while True:
        file_name = train_data_path + 'training_data-{}.npy'.format(FILE_I_END)

        if os.path.isfile(file_name):
            print('File exists: ',FILE_I_END)
            FILE_I_END += 1
        else:
            FILE_I_END -= 1
            print('Final File: ',FILE_I_END) 
            break

"""
tensorboard = TensorBoard(
    log_dir='logs', histogram_freq=0, write_graph=True, write_images=True,
    update_freq='epoch', profile_batch=2, embeddings_freq=0,
    embeddings_metadata=None
)
"""

if LOAD_MODEL:
    try:
        model = load_model(MODEL_NAME)
        print('We have loaded a previous model!')
    except:
        print('Failed to load model!')
        input_tensor = Input(shape=(WIDTH,HEIGHT,3))
        model = network(include_top=True, input_tensor=input_tensor , pooling='max', classes=9, weights=None)
        model.compile(optimizer=SGD(lr=0.0001, momentum=0.9), loss='categorical_crossentropy')

# iterates through the training files
for e in range(EPOCHS):
    data_order = [i for i in range(0,FILE_I_END+1)]
    shuffle(data_order)
    for count,i in enumerate(data_order):
        
        try:
            file_name = train_data_path + 'training_data-{}.npy'.format(i)
            # full file info
            train_data = np.load(file_name, allow_pickle=True)

            SAMPLE = len(train_data)
            print('training_data-{}.npy - Sample Size: {} - Batch Size: {}'.format(i,SAMPLE,BATCH))
            
            X = np.array([i[0] for i in train_data]).reshape(-1,WIDTH,HEIGHT,3)
            Y = np.array([i[1] for i in train_data])
           
            del train_data            

            print("============================")
            print("Epochs: {} - Steps: {}".format(e, count))
            model.fit(X, Y, batch_size=BATCH ,epochs=1) #, callbacks=[tensorboard])
            print("============================")

            del X
            del Y

            if count%1 == 0 and count != 0:
                print('SAVING MODEL!')
                model.save(MODEL_NAME)
                    
        except Exception as e:
            print(str(e))

print("FINISHED {} EPOCHS!".format(EPOCHS))
