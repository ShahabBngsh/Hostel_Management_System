#just testing database from python

import mysql.connector

mydb = mysql.connector.connect(
  host = 'localhost',
  user = 'root',
  password = 'mysql@usama',
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
# val = [(202, 9000, 1, 2, 1),
# (203, 10000, 1, 2, 1),
# (204, 9000, 1, 2, 1)]
# cursor.executemany(sql, val)

# mydb.commit()

# print(cursor.rowcount, "record inserted.")



# ############################################
# query = "SELECT room_no, price, capacity FROM Room;"
# cursor.execute(query)
# x=cursor.fetchall()
# for each in x:
#     print(each)




# ###############  INSERT INTO PACKAGE  #############################

# sql = "INSERT INTO Package (price, description) VALUES (%s, %s);"
# val = [(2500,"refrigerator, Room Cooler"),
# (3500,"refrigerator, Microwave, Room Cooler"),
# (5000,"refrigerator, Microwave, A/C, HEATER")]
# cursor.executemany(sql, val)
# mydb.commit()

# print(cursor.rowcount, "record inserted.")


# #########################################
# query = "SELECT * from PACKAGE;"
# cursor.execute(query)
# pkg=cursor.fetchall()
# for i in pkg:
#     print(i)


######################  INSERT INTO ROOM_PACKAGE  ###########################
# sql = "INSERT INTO Room_Package (charges, room_id, package_id) VALUES (%s, %s,%s);"
# val = [
#     (4500,202,4),
#     (5500,202,5),
#     (6500,202,5),
#     (7500,203,6),
#     (6500,203,5),
#     (5500,203,5),
#     (9000,203,6),
#     (13000,204,4),
#     ]
# cursor.executemany(sql, val)
# mydb.commit()
# print(cursor.rowcount, "record inserted.")

#################################################################


##################  INSERT INTO USER  ###########################
# sql = "INSERT INTO User (name, password, cnic) VALUES (%s, %s, %s);"
# val = [("Bilal","1234", "123456789")]
# cursor.executemany(sql, val)

# sql = "INSERT INTO User (name, password) VALUES (%s, %s);"
# val = [("John", "2345")]
# cursor.executemany(sql, val)

# mydb.commit()

# print(cursor.rowcount, "record inserted.")
ALTER TABLE hostel_db.Room ADD reserve BOOL DEFAULT 0 NULL;

##################################################################