import Adafruit_DHT


sensor = Adafruit_DHT.DHT11
DHT_PIN = 12

def readValue():
	humidity, temperature = Adafruit_DHT.read_retry(sensor, DHT_PIN)
	return humidity, temperature

def getHumidity():
	return humidity

def getTemperature():
	return temperature

if __name__ == '__main__':
	import sys
	sys.path.append("/home/pi/Document/Adafruit_Python_DHT/")
	global humidity;
	global temperature;
	
	print("start read_retry")
	#a, b = Adafruit_DHT.read_retry(sensor, DHT_PIN)
	a, b = readValue()
	print("end read_retyr")
	if a is not None and b is not None:
		print("Humidity : {0:0.1f} Temperature : {1:0.1f}".format(a, b))
	else :
		print("error")
	
