import RPi.GPIO as GPIO
import time

PMP_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) #no warning message printing
GPIO.setup(PMP_PIN, GPIO.OUT)

def doPump():
	GPIO.output(PMP_PIN, 1)

def stopPump():
	GPIO.output(PMP_PIN, 0)

def doPumpTime(sec):
	doPump()
	time.sleep(sec)
	stopPump()


if __name__ == "__main__":
	doPumpTime(3)
	stopPump()
