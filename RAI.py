#Modified code of Sentex Pygta5 3. test_model.py
"""
import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0],True)
"""

import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

import numpy as np
from grabscreen import grab_screen
import cv2
import time
from collections import deque, Counter
import random
import numpy as np
from pynput import keyboard
from actions import straight, left, right, reverse, forward_left, forward_right, reverse_left, reverse_right, no_keys, Restore
from directkeys import PressKey, ReleaseKey, ForwardKey, LeftKey, RightKey, ReverseKey
from keras.applications.inception_v3 import InceptionV3
from keras.models import load_model
from keras import Input
#from SpeedDetect import  ReadSpeed, SpeedDetect
import threading

global pausekey
pausekey = False

def on_press(key):
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k in ['u']:  # keys of interest
        global pausekey
        pausekey = True

listener = keyboard.Listener(on_press=on_press)
listener.start()  # start to listen on a separate thread
#listener.join()  # remove if main thread is polling self.keys


MODEL_NAME = 'ETS2_RAI-{}'.format('InceptionResNetV2')

WIDTH = 288
HEIGHT = 162

choices = 9

w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]

t_time = 0.25

MODEL_NAME = 'ETS2_RAI-{}'.format('InceptionResNetV2')

def RAI():

    try:
        model = load_model(MODEL_NAME)
    except:
        print('Failed to load model!')
    """
    SpeedThread = threading.Thread(target=SpeedDetect, args=(), daemon=True)
    SpeedThread.start()
    """
    paused = False
    mode_choice = 0
    last_choice = mode_choice
    
    stuck_time = 0
    
    last_time = time.time()
    """
    for i in list(range(5))[::-1]:
        print(i+1)
        time.sleep(1)
    """
    while(True):
        
        if not paused:
            last_time = time.time()

            """
            Speed = ReadSpeed()
            print("Speed: ",Speed)
            """
            
            screen = grab_screen((1280,52,1024,768))
            screen = cv2.resize(screen, (WIDTH,HEIGHT))            
            screen = screen.reshape(1,WIDTH,HEIGHT,3)

            prediction = model.predict(state)
            #prediction = prediction[0][0:9] + prediction[1][0:9] + prediction[2][0:9] + prediction[3][0:9]
            #                                           [w, s, a, d, wa, wd, sa, sd, nk]
            #prediction = np.array(prediction) * np.array([1, 1, 1, 1, 1, 1, 1, 1, 0.001])           
            mode_choice = np.argmax(prediction)

  
            if mode_choice == 0:
                if last_choice != 0 or 4 or 5:
                    no_keys()
                straight()
                choice_picked = 'straight'
                
            elif mode_choice == 1:
                if last_choice != 1 or 6 or 7:
                    no_keys()
                reverse()
                choice_picked = 'reverse'
                
            elif mode_choice == 2:
                left()
                choice_picked = 'left'

            elif mode_choice == 3:
                right()
                choice_picked = 'right'

            elif mode_choice == 4:
                if last_choice != 0 or 4 or 5:
                    no_keys()
                forward_left()
                choice_picked = 'forward+left'

            elif mode_choice == 5:
                if last_choice != 0 or 4 or 5:
                    no_keys()
                forward_right()
                choice_picked = 'forward+right'

            elif mode_choice == 6:
                if last_choice != 1 or 6 or 7:
                    no_keys()
                reverse_left()
                choice_picked = 'reverse+left'

            elif mode_choice == 7:
                if last_choice != 1 or 6 or 7:
                    no_keys()
                reverse_right()
                choice_picked = 'reverse+right'

            elif mode_choice == 8:
                no_keys()
                choice_picked = 'nokeys'
            else:
                choice_picked = "Invalid"
                print(mode_choice)

            last_choice = mode_choice

            print('loop took {} seconds. Choice: {}'.format( round(time.time()-last_time, 3) ,choice_picked))
            """
            if Speed<= 10:
                stuck_time += time.time()-last_time
                if stuck_time >= 30:
                    stuck_time = -15
                    Restore()
            else:
                stuck_time = 0
            """
            

        global pausekey
        if pausekey:
            if paused:
                paused = False
                print("Resuming")
                time.sleep(1)
            else:
                paused = True
                ReleaseKey(LeftKey)
                ReleaseKey(ForwardKey)
                ReleaseKey(RightKey)
                ReleaseKey(ReverseKey)
                time.sleep(1)
                print("Paused")
            pausekey = False       

if __name__=="__main__":
    #with tf.device('/cpu:0'):
    RAI()
