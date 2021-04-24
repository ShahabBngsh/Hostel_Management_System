from flask import Flask, render_template
from db_controller import *

app = Flask(__name__)

availRooms = [
    {
        "roomNo": 101,
        "capacity": 4,
        "rate": 15000,
        "floorNo": 1
    },

    {
        "roomNo": 102,
        "capacity": 3,
        "rate": 16000,
        "floorNo": 1
    },

    {
        "roomNo": 103,
        "capacity": 3,
        "rate": 16000,
        "floorNo": 1
    },

    {
        "roomNo": 201,
        "capacity": 4,
        "rate": 15000,
        "floorNo": 2
    },

    {
        "roomNo": 202,
        "capacity": 3,
        "rate": 16000,
        "floorNo": 2
    },

    {
        "roomNo": 203,
        "capacity": 3,
        "rate": 16000,
        "floorNo": 2
    },

    {
        "roomNo": 301,
        "capacity": 2,
        "rate": 17000,
        "floorNo": 2
    }
]

#Business Layer code by 'Piyush'
class users:
    def __init__(self, name, password, cnic, contact_no):
        self.name = name
        self.password = password
        self.cnic = cnic
        self.contact_no = contact_no


class room:
    def __init__(self, room_no, rate, capacity, tenants):
        self.room_no = room_no
        self.rate = rate
        self.capacity = capacity
        self.tenants = tenants


class room_manager:
    def __init__(self):
        self.room_list = []

    def search_rooms(self):
        pass
        # self.room_list = DB.search_rooms
        # return self.room_list


class package:
    def __init__(self, price, description):
        self.price = price
        self.description = description


class package_manager:
    def __init__(self):
        self.package_list = []

    def search_packages(self):
        pass
        #self.room_list = DB.search_rooms
        #return self.room_list
    def search_packages_by_roomNo(self, room_no):
        return dbcont_obj.search_packages_for_roomNo(room_no)


class room_package:
    def __init__(self, room, package):
        self.room = room
        self.package = package


class room_package_manager:
    def __init__(self):
        self.room_package_list = []

    def reserve_room_and_package(self, room, package):
        pass
        #self.room_package_list.append(room_package(room, package))
        #return DB.reserve_room_and_package()



class hostel():
    def __init__(self, address, phone_no, total_rooms):
        self.address = address
        self.phone_no = phone_no
        self.total_rooms = total_rooms
        self.room_list = []
        self.PM = package_manager()
        self.RM = room_manager()
        self.RPM = room_package_manager()

    def reserve_room_and_package(self, room, package):
        return self.RPM.reserve_room_and_package(room, package)

    def search_rooms(self):

        return self.RM.search_rooms()

    def search_packages(self):
        return self.PM.search_packages()
    def search_packages_by_roomNo(self, roomNo):
        return self.RM.search_packages_by_roomNo(roomNo)

class invoice:
    def __init__(self, fee_total, fee_status):
        self.fee_total = fee_total
        self.fee_status = fee_status

class invoice_manager:
    def __init__(self):
        self.invoice_list = []

#route to login.html page
#NOTE: if you want to change function name, then also change in template.html file

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/searchroom")
def searchroom():
    return render_template("searchroom.html", availRooms=availRooms)


if __name__ == "__main__":
    app.run(debug=True)