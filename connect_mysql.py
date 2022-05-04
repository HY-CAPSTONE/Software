from main3 import SensorValues
import mysql.connector
import time
import datetime


# connection, cursor, pid를 리턴.
# 자신의 PID가 DB에 없으면, wait
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


def insert_executor(cursor, mysql_con, table_name, PID, q, SAVE_PATH):
    try:
        # TODO parsing code needed
        if table_name == "Plant":
            sql = "insert into Plant (PID, ICON, LED, TEMP , HUMID, SOIL, TANK, TIME) VALUES(%s, %s, %s, %s, %s, %s, %s, NOW());"
            cursor.execute(sql, (PID, q.ICON, q.LED, q.TEMP, q.HUMID, q.SOIL, q.TANK))

        elif table_name == "Gallery":
            sql = "insert into Gallery (PID, SAVE_DATE, SAVE_PATH) values(%s, NOW(), %s);"
            cursor.execute(sql, (PID, SAVE_PATH))

        else:
            print("no such tables")

        mysql_con.commit()

    except mysql.connector.errors.OperationalError as e:
        print(e)
        return 0


if __name__ == "__main__":
    try:
        print("start")
        mysql_con, mysql_cursor, pid = connect_DB()

        # for i in range(10):
        #     currtime = datetime.datetime.now()
        #     print(currtime)
        #     insert_executor(
        #         mysql_cursor, mysql_con, "Sensors", str(pid), str(currtime), 99, 99, 99, 99, 99, 99
        #     )
        #     time.sleep(1)
        q = SensorValues(-1, -1, -1, -1)
        insert_executor(mysql_con, mysql_cursor, "Plant", pid, q, f"/images/{pid}")

        print("query_executor")

        mysql_cursor.close()

    except Exception as e:
        print(e.message)

    finally:
        if mysql_con is not None:
            mysql_con.close()
