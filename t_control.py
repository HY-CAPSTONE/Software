import connect_mysql as conn
import my_neo as neo
import time
import mysql.connector
from dataclasses import dataclass

@dataclass
class SV:
	TEMP: int=None
	HUMID: int=None
	SOIL: int=None
	TANK: int=None
	def __init__(self, temp, humid, soil, wlvl):
		self.TEMP = temp
		self.HUMID = humid
		self.SOIL = soil
		self.TANK = wlvl

q = SV(22, 22, 22, 22)


try:
	
	#mysql_con, mysql_cursor, pid = conn.connect_DB()
	#mysql_cursor = mysql_con.cursor(dictionary=True)
	while True:

		mysql_con, mysql_cursor, pid = conn.connect_DB()
		
		#mysql_cursor = mysql_con.cursor(dictionary=True)

		rows = conn.select_executor(mysql_con, mysql_cursor, "Control")
		#rows = mysql_cursor.fetchall()
		print(rows)	
		if (rows['CTRL_TYPE']==1):
			neo.doNeoPixel()
		elif (rows['CTRL_TYPE']==2):
			neo.stopNeoPixel()
		else:
			print("MoodLight is On!!")
			neo.doMoodNeoPixel()
		#mysql_cursor.close()
		time.sleep(1)
		conn.insert_executor(mysql_con, mysql_cursor, "Plant2", 99, q, "")
		#mysql_cursor.execute("set foreign_key_checks=0;")

		#mysql_cursor.execute(sql, data)
		time.sleep(1)

finally:
	mysql_cursor.close()
	mysql_con.close()
