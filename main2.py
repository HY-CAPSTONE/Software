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


def write_global_var():
    global g_temperature, g_humidity, g_soil, g_wflow, g_wlvl
    g_soil = pcf.getSoilMoisture()
    g_wlvl = pcf.getWaterLevel()
    g_wflow = wflow.getWaterFlow()
    g_humidity, g_temperature = dht.readValue()


def read_send_sql():
    global g_temperature, g_humidity, g_soil, g_wflow, g_wlvl
    insert_executor(
        mysql_cursor,
        mysql_con,
        "Sensors",
        potID,
        datetime.datetime.now(),
        g_temperature,
        g_humidity,
        g_soil,
        g_wlvl,
        0,
        g_wflow,
    )


def read_dot_matrix():
    global g_temperature, g_humidity, g_soil, g_wflow, g_wlvl


def setup_system():
    # Adding path
    sys.path.append("/home/pi/Documents/Adafruit_Python_DHT/")

    # setup DB connection
    mysql_con, mysql_cursor, potID = setup_DB()

    # make Thread
    th1 = Thread(target=write_global_var)
    th2 = Thread(target=read_send_sql, args=(mysql_con, mysql_cursor, potID))
    th3 = Thread(target=read_dot_matrix, args=())

    # run Thread
    th1.start()
    th2.start()
    th3.start()

    # make thread for I/O
    return th1, th2, th3


if __name__ == "__main__":
    th_w, th_r_sql, th_r_dot = setup_system()
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
        th_r_sql.join()
        th_r_dot.join()

else:
    # do nothing
    print("This do nothing")
