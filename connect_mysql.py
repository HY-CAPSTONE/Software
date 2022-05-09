import mysql.connector
import time
import datetime

def connect_DB():
    pid = 99
    mysql_con = mysql.connector.connect(
        host="112.170.208.72", port="8080", database="capstone", user="root", password="wlgkcjf21gh"
    )
    mysql_cursor = mysql_con.cursor(dictionary=True)
    return mysql_con, mysql_cursor, pid


def check_PID(cursor, PID):
    sql = "select * from Planter where PID = {}".format(PID)
    cursor.execute(sql)
    row = cursor.fetchone()
    if row == None:
        return False
    else:
        return True


def insert_executor(mysql_con,cursor, table_name, PID, q, SAVE_PATH):
    try:
        # TODO parsing code needed
        if table_name == "Plant":
            sql = ("insert into Plant (Plant_id, ICON_pic, LED, TEMP , HUMID, SOIL, TANK, TIME)" 
                  "VALUES(%(PID)s, %(ICON)s, %(LED)s, %(TEMP)s, %(HUMID)s, %(SOIL)s, %(TANK)s, NOW());")
            data = {'PID' : PID, 'ICON':0, 'LED':0, 'TEMP':q.TEMP, 'HUMID':q.HUMID, 'SOIL':q.SOIL, 'TANK':q.TANK}
            cursor.execute(sql, data)

        elif table_name == "Gallery":
            sql = "insert into Gallery (Plant_id, SAVE_DATE, SAVE_PATH) values(%(PID)s, NOW(), %(SAVE_PATH)s);"
            data = {'PID': PID, 'SAVE_PATH':SAVE_PATH}
            cursor.execute(sql, data)

        else:
            print("no such tables")

        mysql_con.commit()

    except mysql.connector.errors.OperationalError as e:
        print(e)
        return 0


if __name__ == "__main__":
    try:
        from dataclasses import dataclass

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

        print("start")
        mysql_con = mysql.connector.connect(host="112.170.208.72", port="8080", database="capstone", user="root", password="wlgkcjf21gh")
        mysql_cursor = mysql_con.cursor(dictionary=True)
        pid = 99
        # mysql_con, mysql_cursor, pid = connect_DB()

        # for i in range(10):
        #     currtime = datetime.datetime.now()
        #     print(currtime)
        #     insert_executor(
        #         mysql_cursor, mysql_con, "Sensors", str(pid), str(currtime), 99, 99, 99, 99, 99, 99
        #     )
        #     time.sleep(1)
        q = SensorValues(-1, -1, -1, -1)
        insert_executor(mysql_con, mysql_cursor, "Plant", pid, q, f"/images/{pid}")
        mysql_con.commit()
        print("query_executor")

        mysql_cursor.close()

    except Exception as e:
        print(e.message)

    finally:
        if mysql_con is not None:
            mysql_con.close()
