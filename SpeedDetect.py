from detectnumber import  DetectNumber
from grabscreen import grab_screen
import cv2

def ReadSpeed():
    try:
        NumberData = open("NumberData.txt", "r")
        Speed = int(NumberData.readline())
        NumberData.close()
        return Speed
    except:
        return 0

def SpeedDetect():
    while True:
        Screen = grab_screen((2056,542, 19,10))
        (SpeedImg, Speed) = DetectNumber(Screen, 0, 10, 0, 19)

        NumberData = open("NumberData.txt", "w")
        NumberData.write(str(Speed))
        NumberData.close()

        print("Speed: ",Speed)
        """
        cv2.imshow('Speed', SpeedImg)
                    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
        """


if __name__ == "__main__":
    while True:
        screen = grab_screen((2056,542, 19,10))
        (SpeedImg, Speed) = DetectNumber(screen, 0, 10, 0, 19)

        NumberData = open(os.getcwd() + "/NumberData.txt", "w")
        NumberData.write(str(Speed))
        NumberData.close()
        print("Speed: ",Speed)

        cv2.imshow('Speed', SpeedImg)
                    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
