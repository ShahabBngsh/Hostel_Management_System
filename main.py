# standard error codes
# _ERROR: 404           Not Found
# _ERROR: 400           Bad Request
# _SUCCESS              return success if DB is altered  but nothing to return

from flask import Flask, render_template, request, redirect, url_for, flash

from BL import (
    Users,
    Room, Room_manager,
    Package, Package_manager,
    Room_package, Room_package_manager,
    Hostel,
    Invoice, Invoice_manager,
    db_controller
)
app = Flask(__name__)
app.secret_key = '\xd6\xf0\xed\xf1\xcf\x9d\x12\xac`\xb9\xeeZ\xd0_\xc0\xbf'


# -----necessary  objects / variables-------
#object for hostel class
hostel_detail, error = db_controller.dbcont_obj.get_hostel_details(1)
if error is None:
    hostel = Hostel(hostel_detail[1], hostel_detail[2], hostel_detail[3])
else:
    print(" --- ", error)
bookedRoom=0
bookedPackage=0
totalPrice=0
room_package_id=0
package_list=[]
userid=0

#route to login.html page
#NOTE: if you want to change function name, then also change in template.html file

@app.route("/login", methods=['GET', 'POST'])
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

@app.route('/', methods=['GET','POST'])
@app.route('/managerLogin', methods=['GET','POST'])
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

@app.route("/roomSelection",methods=['GET', 'POST'])
def roomSelection():
    if request.method == 'POST':
        if request.form.get("selectRoom"):
            global bookedRoom
            bookedRoom=request.form["RoomNo"]
            global package_list
            package_list = hostel.search_packages_by_roomNo(bookedRoom)
            print(package_list)
            return render_template("searchPackages.html", roomNo=bookedRoom, packages=package_list)

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
            return render_template("bookingConfirmation.html",
                                    bookedRoom=bookedRoom,
                                    bookedPackage=request.form["packageNo"],
                                    totalPrice=totalPrice)

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
        duePayment, error = hostel.get_due_payment(request.form["userId"], request.form["R_P_ID"])
        if error is not None:
            flash(error)
        else:
            due_payment=duePayment[0]
            return render_template("payment.html", duePayment=duePayment[0])
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
        hostel.pay_cash(int(userId_manager), int(room_package_id_manager), int(due_payment), int(request.form["enteredAmount"]))
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
