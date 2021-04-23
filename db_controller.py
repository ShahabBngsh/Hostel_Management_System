import mysql.connector
import datetime

mydb = mysql.connector.connect(
  host = 'localhost',
  user = 'root',
  password = 'root',
  auth_plugin = 'mysql_native_password'
)

print(mydb)
cursor = mydb.cursor()
cursor.execute('use hostel_db')

class DBcontroller:
  def __init__(self):
    pass
  def addRooms(self,roomNo,rate,capacity):
    query = "INSERT INTO ROOM ( roomNo,rate,capacity) VALUES (%s, %s,%s)"
    val = (roomNo,rate,capacity)
    cursor.execute(query, val)
    mydb.commit()
    return 'Room added!'

  def search_rooms(self):
    query = "SELECT roomNo,rate,capacity FROM ROOM;"
    cursor.execute(query)
    return cursor.fetchall()

  def add_Package(self,package_id,price,description):
    query = "INSERT INTO PACKAGE ( price,description) VALUES (%s, %s);"
    val = (package_id, price, description)
    cursor.executemany(query, val)
    mydb.commit()
    print(cursor.rowcount, "record inserted.")
    return "Package added"

  def search_packages(self):    
    query = "SELECT * from packages;"
    cursor.execute(query)
    return cursor.fetchall()



obj = DBcontroller
