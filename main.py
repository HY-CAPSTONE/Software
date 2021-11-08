import RPi.GPIO as GPIO
import sys
import time
import datetime

import my_dht11 as dht
import my_pump as pump
import my_wflow as wflow
import my_pcf as pcf
import interaction


try:
    g_temperature = 0
    g_humidity = 0
    g_wflow = 0
    g_wlvl = 0
    g_soil = 0
    water_state = 0
    temp_state = 0
    sun_state = 0

    while True:
        g_humidity, g_temperature = dht.readValue()
        g_wlvl = pcf.getWaterLevel()
        g_soil = pcf.getSoilMoisture()
        printValue(g_humidity, g_temperature, g_wlvl, g_soil)

        if g_soil < 200:
            pump.doPumpTime(1)
            g_wflow = wflow.getWaterFlow()
            print("g_wflow:{0}mL\n".format(g_wflow))

        time.sleep(0.5)

        if g_temperature > 30:
            temp_state = 1
            print("temp_state=1")
            interaction.showtempMatrix(temp_state)
        elif g_temperature < 30:
            temp_state = 2
            print("temp_state =2")
            interaction.showtempMatrix(temp_state)
        else:
            temp_state = 0
            interaction.showtempMatrix(temp_state)

        if g_wlvl < 10:
            water_state = 1
            interaction.showwaterMatrix(water_state)


except KeyboardInterrupt:
    GPIO.cleanup()
