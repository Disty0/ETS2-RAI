import time
from directkeys import PressKey, ReleaseKey, ForwardKey, LeftKey, RightKey, ReverseKey, F5, F7, ENTER, ONE, SPACE, SIX
import random

def no_keys():
    ReleaseKey(ForwardKey)
    ReleaseKey(LeftKey)
    ReleaseKey(RightKey)
    ReleaseKey(ReverseKey)

def straight():
    PressKey(ForwardKey)
    ReleaseKey(LeftKey)
    ReleaseKey(RightKey)
    ReleaseKey(ReverseKey)

def left():
    ReleaseKey(ForwardKey)
    PressKey(LeftKey)
    ReleaseKey(RightKey)
    ReleaseKey(ReverseKey)

def right():
    ReleaseKey(ForwardKey)
    ReleaseKey(LeftKey)
    PressKey(RightKey)
    ReleaseKey(ReverseKey)


def reverse():
    ReleaseKey(ForwardKey)
    ReleaseKey(LeftKey)
    ReleaseKey(RightKey)
    PressKey(ReverseKey)



def forward_left():
    PressKey(ForwardKey)
    PressKey(LeftKey)
    ReleaseKey(RightKey)
    ReleaseKey(ReverseKey)

def forward_right():
    PressKey(ForwardKey)
    ReleaseKey(LeftKey)
    PressKey(RightKey)
    ReleaseKey(ReverseKey)


def reverse_left():
    ReleaseKey(ForwardKey)
    PressKey(LeftKey)
    ReleaseKey(RightKey)
    PressKey(ReverseKey)

def reverse_right():
    ReleaseKey(ForwardKey)
    ReleaseKey(LeftKey)
    PressKey(RightKey)
    PressKey(ReverseKey)


def Restore():
    print("Restoring")
    no_keys()

    PressKey(F7)
    time.sleep(0.5)
    ReleaseKey(F7)

    PressKey(ENTER)
    time.sleep(0.5)
    ReleaseKey(ENTER)

    PressKey(ONE)
    time.sleep(0.5)
    ReleaseKey(ONE)

    time.sleep(1)

    PressKey(ENTER)
    time.sleep(0.5)
    ReleaseKey(ENTER)

    print("---")
    time.sleep(15)

    PressKey(F5)
    time.sleep(0.5)
    ReleaseKey(F5)

    PressKey(SPACE)
    time.sleep(0.5)
    ReleaseKey(SPACE)

    PressKey(SIX)
    time.sleep(0.5)
    ReleaseKey(SIX)

    print("Restored")