import threading
import RPi.GPIO as GPIO
import sys
import time
import datetime
from dataclasses import dataclass
import queue
import os
import subprocess
import requests
import json

import my_dht11 as dht
import my_pump as pump
import my_pcf as pcf
import my_neo as neo
from connect_mysql import connect_DB, insert_executor

que = queue.Queue(2048)
eve_r = threading.Event()
eve_w = threading.Event()
r_lock = threading.Lock()
w_lock = threading.Lock()
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)

@dataclass
class SensorValues:
    TEMP: int = None
    HUMID: int = None
    SOIL: int = None
    TANK: int = None

    def __init__(self, temp, humid, soil, wlvl):
        self.TEMP = temp
        self.HUMID = humid
        self.SOIL = soil
        self.TANK = wlvl


def write():
    try:
        while True:
            with w_lock:
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
            with r_lock:
                if eve_r.is_set():
                    return 0

            # if que is empty, it will blocked for 100sec
            # after 100sec, it will occur "queue.Empty" exception
            # ** if block=True & timeout=None, this operation can't stop, it is not occur keyboardexception
            q = que.get(block=True, timeout=None)
            que.task_done()
            # 가져온 10개의 데이터의 평균을 로컬로 저장

            # 로컬 값을 쏴주기
            print(
                "temp:{} humid:{} soil:{} wlvl:{}".format(
                    q.TEMP,
                    q.HUMID,
                    q.SOIL,
                    q.TANK,
                )
            )

#            read_send_sql(mysql_con, mysql_cursor, potID, q)
            TEMP = int(q.TEMP)
            HUMID = int(q.HUMID)
            SOIL = int(q.SOIL)
            TANK = int(q.TANK)
            subprocess.run(["/home/pi/HomeFarm/Bitmap/TFTDisplay", f"{TEMP}", f"{HUMID}", f"{SOIL}", f"{TANK}"], stdout=subprocess.DEVNULL)

            api = "https://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"
            url = api.format(city = "Seoul", key = "0276eeb82a71d9b7c07ce64e78fc7a3a")
            res = requests.get(url)
            data = json.loads(res.text)

            if (int(data["sys"]["sunset"]) - time.time() < 5 and int(data["sys"]["sunset"]) - time.time() > -5):
                neo.doNeoPixel()
            if (int(data["sys"]["sunrise"]) - time.time() < 5 and int(data["sys"]["sunrise"]) - time.time() > -5):
                neo.stopNeoPixel()
            print(int(data["sys"]["sunset"]) - time.time())

            if (q.SOIL == 255):
                pump.stopPump()
            elif (q.SOIL < 254) :
                pump.doPump()
            elif (q.SOIL > 200) :
                pump.stopPump()

            if (q.TANK < 100) :
                print("TANL LOw")
            else :
                print("TNK HIGH")
            
			# execute LCDcode
    except :
        print('reader exception occur')
        return 0

    finally:
        print("reader finally")


def write_global_var():
    SOIL = pcf.getSoilMoisture()
    TANK = pcf.getWaterLevel()
    HUMID, TEMP = dht.readValue()
    temp = SensorValues(TEMP, HUMID, SOIL, TANK)

    # if que is full, it will blocked 100sec
    # after 100sec, it occur "queue.Full" exception
    que.put(temp, block=True, timeout=100)


def read_send_sql(mysql_con, mysql_cursor, PID, q):
    insert_executor(
        mysql_con,
        mysql_cursor,
        "Plant",
        PID,
        # datetime.datetime.now(),
        q,
        f"/images/{PID}",
    )
    insert_executor(
        mysql_con,
        mysql_cursor,
        "Gallery",
        PID,
        # datetime.datetime.now(),
        q,
        f"/images/{PID}",
    )


def setup_():
    # setup DB connection
    mysql_con, mysql_cursor, PID = connect_DB()

    th1 = threading.Thread(target=write)
    th1.start()

    th2 = threading.Thread(target=read, args=(mysql_con, mysql_cursor, PID))
    th2.start()

    # make thread for I/O
    return th1, th2, mysql_con, mysql_cursor


if __name__ == "__main__":
    th_w, th_r, mysql_con, mysql_cursor = setup_()
    neo.doNeoPixel()
    try:
        while True:
            print("main start, 10sec sleep")
            time.sleep(10)

    finally:
        print("cleanup started")

        # kill write
        with w_lock:
            eve_w.set()
        th_w.join()

        # wait until queue is empty
#        que.join()

        # kill read
        with r_lock:
            eve_r.set()
        th_r.join()

        # free connection
        mysql_cursor.close()
        mysql_con.close()

        # free GPIO
        pump.stopPump()
        neo.stopNeoPixel()
        GPIO.output(17, False)
        GPIO.cleanup()

else:
    # do nothing
    print("This do nothing")
