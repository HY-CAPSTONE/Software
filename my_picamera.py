from picamera import PiCamera
from time import sleep
from datetime import datetime

camera = PiCamera()


def doCapture(now_time):
    camera.capture(f'/home/pi/img/{now_time}.jpg')

if __name__ == "__main__":
    now_time = datetime.now() 
    camera.capture(f'/home/pi/img/{now_time}.jpg')
else :
    now_time = datetime.now()
