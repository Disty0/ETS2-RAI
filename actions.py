import time
from directkeys import PressKey, ReleaseKey, ForwardKey, LeftKey, RightKey, ReverseKey, F5, F7, ENTER, ONE, SPACE
import random

def straight():
    PressKey(ForwardKey)
    ReleaseKey(LeftKey)
    ReleaseKey(RightKey)
    ReleaseKey(ReverseKey)

def left():
    if random.randrange(0,3) == 1:
        PressKey(ForwardKey)
    else:
        ReleaseKey(ForwardKey)
    PressKey(LeftKey)
    ReleaseKey(RightKey)
    ReleaseKey(ReverseKey)

def right():
    if random.randrange(0,3) == 1:
        PressKey(ForwardKey)
    else:
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



def no_keys():
    """if random.randrange(0,4) == 1:
        PressKey(ForwardKey)
    else:
        ReleaseKey(ForwardKey)"""
    ReleaseKey(ForwardKey)
    ReleaseKey(LeftKey)
    ReleaseKey(RightKey)
    ReleaseKey(ReverseKey)


def Restore():
    print("Restoring")
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

    print("Restored")