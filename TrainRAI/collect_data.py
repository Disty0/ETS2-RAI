#Modified code of Sentex Pygta5 1. collect_data.py

import numpy as np
from grabscreen import grab_screen
import cv2
import time
import os
import keyboard


unbalanced_path = 'unbalanced_train_data/'

WIDTH = 480
HEIGHT = 270

starting_value = 0

w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]

output = nk
def outputkey(key):
    global output
    output = key

pause_key = False
def pausekeycheck():
    global pause_key
    pause_key = True
    

keyboard.add_hotkey('w', lambda: outputkey(w))
keyboard.add_hotkey('w + a', lambda: outputkey(wa))
keyboard.add_hotkey('w + d', lambda: outputkey(wd))
keyboard.add_hotkey('a', lambda: outputkey(a))
keyboard.add_hotkey('d', lambda: outputkey(d))
keyboard.add_hotkey('s', lambda: outputkey(s))
keyboard.add_hotkey('s + a', lambda: outputkey(sa))
keyboard.add_hotkey('s + d', lambda: outputkey(sd))
keyboard.add_hotkey('u', lambda: pausekeycheck())


while True:
    file_name = unbalanced_path + 'training_data-{}.npy'.format(starting_value)

    if os.path.isfile(file_name):
        print('File exists: ',starting_value)
        starting_value += 1
    else:
        print('Starting at: ',starting_value)
        
        break


def main(file_name, starting_value):
    training_data = []
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    screen = grab_screen((1280,52,1024,768))
    screen = cv2.resize(screen, (WIDTH,HEIGHT))
    screen = screen.reshape(WIDTH,HEIGHT,3)

    statehistory0 = screen
    statehistory1 = screen
    statehistory2 = screen

    state = np.array([screen,statehistory0,statehistory1,statehistory2]).reshape(4,WIDTH,HEIGHT,3)

    cv2.startWindowThread()

    paused = False
    print('STARTING!!!')
    while(True):
        
        if not paused:
            global output

            screen = grab_screen((1280,52,1024,768))
            screen = cv2.resize(screen, (WIDTH,HEIGHT))            
            screen = screen.reshape(WIDTH,HEIGHT,3)

            state = np.array([screen,statehistory0,statehistory1,statehistory2]).reshape(4,WIDTH,HEIGHT,3)

            cv2.namedWindow("preview")
            cv2.imshow('preview', state[0].reshape(HEIGHT,WIDTH,3))

            cv2.namedWindow("preview1")
            cv2.imshow('preview1', state[1].reshape(HEIGHT,WIDTH,3))

            cv2.namedWindow("preview2")
            cv2.imshow('preview2', state[2].reshape(HEIGHT,WIDTH,3))

            cv2.namedWindow("preview3")
            cv2.imshow('preview3', state[3].reshape(HEIGHT,WIDTH,3))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                cv2.destroyAllWindows()

            print(output)

            training_data.append([state,output])
            output = nk

            statehistory2 = statehistory1
            statehistory1 = statehistory0
            statehistory0 = screen

            if len(training_data) % 128 == 0:
                print("Current Data Size: ",len(training_data))
                
            if len(training_data) == 2048:
                np.save(file_name,training_data)
                print('SAVED')
                training_data = []
                starting_value += 1
                file_name = unbalanced_path + 'training_data-{}.npy'.format(starting_value)
                    
        global pause_key
        if pause_key:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)
            pause_key = False


main(file_name, starting_value)