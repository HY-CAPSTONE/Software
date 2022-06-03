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


def select_executor(con, cursor, table):
	try:
		sql = "select * from Control"
		cursor.execute(sql)
		return cursor.fetchone()
	except mysql.connector.errors as e:
		print(e)
		return 0

def insert_executor(mysql_con,cursor, table_name, PID, q, SAVE_PATH, led_state):
	try:
		# TODO parsing code needed
		if table_name == "Plant2":
			sql = ("insert into Plant2 (Plant_id, ICON_pic, LED, TEMP , HUMID, SOIL, TANK, TIME)" 
					"VALUES(%(PID)s, %(ICON)s, %(LED)s, %(TEMP)s, %(HUMID)s, %(SOIL)s, %(TANK)s, NOW());")
			data = {'PID' : PID, 'ICON':0, 'LED':led_state, 'TEMP':q.TEMP, 'HUMID':q.HUMID, 'SOIL':q.SOIL, 'TANK':q.TANK}
			cursor.execute(sql, data)

		elif table_name == "Gallery":
			sql = "insert into Gallery (Plant_id, SAVE_DATE, SAVE_PATH) values(%(PID)s, NOW(), %(SAVE_PATH)s);"
			data = {'PID': PID, 'SAVE_PATH':SAVE_PATH}
			cursor.execute(sql, data)
		elif table_name == "Control":
			sql = "insert into Control (PLANT_ID, CTRL_TYPE) values(%(PID)s, %(led_state)s);"
			data = {"PID":PID, "led_state":led_state}
			cursor.execute(sql, data)
		else:
			print(table_name)
			print("no such tables")

		mysql_con.commit()

	except mysql.connector.errors.OperationalError as e:
		print(e)
		return 0

def update_executor(mysql_con, cursor, table_name, PID, led_state):
	try:
		if table_name == "Control":
			sql = "update Control set PLANT_ID=%(PID)s, CTRL_TYPE=%(led_state)s where 1;"
			data = {"PID":PID, "led_state":led_state}
			cursor.execute(sql, data)
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
