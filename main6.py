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

import requests
import json

import my_dht11 as dht
import my_pump as pump
import my_pcf as pcf
import my_neo as neo
from connect_mysql import connect_DB, insert_executor, select_executor, update_executor

que = queue.Queue(2048)
eve_r = threading.Event()
eve_w = threading.Event()
eve_led = threading.Event()
eve_stream = threading.Event()

r_lock = threading.Lock()
w_lock = threading.Lock()

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


def read_send_sql(mysql_con, mysql_cursor, PID, q, led_state):
    insert_executor(
        mysql_con,
        mysql_cursor,
        "Plant2",
        PID,
        q,
        f"/images/{PID}",
		led_state
    )
    #update_executor(
    #    mysql_con,
    #    mysql_cursor,
    #    "Control",
    #    PID,
    #    led_state
    #)

def sql_query(q, pid):
    try:
        print("start sql query")
        sql_con, sql_cursor, pid = connect_DB()
        time.sleep(1)
        rows = select_executor(sql_con, sql_cursor, "Control")
        print(rows)
        if (rows['CTRL_TYPE']==1):
            neo.doNeoPixel()
            led_state = 1
        elif (rows['CTRL_TYPE']==0):
            neo.stopNeoPixel()
            led_state = 0
        else:
            neo.doMoodNeoPixel()
            led_state = 2
        time.sleep(1)

        read_send_sql(sql_con, sql_cursor, pid, q, led_state)
    finally:
        sql_cursor.close()
        sql_con.close()


def write():
    try:
        while True:
            if eve_w.is_set():
                return 0
            write_global_var()
            print('write done')
            time.sleep(3)
    except:
        return 0
    finally:
        print("writer finally")


def read(potID):
    try:
        while True:
            if eve_r.is_set():
                return 0

            # if que is empty, it will blocked for 100sec
            # after 100sec, it will occur "queue.Empty" exception
            # ** if block=True & timeout=None, this operation can't stop, it is not occur keyboardexception
            q = que.get(block=True, timeout=None)
            que.task_done()
            # ????????? 10?????? ???????????? ????????? ????????? ??????

            # ?????? ?????? ?????????
            print(
                "temp:{} humid:{} soil:{} wlvl:{}".format(
                    q.TEMP,
                    q.HUMID,
                    q.SOIL,
                    q.TANK,
                )
            )


#            api = "https://api.openweathermap.org/data/2.5/weather?q={city}&APPID={key}"
#            url = api.format(city = "Seoul", key = "0276eeb82a71d9b7c07ce64e78fc7a3a")
#            res = requests.get(url)
#            data = json.loads(res.text)
#            if (int(data["sys"]["sunset"]) - time.time() < 5 and int(data["sys"]["sunset"]) - time.time() > -5):
#                neo.doNeoPixel()
#            if (int(data["sys"]["sunrise"]) - time.time() < 5 and int(data["sys"]["sunrise"]) - time.time() > -5):
#                neo.stopNeoPixel()
#            print(int(data["sys"]["sunset"]) - time.time())

            sql_query(q, potID)
            
            TEMP = int(q.TEMP)
            HUMID = int(q.HUMID)
            SOIL = int(q.SOIL)
            TANK = int(q.TANK)
            subprocess.run(["/home/pi/HomeFarm/Bitmap/TFTDisplay", f"{TEMP}", f"{HUMID}", f"{255-SOIL}", f"{TANK}"], stdout=subprocess.DEVNULL)
            print("end monitor")
            time.sleep(1)

            if (SOIL <= 255 and SOIL >= 201):
                print("do")
                print(q.SOIL)
                pump.doPump()
            else :
                print("stop")
                pump.stopPump()

            if (q.TANK < 100) :
                print("TANL LOw")
            else :
                print("TNK HIGH")
            #time.sleep(54)

			# execute LCDcode
    except Exception as e:
        print('reader exception occur', e)
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



def Videostreaming(camera, connection):
    try:
        camera.start_preview()
        time.sleep(2)
        camera.start_recording(connection, format='h264')
        while not eve_stream.is_set():
            camera.wait_recording(100)
    except socket.error as e:
        print("thread trem")
        camera.stop_recording()

def Streaming_camera():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serv_sock:
        serv_sock.bind(('0.0.0.0', 8000))
        serv_sock.listen(0)
        with picamera.PiCamera(resolution="640x480", framerate=24) as camera:
            camera.start_preview()
            time.sleep(1)
            while not eve_stream.is_set():
                connection = serv_sock.accept()[0].makefile('wb')
                th_tmp = threading.Thread(target=Videostreaming, args=(camera, connection))
                th_tmp.start()
                th_tmp.join()

def setup_():
    th1 = threading.Thread(target=write)
    th1.start()

    th2 = threading.Thread(target=read, args=[99])
    th2.start()

    th4 = threading.Thread(target=Streaming_camera )
    th4.start()

    # make thread for I/O
    return th1, th2,  th4


if __name__ == "__main__":
    th_w, th_r, th_stream = setup_()
    # neo.doNeoPixel()
    try:
        while True:
            print("main start, 10sec sleep")
            time.sleep(10)

    finally:
        print("cleanup started")

        # kill write
        
        eve_w.set()
        th_w.join()

        # wait until queue is empty
#        que.join()

        # kill read
        eve_r.set()
        th_r.join()
		
        eve_stream.set()
        th_stream.join()

        # free GPIO
        pump.stopPump()
        neo.stopNeoPixel()

else:
    # do nothing
    print("This do nothing")
