#Modified code of Sentex Pygta5 3. test_model.py

import numpy as np
from grabscreen import grab_screen
import cv2
import time
from Sentdex.models import otherception3 as googlenet
from collections import deque, Counter
import random
from statistics import mode,mean
import numpy as np
from pynput import keyboard
from actions import straight, left, right, reverse, forward_left, forward_right, reverse_left, reverse_right, no_keys, Restore
from directkeys import PressKey, ReleaseKey, ForwardKey, LeftKey, RightKey, ReverseKey
import  tensorflow as tf

from SpeedDetect import  ReadSpeed, SpeedDetect
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

GAME_WIDTH = 1920
GAME_HEIGHT = 1080

how_far_remove = 800
rs = (20,15)
log_len = 25

motion_req = 800
motion_log = deque(maxlen=log_len)

WIDTH = 480
HEIGHT = 270
LR = 1e-3
EPOCHS = 10

choices = deque([], maxlen=5)
hl_hist = 250
choice_hist = deque([], maxlen=hl_hist)

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
with tf.device('/cpu:0'):
    model = googlenet(WIDTH, HEIGHT, 3, LR, output=9)
MODEL_NAME = 'ETS2_RAI-0.001-Googlenet_Inception_v3_Sentdex-100-epochs.model'
model.load(MODEL_NAME)

print('We have loaded a previous model!!!!')

def RAI():
        SpeedThread = threading.Thread(target=SpeedDetect, args=(), daemon=True)
        SpeedThread.start()

        paused = False
        mode_choice = 0

        screen = grab_screen((1280,65,1024,768))

        stuck_time = 0
        
        last_time = time.time()

        for i in list(range(10))[::-1]:
            print(i+1)
            time.sleep(1)
        
        while(True):
            
            if not paused:
                last_time = time.time()
                
                screen = grab_screen((1280,65,1024,768))

                Speed = ReadSpeed()
                print("Speed: ",Speed)

                screen = cv2.resize(screen, (WIDTH,HEIGHT))
                
                prediction = model.predict([screen.reshape(WIDTH,HEIGHT,3)])[0]
                #prediction = np.array(prediction) * np.array([4.5, 0.1, 0.1, 0.1,  1.8,   1.8, 0.5, 0.5, 0.2])


                mode_choice = np.argmax(prediction)

                if mode_choice == 0:
                    straight()
                    choice_picked = 'straight'
                    
                elif mode_choice == 1:
                    reverse()
                    choice_picked = 'reverse'
                    
                elif mode_choice == 2:
                    left()
                    choice_picked = 'left'
                elif mode_choice == 3:
                    right()
                    choice_picked = 'right'
                elif mode_choice == 4:
                    forward_left()
                    choice_picked = 'forward+left'
                elif mode_choice == 5:
                    forward_right()
                    choice_picked = 'forward+right'
                elif mode_choice == 6:
                    reverse_left()
                    choice_picked = 'reverse+left'
                elif mode_choice == 7:
                    reverse_right()
                    choice_picked = 'reverse+right'
                elif mode_choice == 8:
                    no_keys()
                    choice_picked = 'nokeys'

                print('loop took {} seconds. Choice: {}'.format( round(time.time()-last_time, 3) ,choice_picked))
                
                if Speed<= 10:
                    stuck_time += time.time()-last_time
                    if stuck_time >= 30:
                        stuck_time = -15
                        Restore()
                else:
                    stuck_time = 0

                

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
    RAI()
