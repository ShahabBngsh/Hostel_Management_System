from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
from decimal import *
import credentials  # importing our credentials from credentials.py


import db_controller
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'
#Business Layer code by 'Piyush'
class Users:
    def __init__(self, name, password, cnic, contact_no):
        self.name = name
        self.password = password
        self.cnic = cnic
        self.contact_no = contact_no
        
class User_Manager:
    def __init__(self):
        self.users = []

    def search_customer(self):
        return db_controller.dbcont_obj.search_customer()


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
        if self.room_list is None or self.room_list == '':
            print("\tWarning: empty list returned\n")
            return []
        else:
            return self.room_list

    def checkout(self, roomno):
        rowcount = db_controller.dbcont_obj.checkout(roomno)
        if rowcount <= 0:
            return False
        return True

    def update_room_price(self, room_id, price):
        if (room_id is None) or (price is None) or room_id == '' or price == '':
            return False
        if (int(float(room_id)) < 1) or (int(float(price)) < 0):
            return False
        else:
            rows_affected = db_controller.dbcont_obj.update_room_price(room_id, price)
            if rows_affected < 1:
                return False
            print(f"Price updated for room no: {room_id}, new price: {price}")
            return True


class Package:
    def __init__(self, price, description):
        self.price = price
        self.description = description


class Package_manager:
    def __init__(self):
        self.package_list = []

    def search_packages(self):
        pass
    
    def search_packages_by_roomNo(self, room_no):
        self.package_list, rowcount = db_controller.dbcont_obj.search_packages_for_roomNo(room_no)
        if int(room_no) <= 0:
            print("ERROR: Invalid value\n")
            return []
        if rowcount <= 0 or self.package_list == '':
            print("WARNING: no rooms exist against given room no\n")
            return []
        return self.package_list

    def update_package_price(self, package_id, price):
        if (package_id is None) or (price is None) or package_id == '' or price == '':
            return False
        if (int(float(package_id)) < 1) or (int(float(price)) < 0):
            return False
        else:
            rows_affected = db_controller.dbcont_obj.update_package_price(package_id, price)
            if rows_affected < 1:
                return False
            print(f"Price updated for package no: {package_id}, new price: {price}")
            return True
    


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

    def cancel_booking(self, user_id, room_pkg_id):
        if user_id is None or room_pkg_id is None or user_id == '' or room_pkg_id == '':
            return False
        rowcount =  db_controller.dbcont_obj.cancel_booking(user_id, room_pkg_id)
        if rowcount <= 0:
            return False
        return True
    def check_due_payments(self, user_id, room_pkg_id):
        if user_id is None or room_pkg_id is None or user_id == '' or room_pkg_id == '':
            print("ERROR: invalid ids are entered\n")
            return None
        else:
            payment, rowcount = db_controller.dbcont_obj.get_due_payment(user_id, room_pkg_id)[0][1]
            if rowcount <= 0:
                print("Invoice doesn't exist againt given user\n")
                return None
            else:
                return payment

    def check_customer_room_package(self, user_id, room_pkg_id):
        pass
        #return user details for tenant



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
        self.IM = Invoice_manager()
        self.UM = User_Manager()

    def reserve_room_and_package(self, room, package):
        return self.RPM.reserve_room_and_package(room, package)

    def get_rooms(self):
        return self.RM.get_rooms()

    def search_packages(self):
        return self.PM.search_packages()

    def search_packages_by_roomNo(self, roomNo):
        return self.PM.search_packages_by_roomNo(roomNo)

    def get_due_payment(self, userid):
        return self.IM.get_due_payment(userid)

    def cash_payment(self, room_package, charges, payment):
        return self.IM.cash_payment(room_package, charges, payment)

    def credit_payment(self, card_no, expiration_date, amount, merchant_id = 1):
        return self.IM.credit_payment(card_no, expiration_date, amount, merchant_id)

    def checkout(self, roomno):
        return self.RM.checkout(roomno)

    def gen_invoice(self, due_payment, room_package_id, user_id,roomNo):
        return self.IM.gen_invoice(due_payment, room_package_id, user_id,roomNo)
    
    def get_all_users(self):
        return db_controller.dbcont_obj.get_all_users()

    def get_due_payment(self, userid, room_package_id):
        return self.IM.get_due_payment(userid, room_package_id)
    
    def pay_amount(self, user_id, room_package_id, due_amount, payment):
        return self.IM.cash_payment(user_id, room_package_id, due_amount, payment)

    def cancel_booking(self, user_id, room_pkg_id):
        return self.RPM.cancel_booking(user_id, room_pkg_id)

    def search_customer(self):
        return self.UM.search_customer()

    def check_due_payments(self, user_id, room_pkg_id):
        return self.RPM.check_due_payments(user_id,room_pkg_id)

    def get_all_due_payments(self):
        return self.IM.get_all_due_payments()

    def check_customer_room_package(self, user_id, room_pkg_id):
        return self.RPM.check_customer_room_package(user_id, room_pkg_id)

    def update_room_price(self, room_id, price):
        return self.RM.update_room_price(room_id,price)

    def update_package_price(self, package_id, price):
        return self.PM.update_package_price(package_id,price)

    def get_tenant_record(self):
        return self.IM.get_tenant_record()

