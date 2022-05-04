import mysql.connector

mysql_con = None

def query_executor(cursor, pram1, pram2, pram3, pram4, pram5):
	sql = "insert into Plant (plant_id, plant_owner, plant_name, plant_info, TEMP) VALUES(%s, %s, %s,  %s, %s)"
	cursor.execute(sql, (pram1, pram2, pram3, pram4, pram5))
	

if __name__ == "__main__":
	try:
		print("start")
		mysql_con = mysql.connector.connect(host="112.170.208.72", port="8080", database="capstone", 
		user="root", password="wlgkcjf21gh")
		print("make connect")
		mysql_cursor = mysql_con.cursor(dictionary=True)
		print("make cursor")
		query_executor(mysql_cursor,"6", "0", "0", "0", "0")
		print("execute query")
		mysql_con.commit()
		mysql_cursor.close()
		print("close cursor")

	except Exception as e:
		print(e.message)

	finally:
		if mysql_con is not None :
			mysql_con.close()
			print("close connection")
