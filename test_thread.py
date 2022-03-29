# thread TEST
# 1. 데몬 스레드가 메인 스레드 종료시 정상 종료되는 것을 확인
# 2. 메인스레드가 exception으로 종료시, 데몬 스레드가 종료되는가 확인
# 3. finally 확인
# 4. 자원을 모두 반환 하는지 확인.

import time
import threading
from connect_mysql import setup_DB, insert_executor

from typing import final
import queue

que = queue.Queue(1)
event1 = threading.Event()
event1.clear()
event2 = threading.Event()
event2.clear()


def push():
    try:
        que.put("HI", block=False)
    except queue.Full:
        print("push queue.full excception")


def thr1(mysql_con, mysql_cursor, potID):
    while True:
        if event1.is_set():
            print("get event, i will finish")
            return 0

        print("thread 2")
        time.sleep(1)


def thr2():
    time.sleep(1)
    while True:
        if event2.is_set():
            print("get event2, i wiill finish")
            return 0
        print("thread 2")
        time.sleep(1)


def main():
    print("hi")
    mysql_con, mysql_cursor, potID = setup_DB()
    try:
        th1 = threading.Thread(target=thr1, daemon=True, args=(mysql_con, mysql_cursor, potID))
        th1.start()
        th2 = threading.Thread(target=thr2)
        th2.start()

        time.sleep(10)
    finally:
        print("main finally")
        time.sleep(1)

        event1.set()
        th1.join()
        event2.set()
        th2.join()
        print("finish join")


main()
