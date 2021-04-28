from authorizenet import apicontractsv1
from authorizenet.apicontrollers import *
# from decimal import *
import credentials  # importing our credentials from credentials.py


import db_controller

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
        self.room_list, error = db_controller.dbcont_obj.get_rooms()
        return self.room_list, error

    def checkout(self, roomno):
        db_controller.dbcont_obj.checkout(roomno)


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
        self.package_list, error = db_controller.dbcont_obj.search_packages_for_roomNo(room_no)
        return self.package_list, error


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
        self.IM = Invoice_manager()

    def reserve_room_and_package(self, room, package):
        return self.RPM.reserve_room_and_package(room, package)

    def get_rooms(self):
        return self.RM.get_rooms()

    def search_packages(self):
        return self.PM.search_packages()

    def search_packages_by_roomNo(self, roomNo):
        return self.PM.search_packages_by_roomNo(roomNo)

    def credit_payment(self, card_no, expiration_date, amount, merchant_id = 1):
        return self.IM.credit_payment(card_no, expiration_date, amount, merchant_id)

    def checkout(self, roomno):
        return self.RM.checkout(roomno)

    def gen_invoice(self, due_payment, room_package_id, user_id,roomNo):
        return self.IM.gen_invoice(due_payment, room_package_id, user_id,roomNo)
    
    def get_all_users(self):
        return db_controller.dbcont_obj.get_all_users()

    def get_user(self, user_id):
      return db_controller.dbcont_obj.get_user(user_id)

    def register_user(self, name, password, cnic=None, contact_no=None):
      return db_controller.dbcont_obj.register_user(name, password, cnic, contact_no)

    def get_due_payment(self, userid, room_package_id):
        return self.IM.get_due_payment(userid, room_package_id)
    
    def pay_cash(self, user_id, room_package_id, due_amount, payment):
        return self.IM.cash_payment(user_id, room_package_id, due_amount, payment)

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
        if due_amount>0 and payment>0:
            self.invoice_list.append(Invoice(due_amount, payment))
            if payment >= due_amount:
                ret_val = db_controller.dbcont_obj.pay_cash(user_id, room_package_id, due_amount, due_amount)
                if (ret_val):
                    return (payment - due_amount), "_SUCCESS"
                else:
                    return -1
            else:
                ret_val = db_controller.dbcont_obj.pay_cash(user_id, room_package_id, due_amount, payment)
                if (ret_val):
                    return (payment - due_amount), "_SUCCESS"
                else:
                    return -1
        else:
            return [], "_ERROR: 400" #bad request

    def credit_payment(self, card_no, expiration_date, amount, merchant_id):
        if (self.charge(card_no, expiration_date, amount, merchant_id) != -1):
            self.invoice_list.append(Invoice(amount, amount))
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
