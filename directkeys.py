import pyautogui
import time

ForwardKey = "w"
LeftKey = "a"
RightKey = "d"
ReverseKey = "s"
F5 = "f5"
F7 = "f7"
ENTER = "enter"
ONE = "1"
SPACE = "space"
SIX = "6"

def PressKey(key):
    pyautogui.keyDown(key)

def ReleaseKey(key):
    pyautogui.keyUp(key)
