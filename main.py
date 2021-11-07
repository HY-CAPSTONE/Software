from threading import Thread
from multiprocessing import Process, Queue
from header import g_temperature, g_humidity, g_soil, g_wflow, g_wlvl
import RPi.GPIO as GPIO
import sys
import time
import datetime

import my_dht11 as dht
import my_pump as pump
import my_wflow as wflow
import my_pcf as pcf
import interaction
from connect_mysql import setup_DB, insert_executor


def getDhtValues():
    global g_temperature, g_humidity
    g_humidity, g_temperature = dht.readValue()
    print("humi:{}, temp:{}".format(g_humidity, g_temperature))
    time.sleep(10)


def getWaterLevelValue():
    global g_wlvl
    while True:
        g_wlvl = pcf.getWaterLevel()
        print("waterLevel:{}".format(g_wlvl))
        time.sleep(10)


def getWaterFlowValue():
    global g_wflow
    while True:
        g_wflow = wflow.getWaterFlow()
        print("waterflow:{}".format(g_wflow))
        time.sleep(10)


def getSoilMoistureValue():
    global g_soil
    while True:
        g_soil = pcf.getSoilMoisture()
        print("SoilMois:{}".format(g_soil))
        time.sleep(10)


def setup_system():
    # Adding path
    sys.path.append("/home/pi/Documents/Adafruit_Python_DHT/")

    # make thread for I/O
    dht_thread = Thread(target=getDhtValues)
    wlevel_thread = Thread(target=getWaterLevelValue)
    wflow_thread = Thread(target=getWaterFlowValue)
    soilmois_thread = Thread(target=getSoilMoistureValue)

    dht_thread.start()
    wlevel_thread.start()
    wflow_thread.start()
    soilmois_thread.start()

    return dht_thread, wlevel_thread, wflow_thread, soilmois_thread


if __name__ == "__main__":
  	dht_t, wlevel_t, wflow_t, soil_t = setup_system()
    try:
		global g_temperature, g_humidity, g_soil, g_wflow, g_wlvl
        mysql_con, mysql_cursor, potID = setup_DB()
        while True:
            print("start")
            insert_executor(mysql_cursor, mysql_con, "Sensors",
                            potID, datetime.datetime.now())

            print("{}, {}, {}, {}, {}".format(g_temperature,
                                              g_humidity, g_wflow, g_wlvl, g_soil))

            time.sleep(50)

	except KeyboardInterrupt as e:
		print(e)

    finally:
        GPIO.cleanup()
        mysql_con.close()
        dht_t.join()
        wlevel_t.join()
        wflow_t.join()
        soil_t.join()

else:
    # do nothing
    print("This do nothing")


# try:
#     g_temperature = 0
#     g_humidity = 0
#     g_wflow = 0
#     g_wlvl = 0
#     g_soil = 0
#     water_state = 0
#     temp_state = 0
#     sun_state = 0

#     while True:
#         g_humidity, g_temperature = dht.readValue()
#         g_wlvl = pcf.getWaterLevel()
#         g_soil = pcf.getSoilMoisture()
#         printValue(g_humidity, g_temperature, g_wlvl, g_soil)

#         if (g_soil < 200):
#             pump.doPumpTime(1)
#             g_wflow = wflow.getWaterFlow()
#             print("g_wflow:{0}mL\n".format(g_wflow))

#         time.sleep(0.5)

#         if(g_temperature > 30):
#             temp_state = 1
#             print("temp_state=1")
#             interaction.showtempMatrix(temp_state)
#         elif(g_temperature < 30):
#             temp_state = 2
#             print("temp_state =2")
#             interaction.showtempMatrix(temp_state)
#         else:
#             temp_state = 0
#             interaction.showtempMatrix(temp_state)

#         if(g_wlvl < 10):
#             water_state = 1
#             interaction.showwaterMatrix(water_state)


# except KeyboardInterrupt:
#     GPIO.cleanup()