class Invoice:
    def __init__(self, fee_total, fee_status):
        self.fee_total = fee_total
        self.fee_status = fee_status

class Invoice_manager:
    # Authentication steps using Authorize.Net API credentials
    merchantAuth = apicontractsv1.merchantAuthenticationType()
    merchantAuth.name = credentials.api_login_name
    merchantAuth.transactionKey = credentials.transaction_key

    def __init__(self):
        self.invoice_list = []

    def cash_payment(self, user_id, room_package_id, due_amount, payment):
        if user_id is None or room_package_id is None or payment is None or due_amount is None:
            return None
        if user_id == '' or room_package_id == '' or payment == '' or due_amount == '':
            return None
        self.invoice_list.append(Invoice(due_amount, payment))
        if payment >= due_amount:
            ret_val = db_controller.dbcont_obj.pay_amount(user_id, room_package_id, due_amount, due_amount)
            if (ret_val):
                return (payment - due_amount)
            else:
                return None
        else:
            ret_val = db_controller.dbcont_obj.pay_amount(user_id, room_package_id, due_amount, payment)
            if (ret_val):
                return (payment - due_amount)
            else:
                return None

    def credit_payment(self, card_no, expiration_date, amount, merchant_id):
        if (self.charge(card_no, expiration_date, amount, merchant_id) != -1):
            self.invoice_list.append(invoice(amount, amount))
        else:
            return -1
    

    def get_due_payment(self, userid , room_package_id):
        return db_controller.dbcont_obj.get_due_payment(userid, room_package_id)

    def charge(self, card_number, expiration_date, amount, merchant_id):
        creditCard = apicontractsv1.creditCardType()
        creditCard.cardNumber = card_number
        creditCard.expirationDate = expiration_date

        payment = apicontractsv1.paymentType()
        payment.creditCard = creditCard

        transactionrequest = apicontractsv1.transactionRequestType()
        transactionrequest.transactionType = "authCaptureTransaction"
        transactionrequest.amount = amount
        transactionrequest.payment = payment

        createtransactionrequest = apicontractsv1.createTransactionRequest()
        createtransactionrequest.merchantAuthentication = self.merchantAuth
        createtransactionrequest.refId = merchant_id

        createtransactionrequest.transactionRequest = transactionrequest
        createtransactioncontroller = createTransactionController(createtransactionrequest)
        createtransactioncontroller.execute()

        response = createtransactioncontroller.getresponse()

        if (response.messages.resultCode == "Ok"):
            return str(response.transactionResponse.transId)
        else:
            print("response code: " + str(response.messages.resultCode))
            return -1

    def gen_invoice(self, due_payment, room_package_id, user_id, roomNo):
        if due_payment is None or due_payment == '':
            print("ERROR: due amount field can't be Null\n")
            return False
        if room_package_id is None or room_package_id == '':
            print("ERROR: room_package_id can't be Null\n")
            return False
        if user_id is None or user_id == '':
            print("ERROR: user_id can't be Null\n")
            return False
        if roomNo is None or roomNo == '':
            print("ERROR: room number can't be Null\n")
            return False
        if due_payment <= 0 or roomNo <= 0:
            print("ERROR: payment can't be less than 0")
            return False
        rowcount = db_controller.dbcont_obj.gen_invoice(due_payment, room_package_id, user_id,roomNo)
        if rowcount <= 0:
            print("ERROR: something went wrong\n")
            return False
        else:
            return True

    def checkout(self, roomno):
        return self.RM.checkout(roomno)

    def get_tenant_record(self):
        return db_controller.dbcont_obj.get_tenant_record()

    def get_all_due_payments(self):
        return db_controller.dbcont_obj.get_all_due_payments()

