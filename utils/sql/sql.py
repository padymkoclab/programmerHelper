
import psycopg2

connection = psycopg2.connect(user='temp_user', database='temp_db', password='temp', host='localhost')

try:
    file_sql_code = open('./sql.sql', 'r')

    sql_code = file_sql_code.read()

    cursor = connection.cursor()
    cursor.execute(sql_code)
    result = cursor.fetchall()
    for i in result:
        print(i)
    connection.commit()
finally:
    file_sql_code.close()
    connection.close()
