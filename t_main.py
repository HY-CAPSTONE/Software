import threading
import socket
import RPi.GPIO as GPIO
import sys
import time
import datetime
from dataclasses import dataclass
import queue
import os
import subprocess
import picamera

import my_dht11 as dht
import my_pump as pump
import my_pcf as pcf
import my_neo as neo
from connect_mysql import connect_DB, insert_executor, select_executor, update_executor



neo.doNeoPixel()

subprocess.run(["/home/pi/HomeFarm/Bitmap/TFTDisplay", "25", "50", "50", "20"], stdout=subprocess.DEVNULL)
time.sleep(3)
subprocess.run(["/home/pi/HomeFarm/Bitmap/TFTDisplay", "40", "50", "10", "20"], stdout=subprocess.DEVNULL)
time.sleep(1000)
subprocess.run(["/home/pi/HomeFarm/Bitmap/TFTDisplay", "25", "25", "0", "0"], stdout=subprocess.DEVNULL)

time.sleep(1)
subprocess.run(["/home/pi/HomeFarm/Bitmap/TFTDisplay", "15", "20", "150", "20"], stdout=subprocess.DEVNULL)
time.sleep(1)
subprocess.run(["/home/pi/HomeFarm/Bitmap/TFTDisplay", "20", "20", "10", "40"], stdout=subprocess.DEVNULL)
time.sleep(1)
time.sleep(1)
subprocess.run(["/home/pi/HomeFarm/Bitmap/TFTDisplay", "30", "20", "80", "100"], stdout=subprocess.DEVNULL)
time.sleep(1)
subprocess.run(["/home/pi/HomeFarm/Bitmap/TFTDisplay", "35", "20", "10", "120"], stdout=subprocess.DEVNULL)
time.sleep(1)
subprocess.run(["/home/pi/HomeFarm/Bitmap/TFTDisplay", "40", "20", "1200", "150"], stdout=subprocess.DEVNULL)
time.sleep(1)

time.sleep(1)
neo.doMoodNeoPixel()
time.sleep(1)
neo.stopNeoPixel()