# -----necessary  objects / variables-------
#object for hostel class
hostel_detail = db_controller.dbcont_obj.get_hostel_details(1)
hostel = Hostel(hostel_detail[0][1], hostel_detail[0][2], hostel_detail[0][3])

bookedRoom=0
bookedRoomPrice=0
bookedPackage=0
totalPrice=0
room_package_id=0
package_list=[]
room_list=[]
userid=0
availRooms=[]

#route to login.html page
#NOTE: if you want to change function name, then also change in template.html file

@app.route("/")
def landingPage():
    return render_template('landingPage.html')

@app.route("/managerServices")
def managerServices():
    return render_template('managerServices.html')

@app.route("/userServices")
def userServices():
    return render_template('userServices.html')

@app.route("/userLogin",methods=['GET','POST'])
def userLogin():
    if request.method == 'POST':
        users=hostel.get_all_users()
        for user in users:
            print(user[1],"  ",user[2]) 
            if request.form['userUsername']==user[1] and request.form['userPassword']==str(user[2]):
                global userid
                userid=user[0]
                return render_template("userServices.html")
                # return redirect(url_for('userHome'))
        return render_template('userLogin.html',loginMessage="Invalid Login")
    return render_template('userLogin.html',loginMessage="NULL")

@app.route('/managerLogin',methods=['GET','POST'])
def managerLogin():
    if request.method == 'POST':
        if request.form['employeeUsername']=="manager" and request.form['employeePassword']=="manager123":
            return redirect(url_for('managerServices'))
        return render_template('managerLogin.html', loginMessage = "ERROR: Invalid Login")
    return render_template('managerLogin.html',loginMessage="NULL")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/searchroom")
def searchroom():
    global availRooms 
    availRooms = hostel.get_rooms()
    return render_template("searchRoom_new.html", availRooms=availRooms)

@app.route("/duePayment",methods=['GET', 'POST'])
def duePayment():
    print(hostel.get_all_due_payments())
    return render_template("duePayment.html",payments=hostel.get_all_due_payments()) 

@app.route("/cancelBooking",methods=['GET', 'POST'])
def cancelbooking():
    if request.method == 'POST':
        if hostel.cancel_booking(request.form['userId'],request.form['roomPkgId']):
            return render_template("cancelBooking.html", error="Booking Cancelled Successfully")
        else:
            return render_template("cancelBooking.html", error="Cancellation Failed")
    iscancelled = True
    return render_template("cancelBooking.html", iscancelled=iscancelled)


@app.route("/allcustomerdetails")
def allcustomerdetails():
    all_details = hostel.search_customer()
    print(all_details)
    return render_template("customerDetail.html", all_details=all_details)

@app.route("/singlecustomerdetail",methods=['GET', 'POST'])
def singlecustomerdetail():
    if request.method == 'POST':
        if request.form.get("allcustomerdetails"):
            #do something
            cust_id = 0
            details = hostel.get_details(cust_id)
            return render_template("singleCustomerDetail.html", details=details)


@app.route("/roomSelection",methods=['GET', 'POST'])
def roomSelection():

    if request.method == 'POST':
        if request.form.get("selectRoom"):
            global bookedRoom, bookedRoomPrice, availRooms
            bookedRoom=request.form["selectedRoom"]
            for room in availRooms:
                if int(room[0])==int(bookedRoom):
                    bookedRoomPrice=room[2]
            global package_list
            package_list = hostel.search_packages_by_roomNo(bookedRoom)
            print(package_list)
            return render_template("searchPackages_new.html", roomNo=bookedRoom, roomPrice=bookedRoomPrice, packages=package_list)

