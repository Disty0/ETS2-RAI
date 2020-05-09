#Modified code of Sentex Pygta5 1. collect_data.py

import numpy as np
from grabscreen import grab_screen
import cv2
import time
import os
import keyboard


unbalanced_path = 'unbalanced_train_data/'

w = [1,0,0,0,0,0,0,0,0]
s = [0,1,0,0,0,0,0,0,0]
a = [0,0,1,0,0,0,0,0,0]
d = [0,0,0,1,0,0,0,0,0]
wa = [0,0,0,0,1,0,0,0,0]
wd = [0,0,0,0,0,1,0,0,0]
sa = [0,0,0,0,0,0,1,0,0]
sd = [0,0,0,0,0,0,0,1,0]
nk = [0,0,0,0,0,0,0,0,1]

starting_value = 0

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
    file_name = file_name
    starting_value = starting_value
    training_data = []
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)

    paused = False
    print('STARTING!!!')
    while(True):
        
        if not paused:
            global output
            screen = grab_screen((1280,65,1024,768))
            
            # resize to something a bit more acceptable for a CNN
            screen = cv2.resize(screen, (480,270))
            # run a color convert:
            screen = screen.reshape(480,270,3)

            print(output)

            training_data.append([screen,output])
            output = nk

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