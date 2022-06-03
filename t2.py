import subprocess 

TEMP = 10
HUMID = 12
SOIL = 13
TANK = 14
subprocess.run(["/home/pi/HomeFarm/Bitmap/TFTDisplay", f"{TEMP}", f"{HUMID}", f"{SOIL}", f"{TANK}"], stdout=subprocess.DEVNULL)
