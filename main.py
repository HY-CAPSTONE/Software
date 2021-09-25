import threading
import time
import RPi.GPIO as GPIO
import sys
import ../Adafruit_DHT

class Worker(threading.Thread):
	def __init__(self, name):
		super().__init__()
		self.name = name
		# print default dot matrix display

	def run(self):
		# print dot matrix



def displaying:
	# thread exist -> kill thread & create new one
	t = Worker("dotMatrix")
	t.daemon = True
	t.start()


displaying()
sensor = Adafruit_DHT.DHT11
pint = 18 # pin number

try:
	while 1:
		humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
		if humidity is not None and temperature is not None:
			print("temp={0:0.1f},  Humidity={1:0.1f}%".format(temperature, humidity))
		else:
			print("DHT Error")				
		

except KeyboardInterrupt:
	GPIO.cleanup()