@app.route("/bookingConfirmation", methods=['GET','POST'])
def bookingConfirmation():
    if request.method == 'POST':
        if request.form.get("selectPackage"):
            
            global bookedRoom
            global bookedRoomPrice
            global totalPrice
            global package_list
            global room_package_id
            global userid
            for packages in package_list:
                if int(packages[0])==int(request.form["selectedPackage"]) and int(packages[1])==int(bookedRoom):
                    totalPrice=int(packages[2])+int(bookedRoomPrice)
                    room_package_id=packages[4]
            print(int(totalPrice), int(room_package_id), int(userid))
            ret = hostel.gen_invoice(int(totalPrice), int(room_package_id), int(userid),int(bookedRoom))
            if ret:
                return render_template("bookingConfirmation.html", bookedRoom=bookedRoom, bookedPackage=request.form["selectedPackage"],totalPrice=totalPrice)
            else:
                return render_template("bookingConfirmation.html", error="ERROR: Invalid value!")

userId_manager=0
room_package_id_manager=0
due_payment=0
payed_amount=0

@app.route("/payment", methods=['GET','POST'])
def payment():
    if request.method == 'POST':
        global due_payment
        global userId_manager 
        global room_package_id_manager
        # userId_manager=request.form["userId"]
        # room_package_id_manager=request.form["R_P_ID"]
        duePayment = 0
        duePayment = hostel.get_due_payment(request.form["userId"], request.form["R_P_ID"])
        if duePayment is None:
            return render_template("payment.html", error = "ERROR: due payment cannot be empty!")
        return render_template("payment.html", duePayment=duePayment[0][1])
    return render_template("payment.html", error = "NULL")

@app.route("/checkout", methods=['GET','POST'])
def checkout():
    if request.method == 'POST':
        ret = hostel.checkout(request.form["roomId_checkout"])
        if ret is None or not ret:
            return render_template("checkout.html", error="Check Out Failed") 
        else:
            return render_template("checkout.html", success='checkout successful!') 
    return render_template("checkout.html", error='NULL')

@app.route("/AmountEnteredMsg", methods=['GET','POST'])
def AmountEnteredMsg():
    if request.method == 'POST':
        global userId_manager
        global room_package_id_manager
        global due_payment
        entered_amount = int(request.form["enteredAmount"])
        ret = hostel.pay_amount(int(userId_manager), int(room_package_id_manager), int(due_payment), entered_amount)
        if ret is None or not ret:
            return render_template("AmountEnteredMsg.html", amount=entered_amount)
        else:
            return render_template("AmountEnteredMsg.html", error="ERROR: Invalid amount entered!")

@app.route("/updateRoomPrice",methods=['GET','POST'])
def updateRoomPrice():
    if request.method=='POST':
        roomID=request.form["roomId"]
        newPrice=request.form["newPrice"]
        if hostel.update_room_price(roomID, newPrice) == True:
            return render_template("updateRoomPrice.html", success="Room price updated!")
        else:
            return render_template("updateRoomPrice.html", error="ERROR: Invalid entry!")
    else:
        return render_template("updateRoomPrice.html")

@app.route("/updatePackagePrice",methods=['GET','POST'])
def updatePackagePrice():
    if request.method=='POST':
        packageID=request.form["packageId"]
        newPrice=request.form["newPrice"]
        if hostel.update_package_price(packageID, newPrice) == True:
            return render_template("updatePackagePrice.html", success="Package price updated!")
        else:
            return render_template("updatePackagePrice.html", error="Invalid entry!")
    return render_template("updatePackagePrice.html")

@app.route("/tenantRecord", methods=['GET','POST'])
def tenantHistory():
    return render_template("tenantRecord_new.html",tenantRecord=hostel.get_tenant_record())
    
if __name__ == "__main__":
    app.run(debug=True)
