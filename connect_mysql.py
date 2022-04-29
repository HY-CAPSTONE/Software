import mysql.connector
import time
import datetime


# connection, cursor, pid를 리턴.
# 자신의 PID가 DB에 없으면, wait
def setup_DB():
    pid = 99
    mysql_con = create_sql_connector("112.170.208.72", "8910", "testDB", "root", "wlgkcjf21gh")

    mysql_cursor = create_sql_cursor(mysql_con)

    while not check_PID(mysql_cursor, pid):
        print("no such PID")
        time.sleep(1)

    return mysql_con, mysql_cursor, pid


def create_sql_connector(host, port, db, user, pw):
    mysql_con = mysql.connector.connect(host=host, port=port, database=db, user=user, password=pw)
    return mysql_con


def create_sql_cursor(mysql_con):
    mysql_cursor = mysql_con.cursor(dictionary=True)
    return mysql_cursor


def check_PID(cursor, PID):
    sql = "select * from Planter where PID = {}".format(PID)
    cursor.execute(sql)
    row = cursor.fetchone()
    if row == None:
        return False
    else:
        return True


def insert_executor(
    cursor, mysql_con, table_name, PID, Stime, Temp, Humid, SoilMois, Wlevel, Cds, Wflow
):
    try:
        if table_name == "Sensors":
            sql = "insert into Sensors(PID, Stime, Temp, Humid, SoilMois, Wlevel, Cds, Wflow) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);"
        elif table_name == "Planter":
            sql = "insert into Planter(Ptype, Pdate) values(%s, %s);"

        else:
            print("no such tables")

        cursor.execute(sql, (PID, Stime, Temp, Humid, SoilMois, Wlevel, Cds, Wflow))
        mysql_con.commit()

    except mysql.connector.errors.OperationalError as e:
        print(e)
        return 0


if __name__ == "__main__":
    try:
        print("start")
        mysql_con, mysql_cursor, pid = setup_DB()

        # insert_executor(mysql_cursor, "Planter",
        #                 "param1", "2021-11-7 12:53:33")

        for i in range(10):
            currtime = datetime.datetime.now()
            print(currtime)
            insert_executor(
                mysql_cursor, mysql_con, "Sensors", str(pid), str(currtime), 99, 99, 99, 99, 99, 99
            )
            time.sleep(1)
        print("query_executor")

        mysql_cursor.close()

    except Exception as e:
        print(e.message)

    finally:
        if mysql_con is not None:
            mysql_con.close()
