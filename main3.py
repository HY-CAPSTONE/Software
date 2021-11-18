import threading

# from multiprocessing import Process, Queue

# from header import g_temperature, g_humidity, g_soil, g_wflow, g_wlvl
import RPi.GPIO as GPIO
import sys
import time
import datetime
from dataclasses import dataclass
import queue

import my_dht11 as dht
import my_pump as pump
import my_wflow as wflow
import my_pcf as pcf
import interaction
from connect_mysql import setup_DB, insert_executor

que = queue.Queue(2048)


@dataclass
class SensorValues:
    g_temp: int = None
    g_humid: int = None
    g_soil: int = None
    g_wflow: int = None
    g_wlvl: int = None

    def __init__(self, temp, humid, soil, wflow, wlvl):
        self.g_temp = temp
        self.g_humid = humid
        self.g_soil = soil
        self.g_wflow = wflow
        self.g_wlvl = wlvl


def write():
    try:
        while True:
            write_global_var()
    except:
        return 0


def read(mysql_con, mysql_cursor, potID):
    try:
        while True:
            # if que is empty, it will blocked for 100sec
            # after 100sec, it will occur "empty" exception
            # ** if block=True & timeout=None, this operation can't stop, it is not occur keyboardexception
            q = que.get(block=True, timeout=100)

            # 가져온 10개의 데이터의 평균을 로컬로 저장

            # 로컬 값을 쏴주기
            print(
                "temp:{} humid:{} soil:{} wflow:{} wlvl:{}".format(
                    q.g_temp,
                    q.g_humid,
                    q.g_soil,
                    q.g_wflow,
                    q.g_wlvl,
                )
            )

            read_send_sql(
                mysql_con, mysql_cursor, potID, q.g_temp, q.g_humid, q.g_soil, q.g_wlvl, q.g_wflow
            )
            read_dot_matrix(q.g_temp, q.g_humid, q.g_soil, q.g_wlvl, q.g_wflow)

            time.sleep(1)

    except OSError:
        return 0


def write_global_var():
    g_soil = pcf.getSoilMoisture()
    g_wlvl = pcf.getWaterLevel()
    g_wflow = wflow.getWaterFlow()
    g_humid, g_temp = dht.readValue()
    temp = SensorValues(g_temp, g_humid, g_soil, g_wflow, g_wlvl)

    # if que is full, it will blocked 100sec
    # after 100sec, it occur "full" exception
    que.put(temp, block=True, timeout=100)


def read_send_sql(
    mysql_con, mysql_cursor, potID, l_temperature, l_humidity, l_soil, l_wlvl, l_wflow
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
        l_wlvl,
        0,
        l_wflow,
    )


def read_dot_matrix(l_temperature, l_humidity, l_soil, l_wlvl, l_wflow):
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
        # while True:
        print("main start")
        time.sleep(10)
        print("main finished")
        # que.join()

    # except KeyboardInterrupt:
    #     print("KeyboardInterrupttion")

    finally:
        print("cleanup started")
        GPIO.cleanup()
        mysql_con.close()
        que.join()


else:
    # do nothing
    print("This do nothing")
