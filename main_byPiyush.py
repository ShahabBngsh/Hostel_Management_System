from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
from decimal import *
import credentials  # importing our credentials from credentials.py


import db_controller
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
        return self.room_list

    def checkout(self, roomno):
        db_controller.dbcont_obj.checkout(roomno)

    def update_room(self, room_id):
        pass
        #update in db


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

    def update_package(self, package_id):
        pass
        #update in db
    


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
        # pass
        return db_controller.dbcont_obj.cancel_booking(user_id,room_pkg_id)

    def check_due_payments(self, user_id, room_pkg_id):
        return db_controller.dbcont_obj.get_due_payment(user_id, room_pkg_id)[0][1]
        # pass
        # return DB.check_due_payments()

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

    def owner_check_due_payments(self):
        return self.IM.owner_check_due_payments()

    def check_customer_room_package(self, user_id, room_pkg_id):
        return self.RPM.check_customer_room_package(user_id, room_pkg_id)

    def update_room(self, room_id):
        return self.RM.update_room(room_id)

    def update_package(self, package_id):
        return self.PM.update_package(package_id)

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
        self.invoice_list.append(Invoice(due_amount, payment))
        if payment >= due_amount:
            ret_val = db_controller.dbcont_obj.pay_amount(user_id, room_package_id, due_amount, due_amount)
            if (ret_val):
                return (payment - due_amount)
            else:
                return -1
        else:
            ret_val = db_controller.dbcont_obj.pay_amount(user_id, room_package_id, due_amount, payment)
            if (ret_val):
                return (payment - due_amount)
            else:
                return -1

    def credit_payment(self, card_no, expiration_date, amount, merchant_id):
        if (self.charge(card_no, expiration_date, amount, merchant_id) != -1):
            self.invoice_list.append(invoice(amount, amount))
            # if (DB.payment(self.invoice_list[-1]) ):
            #     return (payment - charges)
            # else:
            #     return -1
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

    def gen_invoice(self, due_payment, room_package_id, user_id,roomNo):
        return db_controller.dbcont_obj.gen_invoice(due_payment, room_package_id, user_id,roomNo)
 
    def checkout(self, roomno):
        return self.RM.checkout(roomno)

    def owner_check_due_payments(self):
        pass
        #return db list of to pay invoices

# -----necessary  objects / variables-------
#object for hostel class
hostel_detail = db_controller.dbcont_obj.get_hostel_details(1)
hostel = Hostel(hostel_detail[0][1], hostel_detail[0][2], hostel_detail[0][3])

bookedRoom=0
bookedPackage=0
totalPrice=0
room_package_id=0
package_list=[]
userid=0

#route to login.html page
#NOTE: if you want to change function name, then also change in template.html file

@app.route("/login",methods=['GET','POST'])
@app.route("/",methods=['GET','POST'])
def login():
    if request.method == 'POST':
        users=hostel.get_all_users()
        for user in users:
            print(user[1],"  ",user[2]) 
            if request.form['userUsername']==user[1] and request.form['userPassword']==str(user[2]):
                global userid
                userid=user[0]
                return render_template("userHome.html")
                # return redirect(url_for('userHome'))
        return render_template('login.html',loginMessage="Invalid Login")
    return render_template('login.html',loginMessage="NULL")

@app.route('/managerLogin',methods=['GET','POST'])
def managerLogin():
    if request.method == 'POST':
        if request.form['employeeUsername']=="manager" and request.form['employeePassword']=="manager123":
            return redirect(url_for('managerHome'))
        return render_template('managerLogin.html',loginMessage="Invalid Login")
    return render_template('managerLogin.html',loginMessage="NULL")

@app.route("/managerHome")
def managerHome():
    return render_template("managerHome.html")


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

@app.route("/duePayment",methods=['GET', 'POST'])
def duePayment():
    if request.method == 'POST':
        return render_template("duePayment.html",duePayment=hostel.check_due_payments(request.form['userId'],request.form['roomPkgId']))
    return render_template("duePayment.html", duePayment=0)

@app.route("/cancelBooking",methods=['GET', 'POST'])
def cancelbooking():
    if request.method == 'POST':
        if hostel.cancel_booking(request.form['userId'],request.form['roomPkgId']):
            print("Here")
            return render_template("cancelBooking.html",bookingCancelMessage="Booking Canceled")
        else:
            return render_template("cancelBooking.html",bookingCancelMessage="Request Denied")
    iscancelled = True #hostel.cancel_roomm()
    return render_template("cancelBooking.html", iscancelled=iscancelled)


@app.route("/allcustomerdetails")
def allcustomerdetails():
    all_details = hostel.search_customer()
    print(all_details)
    return render_template("allcustomerdetails.html", all_details=all_details)

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
            global bookedRoom
            bookedRoom=request.form["RoomNo"]
            global package_list
            package_list = hostel.search_packages_by_roomNo(bookedRoom)

            # print(request.form["RoomNo"])
            #packages=getPackages(RoomNo)
            print(package_list)
            return render_template("searchPackages.html",roomNo=bookedRoom, packages=package_list)#, packages=packages

@app.route("/bookingConfirmation", methods=['GET','POST'])
def bookingConfirmation():
    if request.method == 'POST':
        if request.form.get("selectPackage"):
            global bookedRoom
            global totalPrice
            global package_list
            global room_package_id
            global userid
            for packages in package_list:
                if int(packages[3])==int(request.form["packageNo"]) and int(packages[2])==int(bookedRoom):
                    totalPrice=packages[0]
                    room_package_id=packages[1]
            print(int(totalPrice), int(room_package_id), int(userid))
            hostel.gen_invoice(int(totalPrice), int(room_package_id), int(userid),int(bookedRoom))
            # print("usama")
            return render_template("bookingConfirmation.html", bookedRoom=bookedRoom, bookedPackage=request.form["packageNo"],totalPrice=totalPrice)#, packages=packages

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
        userId_manager=request.form["userId"]
        room_package_id_manager=request.form["R_P_ID"]
        duePayment=0
        # duePayment=hostel.get_due_payment(userid, room_package_id)
        duePayment=hostel.get_due_payment(request.form["userId"],request.form["R_P_ID"])
        due_payment=duePayment[0][1]
        return render_template("payment.html",duePayment=duePayment[0][1])
    return render_template("payment.html")

@app.route("/checkout", methods=['GET','POST'])
def checkout():
    if request.method == 'POST':
        hostel.checkout(request.form["roomId_checkout"])
        checkoutMessage="Checked Out Successfully"
        return render_template("checkout.html", checkoutMessage=checkoutMessage)        
    return render_template("checkout.html")

@app.route("/AmountEnteredMsg", methods=['GET','POST'])
def AmountEnteredMsg():
    if request.method == 'POST':
        global userId_manager
        global room_package_id_manager
        global due_payment
        # print(int(userId_manager), int(room_package_id_manager), int(due_payment), int(request.form["enteredAmount"]))
        hostel.pay_amount(int(userId_manager), int(room_package_id_manager), int(due_payment), int(request.form["enteredAmount"]))
        return render_template("AmountEnteredMsg.html",amount=request.form["enteredAmount"])
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
