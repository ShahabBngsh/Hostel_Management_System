import db_controller
from flask import Flask, render_template, request

app = Flask(__name__)

#Business Layer code by 'Piyush'
class Users:
    def __init__(self, name, password, cnic, contact_no):
        self.name = name
        self.password = password
        self.cnic = cnic
        self.contact_no = contact_no


class Room:
    def __init__(self, room_no, rate, capacity, tenants):
        self.room_no = room_no
        self.rate = rate
        self.capacity = capacity
        self.tenants = tenants


class Room_manager:
    def __init__(self):
        self.room_list = []

    def get_rooms(self):
        self.room_list = db_controller.dbcont_obj.get_rooms()
        return self.room_list


class Package:
    def __init__(self, price, description):
        self.price = price
        self.description = description


class Package_manager:
    def __init__(self):
        self.package_list = []

    def search_packages(self):
        pass
        #self.room_list = DB.get_rooms
        #return self.room_list
    def search_packages_by_roomNo(self, room_no):
        self.package_list = db_controller.dbcont_obj.search_packages_for_roomNo(room_no)
        return self.package_list


class Room_package:
    def __init__(self, room, package):
        self.room = room
        self.package = package


class Room_package_manager:
    def __init__(self):
        self.room_package_list = []

    def reserve_room_and_package(self, room, package):
        pass
        #self.room_package_list.append(Room_package(room, package))
        #return DB.reserve_room_and_package()



class Hostel():
    def __init__(self, name, address, phone_no=-1, total_rooms=-1):
        self.name = name
        self.address = address
        self.phone_no = phone_no
        self.total_rooms = total_rooms
        self.room_list = []
        self.PM = Package_manager()
        self.RM = Room_manager()
        self.RPM = Room_package_manager()

    def reserve_room_and_package(self, room, package):
        return self.RPM.reserve_room_and_package(room, package)

    def get_rooms(self):
        return self.RM.get_rooms()

    def search_packages(self):
        return self.PM.search_packages()
    def search_packages_by_roomNo(self, roomNo):
        return self.PM.search_packages_by_roomNo(roomNo)


class Invoice:
    def __init__(self, fee_total, fee_status):
        self.fee_total = fee_total
        self.fee_status = fee_status

class Invoice_manager:
    def __init__(self):
        self.invoice_list = []


# -----necessary  objects / variables-------
#object for hostel class
hostel_detail = db_controller.dbcont_obj.get_hostel_details(1)
hostel = Hostel(hostel_detail[0][1], hostel_detail[0][2], hostel_detail[0][3])

bookedRoom=0
bookedPackage=0
totalPrice=0


#route to login.html page
#NOTE: if you want to change function name, then also change in template.html file

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/userHome")
def home():
    return render_template("userHome.html")

@app.route("/searchroom")
def searchroom():
    availRooms = hostel.get_rooms()
    return render_template("searchroom.html", availRooms=availRooms)

@app.route("/roomSelection",methods=['GET', 'POST'])
def roomSelection():
    if request.method == 'POST':
        if request.form.get("selectRoom"):
            global bookedRoom
            bookedRoom=request.form["RoomNo"]
            package_list = hostel.search_packages_by_roomNo(bookedRoom)
            # print(request.form["RoomNo"])
            #packages=getPackages(RoomNo)
            return render_template("searchPackages.html",roomNo=bookedRoom, packages=package_list)#, packages=packages

@app.route("/bookingConfirmation", methods=['GET','POST'])
def bookingConfirmation():
    if request.method == 'POST':
        if request.form.get("selectPackage"):
            global bookedRoom
            global totalPrice
            print("usama")
            return render_template("bookingConfirmation.html", bookedRoom=bookedRoom, bookedPackage=request.form["packageNo"],totalPrice=10000)#, packages=packages

# @app.package("/searchPackage")
# def searchPackage():
#     #function to get package of requested roomNo
#     return render_template("searchroom.html", availRooms=availRooms)

# @app.route("/packageSelection")
# def packageSelection():
#     if request.method == 'POST':
#         pass
        #send package to BL
if __name__ == "__main__":
    app.run(debug=True)