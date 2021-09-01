import RPi.GPIO as GPIO
import time, sys
GPIO.setmode(GPIO.BCM)
FLOW_SENSOR = 23
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP) ## GPIO 23 input

global count
count = 0

def countPulse(channel):
	global count
	count = count + 1
	print count
GPIO.add_event_detect(FLOW_SENSOR, GPIO.FALLING, callback=countPulse)
while True:
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		print '\ncaught keyboard interrupt!, bye'
		GPIO.cleanup()
		sys.exit()
