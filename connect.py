# Module Imports
import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="wlgkcjf21gh",
        host="112.170.208.72",
        port=8080,
        database="testDB"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()

# some_name = "Georgi"
# cur.execute(
#     "SELECT first_name,last_name FROM employees WHERE first_name=?", (some_name,))

# for first_name, last_name in cur:
#     print(f"First name: {first_name}, Last name: {last_name}")

# insert information
try:
    cur.execute(
        "INSERT INTO Planter (Ptype,Pdate) VALUES (?, ?)", ("Maria", "2015-04-19 12:11:32"))
except mariadb.Error as e:
    print(f"Error: {e}")

conn.commit()
print(f"Last Inserted ID: {cur.lastrowid}")

conn.close()
