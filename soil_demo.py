import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)

try:
	while 1:
		pin_read = GPIO.input(18)
		time.sleep(1)
		print(pin_read)

except KeyboardInterrupt:
	GPIO.cleanup()
