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
eve_r = threading.Event()
eve_w = threading.Event()


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
            if eve_w.is_set():
                return 0
            write_global_var()
    except:
        return 0
    finally:
        print("writer finally")


def read(mysql_con, mysql_cursor, potID):
    try:
        while True:
            if eve_r.is_set():
                return 0

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

            que.task_done()
            time.sleep(1)

    except OSError:
        return 0

    finally:
        # mysql_con.close()
        print("reader finally")


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

    finally:
        print("cleanup started")

        # 큐에 남은 데이터를 모두 보내고 싶으면
        # kill write
        eve_w.set()
        th_w.join()

        GPIO.cleanup()
        que.join()

        # kill read
        eve_r.set()
        th_r.join()
        mysql_cursor.close()
        mysql_con.close()


else:
    # do nothing
    print("This do nothing")
