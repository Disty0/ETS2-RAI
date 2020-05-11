#Modified code of Sentex Pygta5 3. test_model.py
"""import plaidml.keras
plaidml.keras.install_backend()"""

import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0],True)

import numpy as np
from grabscreen import grab_screen
import cv2
import time
from keras.applications.inception_v3 import InceptionV3
import random
import numpy as np
from pynput import keyboard
from actions import straight, left, right, reverse, forward_left, forward_right, reverse_left, reverse_right, no_keys, Restore
from directkeys import PressKey, ReleaseKey, ForwardKey, LeftKey, RightKey, ReverseKey
from SpeedDetect import  ReadSpeed, SpeedDetect
import threading
from keras.models import load_model
from keras import Input
from collections import deque

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

MODEL_NAME = 'ETS2_RAI-{}'.format('InceptionV3')

BATCH_SIZE = 1
ExpReplay_CAPACITY = 10240
GAMMA = 0.975

WIDTH = 480
HEIGHT = 270

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

def LoadData(screen, mode_choice, reward, screen2):
    try:
        #Load TrainData
        ExpReplay = deque(np.load("TrainData.npy", allow_pickle=True))
        print("Succesfully loaded TrainData!")
    except:
        print("Failed to load TrainData")
        ExpReplay = deque()
        ExpReplay.append((screen, mode_choice, reward, screen2))

    try:
        #Load StepsData
        StepsData = open("StepsData.txt", "r")
        steps = int(StepsData.readline())
        StepsData.close()
        print("Succesfully loaded StepsData!")
    except:
        print("Failed to load StepsData")
        steps = 1
    return (steps , ExpReplay)

def SaveData(steps,ExpReplay):
    try:
        #Save TrainData
        print("Saving TrainData!")
        np.save("TrainData.npy" ,ExpReplay)
        print("Succesfully saved TrainData!")
    except:
        print("Failed to save TrainData")

    try:
        #Save StepsData
        print("Saving StepsData!")
        StepsData = open("StepsData.txt", "w")
        StepsData.write(str(steps))
        StepsData.close()
        print("Succesfully saved StepsData!")
    except :
        print("Failed to save StepsData")

def RAI():
        
        #with tf.device('/cpu:0'):

        input_tensor = Input(shape=(WIDTH,HEIGHT,3))
        model = InceptionV3(include_top=True, input_tensor=input_tensor , pooling='max', classes=9, weights=None) #input_shape=(WIDTH,HEIGHT,3),
        model.compile('Adagrad', 'categorical_crossentropy')

        model = load_model(MODEL_NAME)

        print('We have loaded a previous model!')
        

        SpeedThread = threading.Thread(target=SpeedDetect, args=(), daemon=True)
        SpeedThread.start()

        paused = False
        mode_choice = 0
        last_choice = mode_choice

        screen = grab_screen((1280,65,1024,768))
        screen = cv2.resize(screen, (WIDTH,HEIGHT))
        screen = screen.reshape(WIDTH,HEIGHT,3)

        stuck_time = 0

        reward = 0
        rewardcheck = 0

        epsilon = 0.75

        (steps , ExpReplay) = LoadData(screen,mode_choice,reward,screen)
        
        last_time = time.time()

        for i in list(range(5))[::-1]:
            print(i+1)
            time.sleep(1)


        while(True):
            
            if not paused:
                last_time = time.time()
                
                screen = grab_screen((1280,65,1024,768))
                screen = cv2.resize(screen, (WIDTH,HEIGHT))
                screen = screen.reshape(WIDTH,HEIGHT,3)
                Speed = ReadSpeed()

                if rewardcheck >= 10:
                    if Speed <= 10:
                        reward -= 10
                    
                    elif Speed <= 20:
                        pass

                    elif Speed <= 30:
                        reward += 10

                    elif Speed <= 60:
                        reward += 20

                    elif  Speed <= 100:
                        reward += 40

                    elif Speed <= 140:
                        reward += 80
                    
                    else:
                        reward += 100
                    rewardcheck = 0

                if steps > ExpReplay_CAPACITY:
                    epsilon = 0.5
                if steps > 48000:
                    epsilon = 0.25
                if steps > 64000:
                    epsilon = 0.15
                if steps > 80000:
                    epsilon = 0.1
                if steps > 96000:
                    epsilon = 0.05
                if steps > 112000:
                    epsilon = 0.01

                
                if random.random() < epsilon:
                    mode_choice = random.randint(0,8)
                else:
                    prediction = model.predict(screen.reshape(-1,WIDTH,HEIGHT,3))
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


                lenExpReplay = len(ExpReplay)
                if lenExpReplay < ExpReplay_CAPACITY:
                    if lenExpReplay < BATCH_SIZE:
                        SubBATCH_SIZE = lenExpReplay
                    else:
                        SubBATCH_SIZE = BATCH_SIZE
                else:
                    SubBATCH_SIZE = BATCH_SIZE

                minibatch = random.sample(ExpReplay, SubBATCH_SIZE)

                inputs = np.zeros((SubBATCH_SIZE, WIDTH, HEIGHT, 3))
                targets = np.zeros((inputs.shape[0], choices)) 
                Q_sa = 0


                for i in range(len(minibatch)):
                    state_t = minibatch[i][0]
                    action_t = minibatch[i][1]
                    reward_t = minibatch[i][2]
                    state_t1 = minibatch[i][3]

                    inputs[i] = state_t
                    targets[i] = model.predict(state_t.reshape(1,WIDTH,HEIGHT,3), batch_size=1)
                    Q_sa = model.predict(state_t1.reshape(1,WIDTH,HEIGHT,3), batch_size=1)

                    if state_t1 is None:
                        targets[i,action_t] = reward_t
                    else:
                        targets[i,action_t] = reward_t + GAMMA * np.max(Q_sa)

                model.fit(inputs, targets, batch_size = SubBATCH_SIZE, epochs = 1, verbose = 0)

                screen2 = grab_screen((1280,65,1024,768))
                screen2 = cv2.resize(screen2, (WIDTH,HEIGHT))
                screen2 = screen2.reshape(WIDTH,HEIGHT,3)

                ExpReplay.append((screen, mode_choice, reward, screen2))
                
                if lenExpReplay > ExpReplay_CAPACITY:
                    ExpReplay.popleft()

                if Speed<= 10:
                    stuck_time += time.time()-last_time
                    if stuck_time >= 30:
                        stuck_time = -15
                        reward -= 1000
                        Restore()
                else:
                    stuck_time = 0

                rewardcheck += time.time()-last_time

                steps += 1
                print('loop took {} seconds. Choice: {}. Steps: {}. Reward: {} Speed: {}'.format( round(time.time()-last_time, 3) ,choice_picked, steps, reward, Speed))
                
                if steps%128 == 0:
                    SaveData(steps,ExpReplay)
                    model.save(MODEL_NAME)

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
