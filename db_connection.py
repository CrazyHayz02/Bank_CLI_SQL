import psycopg2

con = psycopg2.connect(
    host="localhost",
    database="bank_db",
    user="bank_user",
    password="securepassword",
    port="5432"
)

cursor = con.cursor()

try:
    cursor.execute("SELECT * FROM users;")
    rows = cursor.fetchall()
except Exception as e:
    print("Database error:", e)
else:
    print (rows)
finally:
    cursor.close()
    con.close()

    