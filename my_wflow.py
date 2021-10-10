import RPi.GPIO as GPIO
import time, sys
GPIO.setmode(GPIO.BCM)
FLOW_PIN = 14
GPIO.setup(FLOW_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP) ## GPIO 23 input

interrupt_counter = 0


def countPulse(channel):
	global interrupt_counter
	interrupt_counter += 1

def getWaterFlow():
	# return mL
	global interrupt_counter
	ml = interrupt_counter / 5880.0 * 1000
	print("before counter:{0}\n".format(interrupt_counter))
	interrupt_counter = 0
	return ml


GPIO.add_event_detect(FLOW_PIN, GPIO.FALLING, callback=countPulse)


if __name__ == "__main__":
	while True:
		try:
			print(interrupt_counter)
			time.sleep(1)
		except KeyboardInterrupt:
			print ('\ncaught keyboard interrupt!, bye')
			GPIO.cleanup()
			sys.exit()


