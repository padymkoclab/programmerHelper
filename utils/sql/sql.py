
import psycopg2


connection = psycopg2.connect(user='test_user', database='temp', password='test', host='localhost')

# try read from file sql.sql
sql = """


"""

try:
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchone()
    print(result)
    # connection.commit()
finally:
    connection.close()
