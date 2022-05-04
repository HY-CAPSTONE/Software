import smbus2
import time

bus = smbus2.SMBus(1)

def setup(address):
	global addr
	addr = address

def getSoilMoisture():
	try:
		bus.write_byte(addr, 0x40)
	except:
		print("soil error")
	bus.read_byte(addr) # dummy read to start conversion

	return bus.read_byte(addr)

def getWaterLevel():
	try:
		bus.write_byte(addr, 0x41)
	except:
		print("wlevel error")
	bus.read_byte(addr) # dummy read to start conversion
	return bus.read_byte(addr)


if __name__ == "__main__":
	setup(0x48)
	while True:
		print("soil {0:0.1f}\n".format(getSoilMoisture()))
		time.sleep(1)
		print("wlevel {0:0.1f}\n".format(getWaterLevel()))
		time.sleep(1)

else:
	setup(0x48)
