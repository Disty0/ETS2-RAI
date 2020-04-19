import time
from directkeys import PressKey, ReleaseKey, ForwardKey, LeftKey, RightKey, ReverseKey, F5, F7, ENTER, ONE, SPACE

def Forward():
    PressKey(ForwardKey)
    ReleaseKey(LeftKey)
    ReleaseKey(RightKey)
    ReleaseKey(ReverseKey)

def Left():
    ReleaseKey(ForwardKey)
    PressKey(LeftKey)
    ReleaseKey(RightKey)
    ReleaseKey(ReverseKey)

def Right():
    ReleaseKey(ForwardKey)
    ReleaseKey(LeftKey)
    PressKey(RightKey)
    ReleaseKey(ReverseKey)


def Reverse():
    ReleaseKey(ForwardKey)
    ReleaseKey(LeftKey)
    ReleaseKey(RightKey)
    PressKey(ReverseKey)



def ForwardLeft():
    PressKey(ForwardKey)
    PressKey(LeftKey)
    ReleaseKey(RightKey)
    ReleaseKey(ReverseKey)

def ForwardRight():
    PressKey(ForwardKey)
    ReleaseKey(LeftKey)
    PressKey(RightKey)
    ReleaseKey(ReverseKey)


def ReverseLeft():
    ReleaseKey(ForwardKey)
    PressKey(LeftKey)
    ReleaseKey(RightKey)
    PressKey(ReverseKey)

def ReverseRight():
    ReleaseKey(ForwardKey)
    ReleaseKey(LeftKey)
    PressKey(RightKey)
    PressKey(ReverseKey)



def ActionNothing():
    ReleaseKey(ForwardKey)
    ReleaseKey(LeftKey)
    ReleaseKey(RightKey)
    ReleaseKey(ReverseKey)


def Restore():
    print("Restoring")
    PressKey(F7)
    time.sleep(0.2)
    ReleaseKey(F7)

    PressKey(ENTER)
    time.sleep(0.2)
    ReleaseKey(ENTER)

    PressKey(ONE)
    time.sleep(0.2)
    ReleaseKey(ONE)

    PressKey(ENTER)
    time.sleep(0.2)
    ReleaseKey(ENTER)

    print("---")
    time.sleep(10)

    PressKey(F5)
    time.sleep(0.2)
    ReleaseKey(F5)

    PressKey(SPACE)
    time.sleep(0.2)
    ReleaseKey(SPACE)

    print("Restored")