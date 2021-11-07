from threading import Thread
from multiprocessing import Process, Queue
import RPi.GPIO as GPIO
import sys
import time

import my_dht11 as dht
import my_pump as pump
import my_wflow as wflow
import my_pcf as pcf
import interaction
from connect_mysql import setup_DB, insert_executor


def getDhtValues():
    g_humidity, g_temperature = dht.readValue()
    print("humi:{}, temp:{}".format(g_humidity, g_temperature))
    time.sleep(1)


def getWaterLevelValue():
    while True:
        g_wlvl = pcf.getWaterLevel()
        print("waterLevel:{}".format(g_wlvl))
        time.sleep(1)


def getWaterFlowValue():
    while True:
        g_wflow = wflow.getWaterFlow()
        print("waterflow:{}".format(g_wflow))
        time.sleep(1)


def getSoilMoistureValue():
    while True:
        g_soil = pcf.getSoilMoisture()
        print("SoilMois:{}".format(g_soil))
        time.sleep(1)


def printValue(humi, temper, wlvl, soil):
    print("humi:{0}, temp:{1}, wlwvl:{2}, soil:{3}\n ".format(
        humi, temper, wlvl, soil))


def setup_system():
    # Adding path
    sys.path.append("/home/pi/Documents/Adafruit_Python_DHT/")

    # define global value
    global g_temperature
    global g_humidity
    global g_wflow
    global g_wlvl
    global g_soil
    global water_state
    global temp_state
    global sun_state

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
    try:
        dht_t, wlevel_t, wflow_t, soil_t = setup_system()
        mysql_con, mysql_cursor, potID = setup_DB()
        while True:
            print("start")
            time.sleep(1000)

    except Exception as e:
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
