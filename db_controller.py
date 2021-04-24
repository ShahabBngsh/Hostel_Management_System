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

  def get_rooms(self):
    query = "SELECT room_no, capacity, price, floor_no FROM Room;"
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
    query = "SELECT * from Room_Package WHERE room_id=%s;"
    val = (room_no, )
    cursor.execute(query, val)
    return cursor.fetchall()
  
  def get_hostel_details(self, hostel_id):
    query = "SELECT * FROM Hostel WHERE id=%s;"
    val = (hostel_id, )
    cursor.execute(query, val)
    return cursor.fetchall()



dbcont_obj = DBcontroller()
