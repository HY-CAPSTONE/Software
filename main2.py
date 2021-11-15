import threading
from multiprocessing import Process, Queue

from mysql.connector.cursor import MySQLCursor
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

rw_mutex = threading.Lock()
event = threading.Event()


def read(mysql_con, mysql_cursor, potID):
    # rw_mutex.acquire()
    # read_send_sql(mysql_cursor, mysql_con, potID)
    # read_dot_matrix()
    # rw_mutex.release()
    global g_temperature, g_humidity, g_soil, g_wflow, g_wlvl

    with rw_mutex:
        print("read")
        l_temperature = g_temperature, l_humidity = g_humidity
        l_soil = g_soil, l_wflow = g_wflow, l_wlvl = g_wlvl

    read_send_sql(
        mysql_con, mysql_cursor, potID, l_temperature, l_humidity, l_soil, l_wflow, l_wlvl
    )
    read_dot_matrix(l_temperature, l_humidity, l_soil, l_wflow, l_wlvl)


def write():
    # rw_mutex.acquire()
    # write_global_var()
    # rw_mutex.release()
    with rw_mutex:
        print("write")
        write_global_var()


def write_global_var():
    global g_temperature, g_humidity, g_soil, g_wflow, g_wlvl
    g_soil = pcf.getSoilMoisture()
    g_wlvl = pcf.getWaterLevel()
    g_wflow = wflow.getWaterFlow()
    g_humidity, g_temperature = dht.readValue()


def read_send_sql(
    mysql_con, mysql_cursor, potID, l_temperature, l_humidity, l_soil, l_wflow, l_wlvl
):
    insert_executor(
        mysql_cursor,
        mysql_con,
        "Sensors",
        potID,
        datetime.datetime.now(),
        l_temperature,
        l_humidity,
        l_soil,
        l_wflow,
        0,
        l_wlvl,
    )


def read_dot_matrix(l_temperature, l_humidity, l_soil, l_wflow, l_wlvl):
    if l_soil < 200:
        pump.doPumpTime(1)
    if l_temperature > 30:
        temp_state = 1
        interaction.showtempMatrix(temp_state)
    elif l_temperature < 30:
        temp_state = 2
        interaction.showtempMatrix(temp_state)
    else:
        temp_state = 0
        interaction.showtempMatrix(temp_state)

    if l_wlvl < 10:
        water_state = 1
        interaction.showwaterMatrix(water_state)


def setup_system():
    # Adding path
    sys.path.append("/home/pi/Documents/Adafruit_Python_DHT/")

    # setup DB connection
    mysql_con, mysql_cursor, potID = setup_DB()

    th1 = threading.Thread(target=write, daemon=True)
    th1.start()

    th2 = threading.Thread(target=read, daemon=True, args=(mysql_con, mysql_cursor, potID))
    th2.start()

    # make thread for I/O
    return th1, th2, mysql_con, mysql_cursor


if __name__ == "__main__":
    th_w, th_r, mysql_con, mysql_cursor = setup_system()
    try:
        while True:
            print("start")
            time.sleep(10)

    except KeyboardInterrupt as e:
        print(e)

    finally:
        GPIO.cleanup()
        mysql_con.close()
        th_w.join()
        th_r.join()


else:
    # do nothing
    print("This do nothing")
