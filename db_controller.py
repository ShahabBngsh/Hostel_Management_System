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

    error = None
    print(cursor.rowcount, "rows returned")
    if cursor.rowcount == -1 or cursor.rowcount == 0:
      error = "_ERROR: 400"
    return None, error

  def get_rooms(self):
    query = "SELECT room_no, capacity, price, floor_no FROM Room;"
    cursor.execute(query)
    result = cursor.fetchall()

    error = None
    print(cursor.rowcount, "rows returned")
    if cursor.rowcount == -1 or cursor.rowcount == 0:
      error = "_ERROR: 404"
    return result, error

  def add_package(self, package_id, price, description):
    query = "INSERT INTO PACKAGE (price, description) VALUES (%s, %s);"
    val = (package_id, price, description)
    cursor.executemany(query, val)
    mydb.commit()

    error = None
    print(cursor.rowcount, "rows returned")
    if cursor.rowcount == -1 or cursor.rowcount == 0:
      error = "_ERROR: 400"
    return None, error

  def get_packages(self):    
    query = "SELECT * from packages;"
    cursor.execute(query)
    result = cursor.fetchall()

    error = None
    print(cursor.rowcount, "rows returned")
    if cursor.rowcount == -1 or cursor.rowcount == 0:
      error = "_ERROR: 404"
    return result, error
  
  def search_packages_for_roomNo(self, room_no):    
    query = "SELECT * from Room_Package WHERE room_id=%s;"
    val = (room_no, )
    cursor.execute(query, val)
    result = cursor.fetchall()

    error = None
    print(cursor.rowcount, "rows returned")
    if cursor.rowcount == -1 or cursor.rowcount == 0:
      error = "_ERROR: 404"
    return result, error
  
  def get_hostel_details(self, hostel_id):
    query = "SELECT * FROM Hostel WHERE id=%s;"
    val = (hostel_id, )
    cursor.execute(query, val)
    result = cursor.fetchone()

    error = None
    print(cursor.rowcount, "rows returned")
    if cursor.rowcount == -1 or cursor.rowcount == 0:
      error = "_ERROR: 404"
    return result, error

  def gen_invoice(self, due_payment, room_package_id, user_id,roomNo):
    query = "INSERT INTO Invoice (due_amount, paid_amount, room_package_id, user_id) VALUES (%s,%s, %s, %s);"
    val = (due_payment,0, room_package_id, user_id)
    cursor.execute(query, val)

    query2 = "UPDATE Room SET reserve=%s WHERE room_no = %s;"
    val2 = (1, roomNo)
    cursor.execute(query2, val2)
    mydb.commit()

    error = None
    print(cursor.rowcount, "rows returned")
    if cursor.rowcount == -1 or cursor.rowcount == 0:
      error = "_ERROR: 400"
    return None, error
  
  def get_all_users(self):
    query = "SELECT * FROM User;"
    cursor.execute(query)
    result = cursor.fetchall()

    error = None
    print(cursor.rowcount, "rows returned")
    if cursor.rowcount == -1 or cursor.rowcount == 0:
      error = "_ERROR: 404"
    return result, error

  def get_user(self, username):
    query = "SELECT * FROM User WHERE username=%s;"
    val = (username, )
    cursor.execute(query, val)
    result = cursor.fetchone()
    error = None

    if cursor.rowcount == -1 or cursor.rowcount == 0:
      error = "_ERROR: 404"
    return result, error

  def register_user(self, name, password, cnic, contact_no):
    query = "INSERT INTO User (name, password, cnic, contact_no) VALUES (%s, %s, %s, %s);"
    val = (name, password, cnic, contact_no)
    cursor.execute(query, val)
    mydb.commit()
    error = None

    if cursor.rowcount == -1 or cursor.rowcount == 0:
      error = "_ERROR: 400"
    return None, error

  def get_due_payment(self, user_id, room_package_id):
    query = "SELECT due_amount FROM Invoice WHERE user_id=%s and room_package_id=%s;"
    val = (user_id, room_package_id)
    cursor.execute(query, val)
    result = cursor.fetchone()

    error = None
    print(cursor.rowcount, "rows returned")
    if cursor.rowcount == -1 or cursor.rowcount == 0:
      error = "_ERROR: 404"
    return result, error

  def pay_cash(self, user_id, room_package_id, due_amount, payment):
    query = "UPDATE Invoice SET paid_amount=%s, due_amount=%s WHERE user_id=%s and room_package_id=%s;"
    val = (payment, (due_amount-payment), user_id, room_package_id)
    cursor.execute(query, val)
    mydb.commit()

    error = None
    print(cursor.rowcount, "rows affected")
    if cursor.rowcount == -1 or cursor.rowcount == 0:
      error = "_ERROR: 400"
    return None, error
  
  def checkout(self, roomno):
    query = "UPDATE Room SET reserve=%s WHERE room_no = %s;"
    val = (0,roomno)
    cursor.execute(query, val)
    mydb.commit()

    error = None
    print(cursor.rowcount, "rows affected")
    if cursor.rowcount == -1 or cursor.rowcount == 0:
      error = "_ERROR: 404"
    return None, error

dbcont_obj = DBcontroller()
