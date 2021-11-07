import mysql.connector
import time


# connection, cursor, pid를 리턴.
# 자신의 PID가 DB에 없으면, wait
def setup_DB():
    pid = 99
    mysql_con = create_sql_connector(
        "112.170.208.72", "20", "testDB", "root", "wlgkcjf21gh")

    mysql_cursor = create_sql_cursor(mysql_con)

    while not check_PID(mysql_cursor, pid):
        print("no such PID")
        time.sleep(1)

    return mysql_con, mysql_cursor, pid


def create_sql_connector(host, port, db, user, pw):
    mysql_con = mysql.connector.connect(
        host=host, port=port, database=db, user=user, password=pw)
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


def insert_executor(cursor, table_name, param1, param2):
    if table_name == "Sensors":
        sql = "insert into Sensors(Stiem, PID, Temp, Humid, SoilMois, Wlevel, Cds, Wflow) VALUES();"
    elif table_name == "Planter":
        sql = "insert into Planter(Ptype, Pdate) values(%s, %s);"

    else:
        print("no such tables")

    cursor.execute(sql, (param1, param2))
    mysql_con.commit()


if __name__ == "__main__":
    try:
        print("start")
        mysql_con, mysql_cursor, pid = setup_DB()

        insert_executor(mysql_cursor, "Planter",
                        "param1", "2021-11-7 12:53:33")
        print("query_executor")

        mysql_cursor.close()

    except Exception as e:
        print(e.message)

    finally:
        if mysql_con is not None:
            mysql_con.close()
