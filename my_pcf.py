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

def test1():
	try:
		bus.write_byte(addr, 0x42)
	except:
		print("error")
	bus.read_byte(addr)
	return bus.read_byte(addr)

def test2():
	bus.write(addr, 0x43)
	bus.read_byte(addr)
	return bus.read_byte(addr)

if __name__ == "__main__":
	setup(0x48)
	while True:
		print("soil {0:0.1f}\n".format(getSoilMoisture()))
		#time.sleep(2)
		print("wlevel {0:0.1f}\n".format(getWaterLevel()))
		print("\n")
		time.sleep(2)
		#print("42: {0:0.1f}\n".format(test1()))
		#print(test2())
else:
	setup(0x48)
