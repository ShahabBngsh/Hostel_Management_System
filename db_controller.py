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

  def gen_invoice(self, due_payment, room_package_id, user_id,roomNo):
    query = "INSERT INTO Invoice (due_amount, paid_amount, room_package_id, user_id) VALUES (%s,%s, %s, %s);"
    val = (due_payment,0, room_package_id, user_id)
    cursor.execute(query, val)
    mydb.commit()
    query2 = "UPDATE Room SET reserve=%s WHERE room_no = %s;"
    val2 = (1,roomNo)
    cursor.execute(query2, val2)
    mydb.commit()
    print(cursor.rowcount, "record inserted.")
    return "Invoice generated"
  
  def get_all_users(self):
    query = "SELECT * FROM User;"
    cursor.execute(query)
    return cursor.fetchall()

  def get_due_payment(self, user_id):
    query = "SELECT user_id, due_amount FROM Invoice WHERE user_id=%s;"
    val = (user_id, )
    cursor.execute(query, val)
    return cursor.fetchall()

  def get_due_payment(self, user_id, room_package_id):
    query = "SELECT user_id, due_amount FROM Invoice WHERE user_id=%s and room_package_id=%s;"
    val = (user_id, room_package_id)
    cursor.execute(query, val)
    return cursor.fetchall()
  
  # def pay_amount(self, user_id, room_package_id, due_amount, payment):
  #   print(user_id, room_package_id, due_amount, payment)
  #   query = "UPDATE Invoice SET paid_amount = %s WHERE user_id=%s and room_package_id=%s;"
  #   val = (payment, user_id, room_package_id)
  #   cursor.execute(query, val)
  #   mydb.commit()
  #   print(cursor.rowcount, "record(s) affected")
  #   return True

  def pay_amount(self, user_id, room_package_id, due_amount, payment):
    query = "UPDATE Invoice SET paid_amount=%s, due_amount=%s WHERE user_id=%s and room_package_id=%s;"
    val = (payment, (due_amount-payment), user_id, room_package_id)
    cursor.execute(query, val)
    mydb.commit()
    print(cursor.rowcount, "record(s) affected")
    return True

  def cancel_booking(self, user_id, room_package_id):
    query = "DELETE from invoice where user_id=%s and room_package_id=%s;"
    val = (user_id, room_package_id)
    cursor.execute(query, val)
    mydb.commit()
    print(cursor.rowcount, "record(s) affected")

    query = "UPDATE ROOM set reserve=0 where room_no =(select room_id from room_package where id=%s);"
    print("!@!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(room_package_id)
    val = (room_package_id,)
    cursor.execute(query, val)
    mydb.commit()
    print(cursor.rowcount, "record(s) affected")
    return True

  

  def search_customer(self):
    query = "SELECT id, name,cnic,contact_no FROM user;"
    cursor.execute(query)      
    return cursor.fetchall()



  def checkout(self, roomno):
    query = "UPDATE Room SET reserve=%s WHERE room_no = %s;"
    val = (0,roomno)
    cursor.execute(query, val)
    mydb.commit()
    print((cursor.rowcount, "record(s) affected"))
    return True 

  def update_room_price(self, roomId, newPrice):
    query = "UPDATE Room SET price=%s WHERE room_no=%s"
    val = (newPrice,roomId)
    cursor.execute(query, val)
    mydb.commit()
    print((cursor.rowcount, "record(s) affected"))
    return True
  def update_package_price(self,packageId, newPrice):
    query = "UPDATE package SET price=%s WHERE id=%s"
    val = (newPrice,packageId)
    cursor.execute(query, val)
    mydb.commit()
    print((cursor.rowcount, "record(s) affected"))
    return True

  def get_tenant_record(self):
    query = "SELECT * FROM invoice;"
    cursor.execute(query)      
    return cursor.fetchall()
dbcont_obj = DBcontroller()
