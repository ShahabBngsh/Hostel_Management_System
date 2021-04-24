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
  def add_room(self, room_no, price, capacity):
    query = "INSERT INTO ROOM (room_no, price, capacity) VALUES (%s, %s,%s)"
    val = (room_no,price,capacity)
    cursor.execute(query, val)
    mydb.commit()
    return 'Room added!'

  def search_rooms(self):
    query = "SELECT room_no, price, capacity FROM ROOM;"
    cursor.execute(query)
    return cursor.fetchall()

  def add_package(self, package_id, price, description):
    query = "INSERT INTO PACKAGE (price, description) VALUES (%s, %s);"
    val = (package_id, price, description)
    cursor.executemany(query, val)
    mydb.commit()
    print(cursor.rowcount, "record inserted.")
    return "Package added"

  def get_packages(self):    
    query = "SELECT * from packages;"
    cursor.execute(query)
    return cursor.fetchall()
  
  def search_packages_for_roomNo(self, room_no):    
    query = "SELECT * from Room_Package WHERE room_id=room_no;"
    cursor.execute(query)
    return cursor.fetchall()



dbcont_obj = DBcontroller()
