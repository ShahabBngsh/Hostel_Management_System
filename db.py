#just testing database from python

import mysql.connector

mydb = mysql.connector.connect(
  host = 'localhost',
  user = 'root',
  password = 'root',
  auth_plugin = 'mysql_native_password'
)

print(mydb)
cursor = mydb.cursor()
cursor.execute('use hostel_db')

# database dummy data
# cursor.execute("INSERT INTO test (ID,name) VALUES ('1','test')")
# mydb.commit()

################ INSERT INTO HOSTEL #############################
# sql = "INSERT INTO Hostel (ID, name, address, phone_no) VALUES (%s, %s, %s, %s);"
# val = [(1, "Royal Hostel", "F11/2 street 16", "12345678")]
# cursor.executemany(sql, val)
# mydb.commit()

################  INSERT INTO ROOM  #############################

# sql = "INSERT INTO Room (room_no, price, capacity, floor_no, hostel_id) VALUES (%s, %s, %s, %s, %s);"
# val = [(202, 9000, 3, 2, 1),
# (203, 10000, 2, 2, 1),
# (204, 9000, 1, 2, 1)]
# cursor.executemany(sql, val)

# mydb.commit()

# print(cursor.rowcount, "record inserted.")



#############################################
# query = "SELECT room_no, price, capacity FROM Room;"
# cursor.execute(query)
# x=cursor.fetchall()
# for each in x:
#     print(each)




################  INSERT INTO PACKAGE  #############################

# sql = "INSERT INTO Package (price, description) VALUES (%s, %s);"
# val = [(2500,"refrigerator, Room Cooler"),
# (3500,"refrigerator, Microwave, Room Cooler"),
# (5000,"refrigerator, Microwave, A/C, HEATER")]
# cursor.executemany(sql, val)
# mydb.commit()

# print(cursor.rowcount, "record inserted.")


##########################################
# query = "SELECT * from PACKAGE;"
# cursor.execute(query)
# pkg=cursor.fetchall()
# for i in pkg:
#     print(i)

