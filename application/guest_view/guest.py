from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app

import json
# from application.forms import LoginForm
from application.database.user.user_db import *
from application.database.user.user_db import db,Guests,User,Booking,Rooms,Payment,Reservation,Refund,Budget,Income,Expenses,Attendance,Iteman,Family,Category,Unit,Stock,Store,StockTransfer,Department,Vendor,PurchaseOrder,PurchaseRequest,ReceivedItem,returnRequest,GOP,RoomType,Session,Wifi,Order,StockUsage,PosPayment,OrderItem,HeldCart,FoodChef,EventPayment,StockTransferOut,Cart,CanceldOrder,Customer,Credit,AccountGroup
from application.database.user.user_db import Account
from sqlalchemy import or_,desc,and_
from datetime import datetime
from datetime import date
from flask import session
from flask import jsonify, request
import json
from flask_praetorian import auth_required, current_user


from collections import Counter

guest = Blueprint("guest", __name__)

class OrderSchema(ma.Schema):
    class Meta:
        fields=("id","user_id","item_name","items","total","created_at","company_name","created_at","total","waiter","order_status","order_id","waiter","status",
                "quantity","onetime","table","discount","customer")








order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
        
class Guest_schema(ma.Schema):
    class Meta:
        fields=("id","first_name","last_name","cart_id","operation","cocktail_setup","unit","family","open_by","department","price","address","has_checkout","checkout_date","arrival","city","country","id_type","id_number","id_upload","dob","gender","work","remark","phone","customer_id",
                "region","email","username","arrival_date","checkout_date","guest_id","note","amount","created_date","date","type","attendace","name","description","store","quantity","hod","requested_by","item","approved_by","attendant","coupon_value","coupon_applied",
                "total_cost","unit_price","store","status","Department","attendance","time_in","time_out","position","reason","voided","item_id","request_by","user","method","subcategory","whole_price",
                    "close_by","open_date","lastname","firstname","close_date","wifi_code","order_id","waiter","food","cashier","is_vip","balance","customer_name","customer_phone","received_by","start_time","end_time",  "category","expired_date","batch_number","discount","customer")






class Refund_Schema(ma.Schema):
    class Meta:
        fields=("id","reason","refund_amount","payment_id","name","refund_time","status","authorized_by","session")


        
        
class PaySchema(ma.Schema):
    class Meta:
        fields=("id","name","amount","food","name","balance","method","children","adult","wifi_code","payment","checkin_date","checkout_date","room_type","discount","status","payment_date","guest_id","booking_id","session","code","attendant","cashier","dscount","customer")

class ReserveSchema(ma.Schema):
    class Meta:
        fields=("id","name","price","status","room_number","room_type","payment_status","arrival","departure","payment_date",
                "adult","children","purpose","departure","room_nmber","created_date","Payment_status","country","email","phone")

refund_schema = Refund_Schema(many=True)
guest_schema = Guest_schema(many=True)
guest_single_schema = Guest_schema()
pay_schema = PaySchema(many=True)

reserve_schema =ReserveSchema(many=True)





@guest.route("/add_guest",methods=["POST"])
@flask_praetorian.auth_required

def add_guest():
        us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
        try:
             username= request.json["username"]
        except:
            username=""
        
        try:
             email= request.json["email"]
        
        except:
            email =""
        try:
            password= request.json["password"]
        except:
            password=""
        hashed_password= guard.hash_password(password)
        try:
             first_name= request.json["first_name"]
        except:
            first_name=""
        try:
             last_name= request.json["last_name"]

        except:
            last_name=""
        try:
            country= request.json["country"]
        except:
            country=""
        try:
             address= request.json["address"]

        except:
            address =""
        
        try:
             city = request.json["city"]

        except:
            city=""

        try:    
        
            phone = request.json["phone"]

        except:
            phon=""
       
        owner =Guests(   
        username= request.json["username"],
        email= request.json["email"],
        password= request.json["password"],
       
        dob= request.json["dob"],
        country= request.json["country"],
        arrival_date = request.json["arrival_date"],
        # photo = request.json["photo"],
        # id_type = request.json["id_type"],
        # id_upload= request.json["id_upload"],



        # id_number= request.json["id_number"],
        checkout_date= request.json["checkout_date"],
        remark= request.json["remark"],
        work= request.json["work"],
        city = request.json["city"],
        gender = request.json["gender"],
        phone = request.json["phone"],
        address= request.json["address"],
        first_name= request.json["first_name"],
        last_name= request.json["last_name"],
        region= request.json["region"],


                      created_by_id =  flask_praetorian.current_user().id
      
        )
        user =User(
                   created_date=datetime.now(),  firstname= first_name, lastname=last_name,
        country= country,address= address,
        city = city,  phone = phone)
        db.session.add(user)
        db.session.commit()
        db.session.add(owner)
        db.session.commit()
        db.session.close()
     
  
        # db.session.close()
        resp = jsonify("success")
        resp.status_code=200
        return resp


@guest.route("/get_all_guest",methods=["GET"])
@flask_praetorian.auth_required
def get_all_guest():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    guests = Guests.query.all()
    results = guest_schema.dump(guests)

    return jsonify(results)



@guest.route("/add_expense",methods=['POST'])
@flask_praetorian.auth_required
def add_expense():
    # us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    session = Session.query.filter_by(status="current").first()
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    amount =request.json["amount"]
    note= request.json["note"]
    date =request.json["date"]
    subcategory =request.json["subcategory"]
    usr = user.firstname +" " + user.lastname
    created_date=datetime.now()
    exp = Expenses(name=name,amount=amount,note=note,date=date,
                   user=usr,created_by_id=flask_praetorian.current_user().id ,subcategory=subcategory,
                   created_date=created_date,company_name=user.company_name,session=session.open_date)
  
    db.session.add(exp)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_expense_list",methods=['GET'])
@flask_praetorian.auth_required
def get_expense_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    exp = Expenses.query.filter_by(company_name=user.company_name)
    result = guest_schema.dump(exp)
    return jsonify(result)



@guest.route("/get_expense/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_expense(id):

    exp = Expenses.query.filter_by(id=id)
    result = guest_schema.dump(exp)
    return jsonify(result)




@guest.route("/update_expense",methods=['PUT'])
@flask_praetorian.auth_required
def update_expense():
    id = request.json["id"]
    sub_data = Expenses.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.amount =request.json["amount"]
    sub_data.note = request.json["note"]
    sub_data.date =request.json["date"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@guest.route("/confirm_order", methods=['PUT'])
@flask_praetorian.auth_required
def confirm_order():
    user = flask_praetorian.current_user()
    order_id = request.json.get("id")
    
    if not order_id:
        return jsonify({"error": "Order ID is required"}), 400

    # Fetch the held cart by its ID
    sub_data = HeldCart.query.filter_by(id=order_id).first()

    if not sub_data:
        return jsonify({"error": "Order not found"}), 404

    # Update the order status to 'Confirmed'
    sub_data.status = "Confirmed"
    sub_data.confirmed_by = request.json.get("confirmed_by")
    
    # Process the items and set their confirmation status
    try:
        items = json.loads(sub_data.items)
        
        for item in items:
            if item.get("family") == "digital_printing" and "digital_printing" in user.roles:
                item["confirmed"] = True  # Set the digital printing item as confirmed
            elif item.get("family") == "dtf" and "dtf"  in user.roles:
                item["confirmed"] = True  # Set the food item as confirmed
            elif item.get("family") == "large_format" and "large_format"  in user.roles:
                item["confirmed"] = True  # Set the large_format item as confirmed

            elif item.get("family") == "label" and "label"  in user.roles:
                item["confirmed"] = True  # Set the label item as confirmed 
        
        # Update the items back to the order
        sub_data.items = json.dumps(items)

    except (json.JSONDecodeError, TypeError) as e:
        return jsonify({"error": f"Error updating items: {e}"}), 400

    # Update other confirmation fields
        # if "bartender" in user.roles:
        #     sub_data.contain_drink = "no"
        #     sub_data.drink_confirm_at =  datetime.now()
        #     sub_data.drink_confirm = f"{user.firstname} {user.lastname}"
        # else:
        #     sub_data.contain_food = "no"
        #     sub_data.food_confirm_at= datetime.now()
        #     sub_data.food_confirm = f"{user.firstname} {user.lastname}"

    # Commit the changes to the database
    db.session.commit()

    # Return a success response
    return jsonify({"message": "Order confirmed successfully"}), 200


@guest.route("/confirm_oder_two", methods=['PUT'])
@flask_praetorian.auth_required
def confirm_oder_two():
    user = flask_praetorian.current_user()
    order_item_id = request.json.get("id")
    
    if not order_item_id:
        return jsonify({"error": "Order Item ID is required"}), 400

    # Fetch the order item by its ID
    sub_data = OrderItem.query.filter_by(id=order_item_id).first()

    if not sub_data:
        return jsonify({"error": "Order item not found"}), 404

    # Update the order item status to 'Confirmed'
    sub_data.status = "Confirmed"
    
    # Process the items and set their confirmation status
   
    # Update other confirmation fields
    if "bartender" in user.roles:
        sub_data.contain_drink = "no"
        sub_data.drink_confirm = f"{user.firstname} {user.lastname}"
    else:
        sub_data.contain_food = "no"
        sub_data.food_confirm = f"{user.firstname} {user.lastname}"

    # Commit the changes to the database
    db.session.commit()

    # Return a success response
    return jsonify({"message": "Order item confirmed successfully"}), 200




@guest.route("/delete_expense/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_expense(id):
      sub_data = Expenses.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp






@guest.route("/guest_info/<id>",methods=["GET"])
@flask_praetorian.auth_required
def guest_info(id):
    guests = db.session.query(Guests).filter_by(id = id).all()
    results = guest_schema.dump(guests)

    return jsonify(results)








@guest.route("/update_guest",methods=["PUT"])
@flask_praetorian.auth_required

def update_guest():
        id = request.json["id"]
        guest = Guests.query.filter_by(id=id).first()
        guest.username= request.json["username"]
        guest.email= request.json["email"]
        password= request.json["password"]
        guest.hashed_password= guard.hash_password(password)
       
       
        guest.dob= request.json["dob"]
        guest.country= request.json["country"]
        guest.arrival_date = request.json["arrival_date"]
       


        
        guest.checkout_date= request.json["checkout_date"]
        guest.remark= request.json["remark"]
        guest.work= request.json["work"]
        guest.city = request.json["city"]
        guest.gender = request.json["gender"]
        guest.phone = request.json["phone"]
        guest.address= request.json["address"]
        guest.first_name= request.json["first_name"]
        guest.last_name= request.json["last_name"]
        guest.region= request.json["region"]


        # guest.created_by_id =  flask_praetorian.current_user().id
      

    
        db.session.commit()
        db.session.close()
        resp = jsonify("success")
        resp.status_code=200
        return resp



@guest.route("/delete_guest/<id>",methods=["DELETE"])
@flask_praetorian.auth_required
def delete_guest(id):
    gst = db.session.query(Guests).filter_by(id =id).first()
    usr =  db.session.query(User).filter_by(username =gst.username).first()
    db.session.delete(gst)
    # db.session.delete(usr)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code=200

    return resp


@guest.route("/fetch_guest/<id>",methods=["GET"])
def fetch_guest(id):
      gst = db.session.query(Guests).filter_by(id=id).all()
      results = guest_schema.dump(gst)
      return jsonify(results)




@guest.route("/add_booking",methods=["POST"])
@flask_praetorian.auth_required
def add_booking():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    session = Session.query.filter_by(status="current").first()
   
    room_number=request.json["room_number"]
    name=request.json["name"]
    guest_id = request.json["guest_id"]
    booking = Booking(name=request.json["name"],  room_type=request.json["room_type"],country=request.json["country"],session=session.open_date,
    
     purpose=request.json["purpose"],
      
     
     departure_date=request.json["departure_date"],
     
     arrival_date =request.json["arrival_date"],
     adult =request.json["adult"],
     children=request.json["children"],



     room_number=request.json["room_number"],
     has_checkout=False,
     
     status=request.json["status"],
     create_date=datetime.now(),
     created_by_id = flask_praetorian.current_user().id,guest_id=guest_id
    )
    room = Rooms.query.filter_by(room_number=room_number).first()
    guest = Guests.query.filter_by(id=guest_id).first()
    guest.room_number = room_number
    room.occupied_state="occupied"
    room.occupied_by=request.json["name"]
    db.session.add(booking)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code=200
    
    return resp



@guest.route("/add_payment", methods=["POST"])
@flask_praetorian.auth_required
def add_payment():
    # Extract data from the request
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    code=""
    session = Session.query.filter_by(status="current").first()
  
    amount = request.json.get("amount")
    room_number = request.json.get("room_number")
    name = request.json.get("name")
    status = request.json.get("status")
    booking_id = request.json.get("booking_id")
    days = request.json["days"]  # Use .get() to avoid KeyError
    
    # if not days:
    #     return jsonify({"error": "Missing 'days' in request"}), 400  # Return error if days is missing

    print("Days:", days)  # Confirm 'days' value is received

    # Query for an available WiFi code
    wifi_code = Wifi.query.filter_by(state="available", duration=days).order_by(func.random()).first()

    if wifi_code:
        code=wifi_code # Return 404 if no matching code is found
        wifi_code.state="used"

    
     # Serialize result
   

    # Create a new payment entry
    pay = Payment(
        name=name,
        wifi_code=code,
        amount=amount,
        refund_amount="0",
        balance=request.json.get("balance"),
        method=request.json.get("method"),
        room_type=request.json.get("room_type"),
        discount=request.json.get("discount"),
        children=request.json.get("children"),
        adult=request.json.get("adult"),
        guest_id=request.json.get("guest_id"),
        payment_date=datetime.now(),
        checkin_date=request.json.get("checkin_date"),
        checkout_date=request.json.get("checkout_date"),
        status=status,booking_id=booking_id,session=session.open_date,
        created_by_id=flask_praetorian.current_user().id)
    
    inc = Income(
            amount=amount,
            date=datetime.now().strftime('%Y-%m-%d'),
            note=request.json.get("room_type"),
            created_date=datetime.now(),cashier=us.firstname +" "+us.lastname,
            created_by_id=flask_praetorian.current_user().id
        )


    # Update room status
    room = Rooms.query.filter_by(room_number=room_number).first()
    if room:
        room.occupied_by = name
        room.occupied_state = "occupied"
        room.date_booked = datetime.now()

    # Commit the changes to the database
    try:
        db.session.add(pay)
        db.session.add(inc)
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

    # Get user details for the email
    usr = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    payment_date = datetime.now()

    # Beautify the email message
    email_message = f"""
    Hello Kevin,

    A new booking payment has been recorded in your Hotel Management System.

    **Payment Details:**
    - Guest Name: {name}
    - Payment Amount: ${amount}
    - Room Number: {room_number}
    - Room Type: {request.json.get("room_type")}
    - Discount Applied: ${request.json.get("discount")}
    - Balance: ${request.json.get("balance")}
    - Payment Method: {request.json.get("method")}
    - Check-in Date: {request.json.get("checkin_date")}
    - Check-out Date: {request.json.get("checkout_date")}
    - Payment Status: Success
    - Date|Time: {payment_date}

    **Issued By:**
    - {usr.firstname} {usr.lastname}

    Please log in to review this transaction.

    Best regards,  
    **Kevo Executive Hotel Team**
    """

    # Send the email
    msg = Message(
        subject="New Booking Payment - Kevo Executive Hotel",
        sender="jxkalmhefacbuk@gmail.com",
        recipients=["kevinfiadzeawu@gmail.com"]
    )
    msg.body = email_message
    # mail.send(msg)

    # Return a success response
    return jsonify("success"), 200


     
     

# query_list = db.session.query(Ads).filter(Ads.category=="electronics")
# #                  imb =  query_list.order_by(desc(Ads.post_on))

@guest.route("/get_payment",methods=["GET"])
@flask_praetorian.auth_required
def get_payment():
     us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
     pay = Payment.query.all()
    #  lst =  pay.order_by(desc(Payment.payment_date))
     result = pay_schema.dump(pay)
     return jsonify(result)


@guest.route("/get_payment_pos",methods=["GET"])
@flask_praetorian.auth_required
def get_payment_pos():
     us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
     pay = PosPayment.query.all()
    #  lst =  pay.order_by(desc(Payment.payment_date))
     result = pay_schema.dump(pay)
     return jsonify(result)



@guest.route("/current_payment", methods=["GET"])
@flask_praetorian.auth_required
def current_payment():
    try:
        # Get the current year
        current_year = datetime.now().year
        
        # Filter payments where the payment_date contains the current year
        payments = Payment.query.filter(Payment.payment_date.like(f"%{current_year}%")).order_by(Payment.payment_date.desc()).all()
        
        # Serialize the results
        result = pay_schema.dump(payments)
        
        return jsonify(result), 200
    except Exception as e:
        # Handle unexpected errors gracefully
        return jsonify({"error": str(e)}), 500






@guest.route("/get_return_request",methods=["GET"])
@flask_praetorian.auth_required
def get_return_request():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # date = request.json["date"]
    # print(date)
    refund = returnRequest.query.all()
    
    result = guest_schema.dump(refund)
    return jsonify(result)




@guest.route("/search_stock_usuage",methods=["POST"])
@flask_praetorian.auth_required
def search_stock_usuage():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    # print(date)
    refund = StockUsage.query.filter(StockUsage.created_date.contains(date) ,StockUsage.company_name.contains(us.company_name))
    lst = refund.order_by(desc(StockUsage.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)


@guest.route("/search_account_group",methods=["POST"])
@flask_praetorian.auth_required
def search_account_group():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    find = request.json["find"]
    # print(date)
    group = AccountGroup.query.filter(AccountGroup.subcategory.contains(find))
    result = guest_schema.dump(group)
    return jsonify(result)

@guest.route("/search_expense_group",methods=["POST"])
@flask_praetorian.auth_required
def search_expense_group():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    find = request.json["find"]
    # print(date)
    group = Expenses.query.filter(AccountGroup.subcategory.contains(find))
    result = guest_schema.dump(group)
    return jsonify(result)



@guest.route("/search_account",methods=["POST"])
@flask_praetorian.auth_required
def search_account():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    find = request.json["find"]
    # print(date)
    group = Account.query.filter_by(subcategory=find).all()
    result = guest_schema.dump(group)
    return jsonify(result)



@guest.route("/search_stock_usage_two",methods=["POST"])
@flask_praetorian.auth_required
def search_stock_usage_two():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    datetwo = request.json["datetwo"]
    # print(date)
    refund = StockUsage.query.filter(
        or_(StockUsage.created_date.contains(date) ,StockUsage.created_date.contains(datetwo) )
        ).filter(StockUsage.company_name.contains(us.company_name))
    lst = refund.order_by(desc(StockUsage.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)


@guest.route("/search_refund_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_refund_dates():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    # print(date)
    refund = Refund.query.filter(Refund.session.contains(date) ,Refund.company_name.contains(us.company_name))
    lst = refund.order_by(desc(Refund.session))
    result = refund_schema.dump(lst)
    return jsonify(result)


@guest.route("/search_return_date",methods=["POST"])
@flask_praetorian.auth_required
def search_return_date():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    # print(date)
    refund = returnRequest.query.filter(returnRequest.created_date.contains(date),returnRequest.status.contains("Success") ,
                                        returnRequest.company_name.contains(us.company_name))
    lst = refund.order_by(desc(returnRequest.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)




@guest.route("/search_return_date_two",methods=["POST"])
@flask_praetorian.auth_required
def search_return_date_two():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    datetwo = request.json["datetwo"]
    # print(date)
    refund = returnRequest.query.filter(
         
        or_(returnRequest.created_date.contains(date), returnRequest.created_date.contains(datetwo))
            ).filter( returnRequest.status.contains("Success") ,
                                        returnRequest.company_name.contains(us.company_name))
    lst = refund.order_by(desc(returnRequest.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)

    

@guest.route("/search_purchase_date",methods=["POST"])
@flask_praetorian.auth_required
def search_purchase_date():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    # print(date)
    refund = PurchaseRequest.query.filter(PurchaseRequest.created_date.contains(date),PurchaseRequest.company_name.contains(us.company_name) )
    lst = refund.order_by(desc(PurchaseRequest.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)





@guest.route("/search_order_date",methods=["POST"])
@flask_praetorian.auth_required
def search_order_date():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    # print(date)
    refund = PurchaseOrder.query.filter(PurchaseOrder.created_date.contains(date) ,PurchaseOrder.company_name.contains(us.company_name))
    lst = refund.order_by(desc(PurchaseOrder.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)






@guest.route("/search_order_dates_two",methods=["POST"])
@flask_praetorian.auth_required
def search_order_dates_two():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    datetwo = request.json["datetwo"]
    # print(date)
    refund = PurchaseOrder.query.filter(

        or_(

            PurchaseOrder.created_date.contains(date), PurchaseOrder.created_date.contains(datetwo)


        )

    ).filter( PurchaseOrder.company_name.contains(us.company_name))
    lst = refund.order_by(desc(PurchaseOrder.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)




@guest.route("/search_received_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_received_dates():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    # datetwo = request.json["datetwo"]
    # print(date)
    refund = ReceivedItem.query.filter(ReceivedItem.company_name.contains(us.company_name) )
    lst = refund.order_by(desc(ReceivedItem.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)






@guest.route("/search_recieve_date_two",methods=["POST"])
@flask_praetorian.auth_required
def search_recieve_date_two():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    date = request.json["datetwo"]
    # print(date)
    refund = ReceivedItem.query.filter(ReceivedItem.created_date.contains(date),ReceivedItem.company_name.contains(us.company_name) )
    lst = refund.order_by(desc(ReceivedItem.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)



@guest.route("/search_stock_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_stock_dates():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    # print(date)
    refund = Stock.query.filter(Stock.session.contains(date) ,Stock.company_name.contains(us.company_name))
    lst = refund.order_by(desc(Stock.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)




@guest.route("/search_stock_date_two", methods=["POST"])
@flask_praetorian.auth_required
def search_stock_date_two():
    current_user = flask_praetorian.current_user()
    us = User.query.filter_by(id=current_user.id).first()

    # Get dates from the request
    date = request.json.get("date")
    datetwo = request.json.get("datetwo")

    # Query matching created_date by date (not datetime) and company_name
    refund_query = Stock.query.filter(
        or_(
            func.date(Stock.session) == date,
            func.date(Stock.session) == datetwo
        ),
        Stock.company_name == us.company_name
    ).order_by(desc(Stock.created_date))

    result = guest_schema.dump(refund_query)
    return jsonify(result)

@guest.route("/searchdates",methods=["POST"])
@flask_praetorian.auth_required
def searchdates():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    # print(date)
    pay = Payment.query.filter(Payment.session.contains(date),Payment.company_name.contains(us.company_name) )
    lst = pay.order_by(desc(Payment.session))
    result = pay_schema.dump(lst)
    return jsonify(result)



@guest.route("/get_chef_dates",methods=["POST"])
@flask_praetorian.auth_required
def get_chef_dates():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    # print(date)
    pay = FoodChef.query.filter(FoodChef.created_date.contains(date),FoodChef.company_name.contains(us.company_name) )
    lst = pay.order_by(desc(FoodChef.created_date))
    result = pay_schema.dump(lst)
    return jsonify(result)


@guest.route("/search_event_date",methods=["POST"])
@flask_praetorian.auth_required
def search_event_date():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    # print(date)
    pay = EventPayment.query.filter(EventPayment.created_date.contains(date),EventPayment.company_name.contains(us.company_name) )
    lst = pay.order_by(desc(EventPayment.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)



@guest.route("/search_chef_dates_two",methods=["POST"])
@flask_praetorian.auth_required
def search_chef_dates_two():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    datetwo = request.json["datetwo"]
    # print(date)
    pay = FoodChef.query.filter(
         
        or_(FoodChef.created_date.contains(date), FoodChef.created_date.contains(datetwo)
            )).filter(FoodChef.created_date.contains(date),FoodChef.company_name.contains(us.company_name) )
    lst = pay.order_by(desc(FoodChef.created_date))
    result = pay_schema.dump(lst)
    return jsonify(result)


@guest.route("/search_event_dates_two",methods=["POST"])
@flask_praetorian.auth_required
def search_event_dates_two():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    datetwo = request.json["datetwo"]
    # print(date)
    pay = EventPayment.query.filter(
         
        or_(EventPayment.created_date.contains(date), EventPayment.created_date.contains(datetwo)
            )).filter(EventPayment.created_date.contains(date),EventPayment.company_name.contains(us.company_name) )
    lst = pay.order_by(desc(EventPayment.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)

@guest.route("/search_held_order_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_held_order_dates():
    us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    try:
        date = request.json.get("date")
        
        if not date:
            return jsonify({"error": "Date is required"}), 400

        # Query HeldCart for orders on the specified date
        held_orders = HeldCart.query.filter(
            db.func.date(HeldCart.created_at) == date,
            HeldCart.company_name == us.company_name
        ).all()
        
        result = []
        for order in held_orders:
            try:
                items = json.loads(order.items) if order.items else []
                
                # Get customer name safely
                customer_name = "Walk-in"
                if order.customer:
                    try:
                        customer_id = int(order.customer)
                        customer = Customer.query.filter_by(id=customer_id).first()
                        if customer:
                            customer_name = f"{customer.firstname} {customer.lastname}".strip() or "Walk-in"
                    except (ValueError, TypeError):
                        customer_name = order.customer
                
                result.append({
                    "id": order.id,
                    "items": items,
                    "total": float(order.total) if order.total else 0,
                    "balance": float(order.balance) if order.balance else 0,
                    "waiter": order.waiter or 'N/A',
                    "customer": order.customer,
                    "customer_name": customer_name,
                    "status": order.status,
                    "paid_status": order.paid_status,
                    "created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else None,
                    "note": order.note or '',
                    "contain_dtf": order.contain_dtf,
                    "contain_digital_printing": order.contain_digital_printing,
                    "contain_large_format": order.contain_large_format,
                    "contain_label": order.contain_label
                })
            except Exception as e:
                print(f"Error processing order {order.id}: {e}")
                continue
        
        return jsonify(result), 200

    except Exception as e:
        print(f"Error in search_held_order_dates: {str(e)}")
        return jsonify({"error": str(e)}), 500
from datetime import datetime, time

@guest.route("/search_held_order_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_held_order_dates_two():
    # Get the current user
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Get date range from request
    date = request.json.get("date")
    datetwo = request.json.get("date_two")
    if not date or not datetwo:
        return jsonify({"error": "Both date and datetwo are required"}), 400

    try:
        # Convert to datetime range covering full days
        start_date = datetime.combine(datetime.strptime(date, "%Y-%m-%d"), time.min)
        end_date = datetime.combine(datetime.strptime(datetwo, "%Y-%m-%d"), time.max)

        # Convert dates to string format for comparison with database
        start_date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
        end_date_str = end_date.strftime("%Y-%m-%d %H:%M:%S")

        # Query HeldCart with filtering - No delivery_status filter
        held_orders = HeldCart.query.filter(
            HeldCart.session >= start_date_str,
            HeldCart.session <= end_date_str,
            HeldCart.company_name == user.company_name,
            HeldCart.paid_status.in_(["Pending", "Partial"])
        ).order_by(desc(HeldCart.session)).all()

        # Prepare response with items
        result = []
        total_held_amount = 0
        
        for order in held_orders:
            try:
                # Parse items JSON
                order_items = json.loads(order.items) if order.items else []
                
                # Calculate total for this order
                order_total = 0
                for item in order_items:
                    if isinstance(item, dict):
                        qty = item.get('qty', 0)
                        price = item.get('price', 0)
                        order_total += qty * price
                
                total_held_amount += order_total
                
                # Add order with items
                result.append({
                    "id": order.id,
                    "items": order_items,
                    "waiter": order.waiter,
                    "status": order.paid_status,
                    "total": order.total,
                    "customer": order.customer,
                    
                    "session": order.session,
                    "balance":order.balance,
                    "company_name": order.company_name,
                    "created_at": order.created_at
                })
                
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON for order {order.id}: {e}")
                # Add order with empty items if JSON is invalid
                result.append({
                    "id": order.id,
                    "items": [],
                    "waiter": order.waiter,
                    "status": order.paid_status,
                    "total": order.total,
                    "customer": order.customer,
                    
                    "session": order.session,
                    "balance":order.balance,
                    "company_name": order.company_name,
                    "created_at": order.created_at
                })

        return jsonify({
            "HeldList": result,
            "totalHeldAmount": total_held_amount
        }), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return jsonify({"error": "An error occurred while fetching data"}), 500

@guest.route("/search_held_order_dates_food", methods=["POST"])
@flask_praetorian.auth_required
def search_held_order_dates_food():
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    date = request.json.get("date")
    if not date:
        return jsonify({"error": "Date is required"}), 400

    held_orders = HeldCart.query.filter(
        HeldCart.session.contains(date),
        HeldCart.company_name == user.company_name
    ).order_by(desc(HeldCart.created_at)).all()

    result = []
    for order in held_orders:
        try:
            items = json.loads(order.items)
        except json.JSONDecodeError:
            items = []

        # Check if the order has at least one item with family == "food"
        food_items = [item for item in items if item.get("family") == "food"]

        if food_items:
            result.append({
                "id": order.id,
                "company_name": order.company_name,
                "created_at": order.created_at,
                "status": order.status,
                "total": order.total,
                "waiter": order.waiter,
                "items": food_items,  # return only food items
                "food_confirm": order.food_confirm,
                "drink_confirm": order.drink_confirm
            })

    return jsonify(result), 200






@guest.route("/search_held_order_dates_drink", methods=["POST"])
@flask_praetorian.auth_required
def search_held_order_dates_drink():
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    date = request.json.get("date")
    if not date:
        return jsonify({"error": "Date is required"}), 400

    held_orders = HeldCart.query.filter(
        HeldCart.session.contains(date),
        HeldCart.company_name == user.company_name
    ).order_by(desc(HeldCart.created_at)).all()

    result = []
    for order in held_orders:
        try:
            items = json.loads(order.items)
        except json.JSONDecodeError:
            items = []

        # Check if the order has at least one item with family == "food"
        food_items = [item for item in items if item.get("family") == "drink"]

        if food_items:
            result.append({
                "id": order.id,
                "company_name": order.company_name,
                "created_at": order.created_at,
                "status": order.status,
                "total": order.total,
                "waiter": order.waiter,
                "items": food_items,  # return only food items
                "food_confirm": order.food_confirm,
                "drink_confirm": order.drink_confirm
            })

    return jsonify(result), 200




@guest.route("/searchdates_pos",methods=["POST"])
@flask_praetorian.auth_required
def searchdates_pos():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    # print(date)
    pay = PosPayment.query.filter(PosPayment.session.contains(date),PosPayment.company_name.contains(us.company_name) )
    lst = pay.order_by(desc(PosPayment.payment_date))
    result = pay_schema.dump(lst)
    return jsonify(result)


from datetime import datetime, time

@guest.route("/search_pos_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_pos_dates_two():
    us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    date = request.json.get("date")
    datetwo = request.json.get("datetwo")

    try:
        # Convert to datetime range covering full days
        start_date = datetime.combine(datetime.strptime(date, "%Y-%m-%d"), time.min)
        end_date = datetime.combine(datetime.strptime(datetwo, "%Y-%m-%d"), time.max)

        # Filter POS payments by date and company name
        pay = PosPayment.query.filter(
            PosPayment.session >= start_date,
            PosPayment.session <= end_date,
            PosPayment.company_name.contains(us.company_name)
        ).order_by(desc(PosPayment.payment_date))

        result = pay_schema.dump(pay)
        return jsonify(result), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return jsonify({"error": "An error occurred while fetching data"}), 500


@guest.route("/search_waiter_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_waiter_dates():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    waiter =request.json["waiter"]
    
    print(date)
    pay = PosPayment.query.filter(PosPayment.session.contains(date),PosPayment.attendant.contains(waiter),
                                  )
    lst = pay.order_by(desc(PosPayment.payment_date))
    result = pay_schema.dump(lst)
    return jsonify(result)

@guest.route("/search_method_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_method_dates():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    method =request.json["waiter"]
    
    # print(date)
    pay = PosPayment.query.filter(PosPayment.session.contains(date),PosPayment.method.contains(method),
                                  )
    lst = pay.order_by(desc(PosPayment.payment_date))
    result = pay_schema.dump(lst)
    return jsonify(result)

@guest.route("/search_department_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_department_dates():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    category =request.json["waiter"]
    
    # print(date)
    pay = Income.query.filter(Income.session.contains(date),Income.category.contains(request.json["waiter"]),
                                  )
    lst = pay.order_by(desc(Income.date))
    result = guest_schema.dump(lst)
    return jsonify(result)







@guest.route("/search_cashier_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_cashier_dates():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    cashier =request.json["waiter"]
    
    # print(date)
    pay = Income.query.filter(Income.session.contains(date),Income.cashier.contains(cashier),
                                  )
    lst = pay.order_by(desc(Income.date))
    result = guest_schema.dump(lst)
    return jsonify(result)


from datetime import datetime, time

@guest.route("/search_waiter_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_waiter_dates_two():
    us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    date = request.json["date"]
    datetwo = request.json["datetwo"]
    waiter = request.json["waiter"]

    try:
        # Convert to full datetime range
        start_date = datetime.combine(datetime.strptime(date, "%Y-%m-%d"), time.min)
        end_date = datetime.combine(datetime.strptime(datetwo, "%Y-%m-%d"), time.max)

        pay = Income.query.filter(
            Income.session >= start_date,
            Income.session <= end_date,
            Income.attendant.contains(waiter)
        ).order_by(desc(Income.date))

        result = guest_schema.dump(pay)
        return jsonify(result), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return jsonify({"error": "An error occurred while fetching data"}), 500


@guest.route("/search_attendant_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_attendant_dates_two():
    us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    date = request.json["date"]
    datetwo = request.json["datetwo"]
    waiter = request.json["waiter"]

    try:
        # Convert to full datetime range
        start_date = datetime.combine(datetime.strptime(date, "%Y-%m-%d"), time.min)
        end_date = datetime.combine(datetime.strptime(datetwo, "%Y-%m-%d"), time.max)

        pay = CanceldOrder.query.filter(
            CanceldOrder.session >= start_date,
            CanceldOrder.session <= end_date,
            CanceldOrder.company_name.contains(us.company_name),
            CanceldOrder.attendant.contains(waiter)
        ).order_by(desc(CanceldOrder.date))

        result = guest_schema.dump(pay)
        return jsonify(result), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return jsonify({"error": "An error occurred while fetching data"}), 500 



from datetime import datetime, time

@guest.route("/search_method_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_method_dates_two():
    us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    date = request.json["date"]
    datetwo = request.json["datetwo"]
    method = request.json["waiter"]

    try:
        # Convert to full datetime range
        start_date = datetime.combine(datetime.strptime(date, "%Y-%m-%d"), time.min)
        end_date = datetime.combine(datetime.strptime(datetwo, "%Y-%m-%d"), time.max)

        pay = Income.query.filter(
            Income.session >= start_date,
            Income.session <= end_date,
            Income.method.contains(method)
        ).order_by(desc(Income.date))

        result = guest_schema.dump(pay)
        return jsonify(result), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return jsonify({"error": "An error occurred while fetching data"}), 500





@guest.route("/search_department_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_department_dates_two():
    us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    date = request.json["date"]
    datetwo = request.json["datetwo"]
    category = request.json["waiter"]

    try:
        # Convert to full datetime range
        start_date = datetime.combine(datetime.strptime(date, "%Y-%m-%d"), time.min)
        end_date = datetime.combine(datetime.strptime(datetwo, "%Y-%m-%d"), time.max)

        pay = Income.query.filter(
            Income.session >= start_date,
            Income.session <= end_date,
            Income.category.contains(request.json["waiter"])
        ).order_by(desc(Income.date))

        result = guest_schema.dump(pay)
        return jsonify(result), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return jsonify({"error": "An error occurred while fetching data"}), 500







@guest.route("/search_category_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_category_dates_two():
    us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    date = request.json["date"]
    datetwo = request.json["datetwo"]
    category = request.json["waiter"]

    try:
        # Convert to full datetime range
        start_date = datetime.combine(datetime.strptime(date, "%Y-%m-%d"), time.min)
        end_date = datetime.combine(datetime.strptime(datetwo, "%Y-%m-%d"), time.max)

        pay = Income.query.filter(
            Income.session >= start_date,
            Income.session <= end_date,
            Income.cat.contains(request.json["waiter"])
        ).order_by(desc(Income.date))

        result = guest_schema.dump(pay)
        return jsonify(result), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return jsonify({"error": "An error occurred while fetching data"}), 500



from datetime import datetime, time


@guest.route("/search_cashier_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_cashier_dates_two():
    us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    date = request.json.get("date")
    datetwo = request.json.get("datetwo")
    cashier = request.json.get("waiter")  # still using "waiter" key to mean cashier?

    try:
        # Convert date strings to datetime range (covering full day)
        start_date = datetime.combine(datetime.strptime(date, "%Y-%m-%d"), time.min)
        end_date = datetime.combine(datetime.strptime(datetwo, "%Y-%m-%d"), time.max)

        # Perform the query
        pay = Income.query.filter(
            Income.session >= start_date,
            Income.session <= end_date,
            Income.cashier.contains(cashier)
        ).order_by(desc(Income.date))

        result = pay_schema.dump(pay)
        return jsonify(result), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return jsonify({"error": "An error occurred while fetching data"}), 500







from sqlalchemy import Integer, or_

@guest.route("/search_payment_date_two", methods=["POST"])
@flask_praetorian.auth_required
def search_payment_date_two():
    us = User.query.filter_by(id=flask_praetorian.current_user().id).first()

    date = request.json.get("date")
    date_two = request.json.get("date_two")

    if not date:
        return jsonify({"error": "Date is required"}), 400

    payments = Payment.query.filter(
        or_(
            Payment.session.contains(date),
            Payment.session.contains(date_two)
        )
    ).filter(
        Payment.balance.cast(Integer) > 0
    ).filter(
        Payment.session != None
    ).filter(
        Payment.company_name.contains(us.company_name)
    ).order_by(
        Payment.session.desc()
    )

    result = pay_schema.dump(payments)

    return jsonify(result)


from sqlalchemy import Integer

@guest.route("/search_payment_date", methods=["POST"])
@flask_praetorian.auth_required
def search_payment_date():
    us = User.query.filter_by(id=flask_praetorian.current_user().id).first()

    date = request.json.get("date")

    if not date:
        return jsonify({"error": "Date is required"}), 400

    payments = Payment.query.filter(
        Payment.session.contains(date),
        Payment.company_name.contains(us.company_name),
        Payment.balance.cast(Integer) > 0   # ✅ FIXED
    ).order_by(
        Payment.session.desc()
    )

    result = pay_schema.dump(payments)

    return jsonify(result)



@guest.route("/search_payment_held_date", methods=["POST"])
@flask_praetorian.auth_required
def search_payment_held_date():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # Extract date from the request payload
    date = request.json.get("date")
    # date_two = request.json.get("datetwo")
    
    if not date:
        return jsonify({"error": "Date is required"}), 400
    
    # Query to find payments with balance greater than 0, and payment date containing the given date
    payments = HeldCart.query.filter(
        HeldCart.created_at.contains(date),HeldCart.company_name.contains(us.company_name),
        HeldCart.total.cast(int) > 0 ,HeldCart.status=="Pending"
    ).order_by(Payment.session.desc())

    # Serialize the payments data
    result = orders_schema.dump(payments)
    
    # Return the results as JSON
    return jsonify(result)






@guest.route("/get_payment_for/<id>",methods=["GET"])
@flask_praetorian.auth_required
def get_payment_for(id):
     
     pay = Payment.query.filter_by(id=id).all()
     result = pay_schema.dump(pay)
     return jsonify(result)


@guest.route("/filter_payment_day/<day>",methods=["GET"])
@flask_praetorian.auth_required
def filter_payment_day(day):
     result ="yes"
     if day =="daily":
         pay = Payment.query.filter(Payment.payment_day <= datetime.now()).all()
         result = pay_schema.dump(pay)
     return jsonify(result)






@guest.route("/update_payment", methods=["PUT"])
@flask_praetorian.auth_required
def update_payment():
    amount = request.json["amount"]
    id = request.json["id"]
    
    # Query the payment by ID
    pay = Payment.query.filter_by(id=id).first()

    # Update the amount by adding the new amount to the existing amount
    a= pay.amount = int(amount) + int(pay.amount)
    pay.amount =a
    pay.method = request.json["method"]
    pay.room_type = request.json["room_type"]
    pay.discount = request.json["discount"]
    pay.children = request.json["children"]
    pay.adult = request.json["adult"]
    pay.checkin_date = request.json["checkin_date"]
    pay.checkout_date = request.json["checkout_date"]
    pay.status = request.json["status"]
    pay.balance = a
                      
# int( request.json["amount"]) + int(pay.balance)
    # Commit the changes to the database
    db.session.commit()

    # Re-query the payment to get the most recent data
    p = Payment.query.filter_by(id=id).first()

    # Calculate the new balance
    b =  int(p.amount) - int(p.balance)  # Add the current amount and subtract the old amount
    p.balance = b
    print(b)

    # Commit the balance update
    db.session.commit()

    # Return the success response
    resp = jsonify("success")
    resp.status_code = 200
    return resp










@guest.route("/update_payment_checkout", methods=["PUT"])
@flask_praetorian.auth_required
def update_payment_checkout():
    amount = request.json["amount"]
    id = request.json["id"]
    
    # Query the payment by ID
    pay = Payment.query.filter_by(id=id).first()
    guest_id = request.json["guest_id"]
    # Update the amount by adding the new amount to the existing amount
    a= pay.amount = int(amount) + int(pay.amount)
    pay.amount =a
    pay.method = request.json["method"]
    pay.room_type = request.json["room_type"]
    pay.discount = request.json["discount"]
    pay.children = request.json["children"]
    pay.adult = request.json["adult"]
    pay.checkin_date = request.json["checkin_date"]
    pay.checkout_date = request.json["checkout_date"]
    pay.status = request.json["status"]
    pay.balance = a
                      
# int( request.json["amount"]) + int(pay.balance)
    # Commit the changes to the database
    db.session.commit()


   

    # Re-query the payment to get the most recent data
    p = Payment.query.filter_by(id=id).first()

    # Calculate the new balance
    b =  int(p.amount) - int(p.balance)  # Add the current amount and subtract the old amount
    p.balance = b
    book = Booking.query.filter_by(guest_id=p.guest_id).first()
    guest = Guests.query.filter_by(id=book.guest_id).first()
    room = Rooms.query.filter_by(room_number=book.room_number).first()
    
    # Commit the balance update
    db.session.commit()

    payments = Payment.query.filter_by(guest_id=guest_id, status="success").all()
    if not payments:
        return jsonify({"error": "No successful payments found for this guest"}), 404
    
    total_balance = sum(int(payment.balance) for payment in payments if payment.balance and payment.balance.replace('.', '', 1).isdigit())
    if total_balance<=0:
        book.has_checkout = True
        room.occupied_by = "none"
        room.occupied_state = "available"
        guest.has_checkout = datetime.now()
        db.session.commit()

    else:
        return 401
    # Return the success response
    resp = jsonify("success")
    resp.status_code = 200
    return resp







@guest.route("/delete_payment/<id>",methods=["DELETE"])
def delete_payment(id):
        pay = Payment.query.filter_by(id=id).first()
        db.session.delete(pay)
        db.session.commit()
        resp= jsonify("success")
        resp.status_code=200
        return resp

@guest.route("/checkout/<id>", methods=["PUT"])
@flask_praetorian.auth_required
def checkout(id):
    # Retrieve the booking and corresponding guest
    booking = Booking.query.filter_by(id=id).first()
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    guest = Guests.query.filter_by(id=booking.guest_id).first()
    if not guest:
        return jsonify({"error": "Guest not found"}), 404

    # Get all successful payments
    payments = Payment.query.filter_by(guest_id=booking.guest_id, status="success").all()
    if not payments:
        return jsonify({"error": "No successful payments found for this guest"}), 404

    # Calculate current balance
    total_balance = sum(
        int(payment.balance)
        for payment in payments
        if payment.balance and payment.balance.replace('.', '', 1).isdigit()
    )

    # Get room and room type info
    room = Rooms.query.filter_by(room_number=booking.room_number).first()
    if not room:
        return jsonify({"error": "Room not found"}), 404

    room_type = RoomType.query.filter_by(room_type=room.room_type).first()
    if not room_type:
        return jsonify({"error": "Room type not found"}), 404

    current_time = datetime.now()
    current_time_str = current_time.strftime('%Y-%m-%d %H:%M')
    departure_date = datetime.strptime(booking.departure_date, "%Y-%m-%d")

    # Charge extra days ONLY IF guest already owes money
    if total_balance > 0 and current_time > departure_date:
        extra_days = (current_time - departure_date).days
        extra_charge = extra_days * int(room_type.base_price)

        total_balance += extra_charge
        print(f"Guest stayed {extra_days} extra days. Extra charge: {extra_charge}")

        # Update last payment balance
        last_payment = payments[-1]
        last_payment.balance = str(total_balance)

        try:
            db.session.commit()
        except Exception as e:
            print(f"Error during commit: {e}")
            db.session.rollback()
            return jsonify({"error": "Failed to update balance"}), 401

    # Room and guest checkout status updates
    room.occupied_by = "none"
    room.occupied_state = "available"
    guest.has_checkout = current_time_str
    booking.has_checkout = True

    try:
        db.session.commit()
        print("Room and guest commit successful.")
    except Exception as e:
        print(f"Error during commit: {e}")
        db.session.rollback()
        return jsonify({"error": "Failed to commit changes"}), 401

    return jsonify({"message": "Checkout successful", "balance": total_balance}), 200


@guest.route("/add_reservation", methods=["POST"])
@flask_praetorian.auth_required
def add_reservation():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # Extract data from the request
    name = request.json.get("name")
    arrival = request.json.get("arrival")
    departure = request.json.get("departure")
    email = request.json.get("email")
    phone = request.json.get("phone")
    
    # Create a new reservation object
    rsv = Reservation(
        email=email,
        phone=phone,
        adult=request.json.get("adult"),
        name=name,
        arrival=arrival,
        departure=departure,
        children=request.json.get("children"),
        purpose=request.json.get("purpose"),
        room_type=request.json.get("room_type"),
        room_nmber="Not Assigned",
        Payment_status="Not Yet",
        status="Pending",
        country=request.json.get("country"),
        price=request.json.get("price"),
        created_date=datetime.now(),
        created_by_id=flask_praetorian.current_user().id
    )

    # Save the reservation to the database
    db.session.add(rsv)
    db.session.commit()
    db.session.close()

    # Beautify the email message
    email_message = f"""
    Hello Kevin,

    A new room booking has been received with the following details:

    **Guest Information:**
    - Name: {name}
    - Phone: {phone}
    - Email: {email}
    - Country: {request.json.get('country')}

    **Reservation Details:**
    - Arrival Date: {arrival}
    - Departure Date: {departure}
    - Room Type: {request.json.get('room_type')}
    - Number of Adults: {request.json.get('adult')}
    - Number of Children: {request.json.get('children')}
    - Purpose of Stay: {request.json.get('purpose')}
    - Price: {request.json.get('price')}

    **Reservation Status:**
    - Room Number: Not Assigned
    - Payment Status: Not Yet
    - Current Status: Pending

    Please log in to the system to assign a room and confirm the reservation.

    Best regards,  
    **Kevo Executive Hotel Team**
    """

    # Send the email
    msg = Message(
        subject="New Room Booking - Kevo Executive Hotel",
        sender="jxkalmhefacbuk@gmail.com",
        recipients=["kevinfiadzeawu@gmail.com"]
    )
    # msg.body = email_message
    # mail.send(msg)

    # Return a success response
    return jsonify("success"), 200



@guest.route("/get_reserve",methods=["GET"])
@flask_praetorian.auth_required
def get_reserve():
      us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
      rsv = db.session.query(Reservation).filter(Reservation.created_by_id ==flask_praetorian.current_user().id)
    #   lst = rsv.order_by(desc(Reservation.created_date))
      result = reserve_schema.dump(rsv)
      return jsonify(result)


@guest.route("/get_all_reserve",methods=["GET"])
@flask_praetorian.auth_required
def get_all_reserve():
      us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
      rsv = db.session.query(Reservation).all()

      result = reserve_schema.dump(rsv)
      return jsonify(result)


@guest.route("/get_reserve_for/<id>",methods=["GET"])
@flask_praetorian.auth_required
def get_reserve_for(id):
      rsv = db.session.query(Reservation).filter_by(id=id).all()
      result = reserve_schema.dump(rsv)
      return jsonify(result)

@guest.route("/update_reservation", methods=["PUT"])
@flask_praetorian.auth_required
def update_reservation():
    # Extract data from the request
    reservation_id = request.json.get("id")
    room_number = request.json.get("room_number")
    name = request.json.get("name")
    email = request.json.get("email")

    try:
        # Fetch and update the reservation record
        rsv = Reservation.query.filter_by(id=reservation_id).first()
        if not rsv:
            return jsonify({"error": "Reservation not found"}), 404

        # Update fields
        rsv.adult = request.json.get("adult")
        rsv.name = name
        rsv.email = email
        rsv.phone = request.json.get("phone")
        rsv.arrival = request.json.get("arrival")
        rsv.departure = request.json.get("departure")
        rsv.children = request.json.get("children")
        rsv.purpose = request.json.get("purpose")
        rsv.room_type = request.json.get("room_type")
        rsv.room_nmber = room_number
        rsv.Payment_status = request.json.get("payment_status")
        rsv.status = request.json.get("status")
        rsv.country = request.json.get("country")

        # Commit the updates
        db.session.commit()

        # Beautify the email message
        email_message = f"""
        Hello {name},

        Your reservation has been successfully updated! You can visit your dashboard to track all reservations:  
        [Track Your Reservations](http://localhost:4200/home/track-reservation)

        **Updated Reservation Details:**
        - Room Number(s): {room_number}
        - Arrival Date: {rsv.arrival}
        - Departure Date: {rsv.departure}
        - Number of Adults: {rsv.adult}
        - Number of Children: {rsv.children}
        - Purpose of Stay: {rsv.purpose}
        - Room Type: {rsv.room_type}
        - Payment Status: {rsv.Payment_status}
        - Reservation Status: {rsv.status}

        Thank you for choosing Kevo Executive Hotel.  
        We look forward to hosting you!

        Best regards,  
        **Kevo Executive Hotel Team**
        """

        # Send the email
        msg = Message(
            subject="Reservation Updated - Kevo Executive Hotel",
            sender="jxkalmhefacbuk@gmail.com",
            recipients=[email]
        )
        msg.body = email_message
        # mail.send(msg)

        # Return a success response
        return jsonify("success"), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.session.close()



@guest.route("/cancel_reservation/<id>",methods=["PUT"])
def cancel_reservation(id):
      rsv = Reservation.query.filter_by(id=id).first()
      rsv.status="Cancelled"
      
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =200
      return resp
  
  
@guest.route("/add_refund",methods=["POST"])
@flask_praetorian.auth_required
def add_refund():
          us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
          session = Session.query.filter_by(status="current").first()
          if session:
                 open_date=session.open_date
          authorized_by=request.json["authorized_by"]
          id = request.json["id"]
          refund_amount = request.json["refund_amount"]
        #   amount= request.json["amount"]
          refund = Refund( name = request.json["name"],session=session.open_date,
          refund_amount = request.json["refund_amount"],
        #   description = request.json["description"],
          reason=request.json["reason"],
          authorized_by=request.json["authorized_by"],
          payment_id = request.json["id"],company_name=us.company,
      

          status = "pending",
          refund_time =datetime.now()
          )
          payData = Payment.query.filter_by(id =id).first()
          payData.refund_amount = refund_amount
          
          db.session.add(refund)
          db.session.commit()
          db.session.close()
          mm = "Hello , New Refund initiated by"  +" "+ authorized_by
          msg = Message('Kevo Executive Hotel', sender = 'jxkalmhefacbuk@gmail.com', recipients = ['kevinfiadzeawu@gmail.com'])
          msg.body = mm 
        #   + flask_praetorian.current_user().firstname + " "+flask_praetorian.current_user().lastname
        #   mail.send(msg)
          resp = jsonify("success")
          resp.status_code=200
          return resp
      
@guest.route("/get_refund", methods=["GET"])
@flask_praetorian.auth_required
def get_refund():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # Query the Refund table, ordering by the latest refund time
    refund_list = Refund.query.all().order_by(Refund.refund_time.desc()).all()
    
    # Serialize the results
    result = refund_schema.dump(refund_list)
    
    # Return the JSON response
    return jsonify(result)

@guest.route("/update_refund", methods=["PUT"])
@flask_praetorian.auth_required
def update_refund():
    # Get the refund ID from the request
    refund_id = request.json.get("id")

    if not refund_id:
        return jsonify({"error": "Refund ID is required"}), 400

    # Update refund status
    refund = Refund.query.filter_by(id=refund_id).first()

    if not refund:
        return jsonify({"error": "Refund not found"}), 404

    refund.status = "success"

    # Adjust payment data
    payment = Payment.query.filter_by(id=refund.payment_id).first()
    if not payment:
        return jsonify({"error": "Payment record not found"}), 404

    # Ensure refund doesn't exceed payment amount
    if int(refund.refund_amount) > int(payment.amount):
        return jsonify({"error": "Refund amount cannot exceed payment amount"}), 400

    # Update the payment amount and balance
    payment.amount = int(payment.amount) - int(refund.refund_amount)
    payment.balance = int(payment.balance) - int(refund.refund_amount)

    # Commit changes to the database
    try:
        db.session.commit()
        db.session.refresh(refund)  # Refresh the refund instance to ensure it's still valid in session
        db.session.refresh(payment)  # Refresh the payment instance as well
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

    # Create a beautiful email message
    email_message = f"""
    Hello,

    We are pleased to inform you that your refund request with ID **{refund_id}** has been successfully approved.

    **Refund Details:**
    - Refund ID: {refund_id}
    - Refund Amount: {refund.refund_amount}
    - Remaining Balance: {payment.balance}

    Thank you for choosing Kevo Executive Hotel. If you have any further inquiries, feel free to reach out to us.

    Best regards,  
    **Kevo Executive Hotel Team**
    """

    # Send the email
    msg = Message(
        subject="Refund Approved - Kevo Executive Hotel",
        sender="jxkalmhefacbuk@gmail.com",
        recipients=["kevinfiadzeawu@gmail.com"]
    )
    msg.body = email_message
    # mail.send(msg)

    # Return success response
    return jsonify({"message": "Refund successfully approved"}), 200













@guest.route("/get_budget/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_budget(id):

    inc = Budget.query.filter_by(id=id)
    result = guest_schema.dump(inc)
    return jsonify(result)




@guest.route("/update_Budget",methods=['PUT'])
@flask_praetorian.auth_required
def update_Budget():
    id = request.json["id"]
    sub_data = Budget.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.amount =request.json["amount"]
    sub_data.note = request.json["note"]
    sub_data.type =request.json["type"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@guest.route("/delete_budget<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_budget(id):
      sub_data = Budget.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp











@guest.route("/add_income",methods=['POST'])
@flask_praetorian.auth_required
def add_income():

    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    session = Session.query.filter_by(status="current").first()
    name= request.json["name"]
    amount =request.json["amount"]
    note= request.json["note"]
    date =request.json["date"]
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now()
    inc = Income(name=name,amount=amount,note=note,date=date,session=session.open_date,
                   created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date,company_name=user.company_name,cashier=user.firstname+" "+user.lastname)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp


from flask import jsonify
from sqlalchemy import func
from datetime import datetime
import flask_praetorian

@guest.route("/get_income_list", methods=["GET"])
@flask_praetorian.auth_required
def get_income_list():

    try:

        user = flask_praetorian.current_user()

        # Get only successful paid orders for the company
        sales = HeldCart.query.filter(
            HeldCart.paid_status == "Success"
        ).order_by(HeldCart.created_at.asc()).all()

        result = []

        for item in sales:

            result.append({
                "id": item.id,
                "total": item.total or 0,
                "created_at": item.created_at.strftime("%Y-%m-%d %H:%M:%S") if item.created_at else None,
                "customer": item.customer,
                "paid_status": item.paid_status,
                "payment_method": item.payment_method
            })

        return jsonify({
            "success": True,
            "data": result
        }), 200

    except Exception as e:

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500

@guest.route("/get_income/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_income(id):

    inc = Income.query.filter_by(id=id)
    result = guest_schema.dump(inc)
    return jsonify(result)




@guest.route("/update_income",methods=['PUT'])
@flask_praetorian.auth_required
def update_income():
    id = request.json["id"]
    sub_data = Income.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.amount =request.json["amount"]
    sub_data.note = request.json["note"]
    sub_data.date =request.json["date"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@guest.route("/delete_income/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_income(id):
      sub_data = Income.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp












@guest.route("/add_hall_payment",methods=['POST'])
@flask_praetorian.auth_required
def add_hall_payment():

    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    session = Session.query.filter_by(status="current").first()
    name= request.json["name"]
    amount =request.json["amount"]
    note= request.json["note"]
    date =request.json["date"]
    customer_name= request.json["customer_name"]
    customer_phone =request.json["customer_phone"]
    balance= request.json["balance"]
    method =request.json["method"]
    start_time= request.json["start_time"]
    end_time =request.json["end_time"]
    status="Success"
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now()
    event_payment = EventPayment(name=name,amount=amount,note=note,date=date,session=session.open_date,
                   created_by_id=flask_praetorian.current_user().id ,balance=balance,method=method,customer_name=customer_name,
                   customer_phone=customer_phone,status=status,start_time=start_time,end_time=end_time,
                   created_date=created_date,company_name=user.company_name,received_by=user.firstname+" "+user.lastname)
    inc = Income(name=name,amount=amount,note=note,date=date,session=session.open_date,
                   created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date,company_name=user.company_name,cashier=user.firstname+" "+user.lastname)
  
    db.session.add(inc)
    db.session.add(event_payment)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_hall_payment",methods=['GET'])
@flask_praetorian.auth_required
def get_hall_payment():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = EventPayment.query.all()
    result = guest_schema.dump(inc)
    return jsonify(result)



@guest.route("/get_hall_payment_one/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_hall_payment_one(id):

    inc = EventPayment.query.filter_by(id=id)
    result = guest_schema.dump(inc)
    return jsonify(result)




@guest.route("/update_hall_payment",methods=['PUT'])
@flask_praetorian.auth_required
def update_hall_payment():
    id = request.json["id"]
    sub_data = EventPayment.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.amount =request.json["amount"]
    sub_data.note = request.json["note"]
    sub_data.date =request.json["date"]
    sub_data.customer_name = request.json["customer_name"]
    sub_data.customer_phone =request.json["customer_phone"]
    sub_data.balance = request.json["balance"]
    sub_data.method =request.json["method"]
    sub_data.start_time = request.json["start_time"]
    sub_data.end_time =request.json["end_time"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@guest.route("/delete_event_payment/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_event_payment(id):
      sub_data = EventPayment.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp









@guest.route("/add_item",methods=['POST'])
@flask_praetorian.auth_required
def add_item():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    description =request.json["description"]
    price= request.json["price"]
    unit =request.json["unit"]
    category= request.json["category"]
    family= request.json["family"]
    wholesale= request.json["wholesale"]
    
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now()
    inc = Iteman(name=name,description=description,price=price,is_vip=wholesale,quantity="1000000",
                   created_date=created_date,family=family,category=category,unit=unit,whole_price=request.json["whole_price"])
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_item_list",methods=['GET'])
@flask_praetorian.auth_required
def get_item_list():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Iteman.query.filter_by(is_vip="no")
    result = guest_schema.dump(inc)
    return jsonify(result)



@guest.route("/search_item",methods=['POST'])
@flask_praetorian.auth_required
def search_item():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    item=request.json["find"]
    inc = Iteman.query.filter(Iteman.name.contains(item))
    result = guest_schema.dump(inc)
    return jsonify(result)


@guest.route("/search_discount",methods=['POST'])
@flask_praetorian.auth_required
def search_discount():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    id=request.json["find"]
    inc = Customer.query.filter_by(id=id)
    result = guest_schema.dump(inc)
    return jsonify(result)




@guest.route("/get_item/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_item(id):
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Iteman.query.filter_by(id=id)
    result = guest_schema.dump(inc)
    return jsonify(result)



@guest.route("/get_food/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_food(id):
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    cat = Category.query.filter_by(id=id).first()

    inc = Iteman.query.filter_by(category=cat.name,is_vip="no")
    result = guest_schema.dump(inc)
    return jsonify(result)




@guest.route("/get_food_vip/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_food_vip(id):
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    cat = Category.query.filter_by(id=id).first()

    inc = Iteman.query.filter_by(category=cat.name).all()
    result = guest_schema.dump(inc)
    return jsonify(result)



@guest.route("/update_item",methods=['PUT'])
@flask_praetorian.auth_required
def update_item():
    id = request.json["id"]
    sub_data = Iteman.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.description =request.json["description"]
    sub_data.price =request.json["price"]
    sub_data.Category = request.json["category"]
    sub_data.unit =request.json["unit"]
    sub_data.faily =request.json["family"]
    sub_data.whole_price=request.json["whole_price"]

    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@guest.route("/delete_item/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_item(id):
      sub_data = Iteman.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp








@guest.route("/add_category",methods=['POST'])
@flask_praetorian.auth_required
def add_category():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    description =request.json["description"]
    # price= request.json["price"]
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now()
    inc = Category(name=name,description=description,
                   created_date=created_date)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_category_list",methods=['GET'])
@flask_praetorian.auth_required
def get_category_list():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Category.query.all()
    result = guest_schema.dump(inc)
    return jsonify(result)



@guest.route("/get_categroy/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_categroy(id):

    inc = Category.query.filter_by(id=id)
    result = guest_schema.dump(inc)
    return jsonify(result)




@guest.route("/update_category",methods=['PUT'])
@flask_praetorian.auth_required
def update_category():
    id = request.json["id"]
    sub_data = Category.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.description =request.json["description"]
    # sub_data.price =request.json["price"]

    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@guest.route("/delete_category/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_category(id):
      sub_data = Category.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp











@guest.route("/add_family",methods=['POST'])
@flask_praetorian.auth_required
def add_family():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    description =request.json["description"]
    # price= request.json["price"]
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now()
    inc = Family(name=name,description=description,
                   created_date=created_date)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_family_list",methods=['GET'])
@flask_praetorian.auth_required
def get_family_list():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Family.query.all()
    result = guest_schema.dump(inc)
    return jsonify(result)



@guest.route("/get_family/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_family(id):

    inc = Family.query.filter_by(id=id)
    result = guest_schema.dump(inc)
    return jsonify(result)




@guest.route("/update_family",methods=['PUT'])
@flask_praetorian.auth_required
def update_family():
    id = request.json["id"]
    sub_data = Family.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.description =request.json["description"]
    # sub_data.price =request.json["price"]

    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@guest.route("/delete_family/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_family(id):
      sub_data = Family.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp









@guest.route("/add_unit",methods=['POST'])
@flask_praetorian.auth_required
def add_unit():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()

    name= request.json["name"]
    description =request.json["description"]
    # price= request.json["price"]
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now()
    inc = Unit(name=name,description=description,
                   created_date=created_date,company_name=user.company_name)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_unit_list",methods=['GET'])
@flask_praetorian.auth_required
def get_unit_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Unit.query.filter_by(company_name=user.company_name)
    result = guest_schema.dump(inc)
    return jsonify(result)



@guest.route("/get_unit/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_unit(id):

    inc = Unit.query.filter_by(id=id)
    result = guest_schema.dump(inc)
    return jsonify(result)




@guest.route("/update_unit",methods=['PUT'])
@flask_praetorian.auth_required
def update_unit():
    id = request.json["id"]
    sub_data = Unit.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.description =request.json["description"]
    # sub_data.price =request.json["price"]

    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@guest.route("/delete_unit/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_unit(id):
      sub_data = Unit.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp






@guest.route("/add_budget",methods=['POST'])
@flask_praetorian.auth_required
def add_budget():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # acd = Academic.query.filter_by(guest_name=user.guest_name,status="current").first()
    name= request.json["name"]
    amount =request.json["amount"]
    note= request.json["note"]
    type =request.json["type"]
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now()
    inc = Budget(name=name,amount=amount,note=note,type=type,
                   created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date,company_name=user.company_name)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_budget_list",methods=['GET'])
@flask_praetorian.auth_required
def get_budget_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Budget.query.filter_by(company_name=user.company_name)
    result = guest_schema.dump(inc)
    return jsonify(result)











@guest.route("/search_attendance_date",methods=["POST"])
@flask_praetorian.auth_required
def search_attendance_date():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    # print(date)
    pay = Attendance.query.filter(Attendance.created_date.contains(date),Attendance.company_name.contains(us.company_name) )
    lst = pay.order_by(desc(Attendance.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)



@guest.route("/search_attendance_dates_two",methods=["POST"])
@flask_praetorian.auth_required
def search_attendance_dates_two():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    datetwo= request.json["datetwo"]
    # print(date)
    pay = Attendance.query.filter(
        or_(
                Attendance.created_date.contains(date), Attendance.created_date.contains(datetwo)

        )
    ).filter(Attendance.company_name.contains(us.company_name) )
    lst = pay.order_by(desc(Attendance.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)

@guest.route("/search_income_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_income_dates():
    us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    """
    Searches for income records from HeldCart by a specific date.
    """
    try:
        # Extract the date from the JSON request body
        date = request.json.get("date")
        
        if not date:
            return jsonify({"error": "Date is required"}), 400

        # Parse the date
        from datetime import datetime
        target_date = datetime.strptime(date, '%Y-%m-%d').date()
        
        # Query HeldCart for orders on the specified date
        held_orders = HeldCart.query.filter(
            db.func.date(HeldCart.created_at) == target_date,
            HeldCart.company_name == us.company_name
        ).all()
        
        result = []
        total_sales = 0
        total_collected = 0
        total_balance = 0
        
        for order in held_orders:
            try:
                items = json.loads(order.items) if order.items else []
                
                # Calculate order totals
                order_total = float(order.total) if order.total else 0
                order_balance = float(order.balance) if order.balance else 0
                order_collected = order_total - order_balance
                
                total_sales += order_total
                total_collected += order_collected
                total_balance += order_balance
                
                # Get customer name
                customer_name = "Walk-in"
                if order.customer:
                    # Check if customer is a name or ID
                    try:
                        customer_id = int(order.customer)
                        customer = Customer.query.filter_by(id=customer_id).first()
                        if customer:
                            customer_name = f"{customer.firstname} {customer.lastname}".strip() or "Walk-in"
                    except (ValueError, TypeError):
                        customer_name = order.customer
                
                # Add each item as an income entry
                for item in items:
                    if item.get('confirmed') == False:
                        status = "Pending"
                    elif item.get('confirmed') == True:
                        status = "Confirmed"
                    else:
                        status = "Processing"
                    
                    item_price = float(item.get('price', 0))
                    item_qty = int(item.get('qty', 0))
                    item_total = item_price * item_qty
                    
                    # Calculate prorated amount based on collected ratio
                    if order_total > 0:
                        item_collected = (order_collected / order_total) * item_total
                    else:
                        item_collected = 0
                    
                    result.append({
                        "id": order.id,
                        "name": item.get('name', 'Unknown'),
                        "amount": round(item_collected, 2),
                        "quantity": item_qty,
                        "price": item_price,
                        "total": round(item_total, 2),
                        "order_total": round(order_total, 2),
                        "balance": round(order_balance, 2),
                        "collected": round(order_collected, 2),
                        "payment_method":order.payment_method,
                        "attendant": order.waiter or 'N/A',
                        "cashier": order.waiter or 'N/A',
                        "customer": customer_name,
                        "method": order.paid_status or 'Pending',
                        "status": status,
                        "waiter": order.waiter,
                        "discount": "0",
                        "date": order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else date,
                        "note": order.note or '',
                        "contain_dtf": order.contain_dtf,
                        "contain_digital_printing": order.contain_digital_printing,
                        "contain_large_format": order.contain_large_format,
                        "contain_label": order.contain_label,
                        "contain_food": order.contain_food,
                        "contain_drink": order.contain_drink,
                        "paid_status": order.paid_status,
                        "order_status": order.status,
                        "customer_id": order.customer
                    })
                    
            except Exception as e:
                print(f"Error processing order {order.id}: {e}")
                continue
        
        # Add summary to response
        summary = {
            "total_sales": round(total_sales, 2),
            "total_collected": round(total_collected, 2),
            "total_balance": round(total_balance, 2),
            "total_orders": len(held_orders),
            "total_items": len(result)
        }

        return jsonify({
            "data": result,
            "summary": summary
        }), 200

    except Exception as e:
        # Handle unexpected errors
        print(f"Error in search_income_dates: {str(e)}")
        return jsonify({"error": str(e)}), 500

from datetime import datetime, timedelta
import json

from flask import request, jsonify
from sqlalchemy import desc



@guest.route("/held_cart_report", methods=["POST"])
@flask_praetorian.auth_required
def held_cart_report():
    """
    Generate comprehensive report from HeldCart data with filters
    """
    try:
        us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        data = request.json
        
        date_from = data.get("date_from")
        date_to = data.get("date_to")
        waiter = data.get("waiter")
        cashier = data.get("cashier")
        method = data.get("method")
        department = data.get("department")
        status = data.get("status")  # pending, confirmed, partial, paid
        
        # Base query
        query = HeldCart.query
        
        # Date range filter
        from datetime import datetime, timedelta

# =====================================================
# DATE RANGE FILTER
# =====================================================

        if date_from:
            from_date = datetime.strptime(
                date_from,
                "%Y-%m-%d"
            )

            query = query.filter(
                HeldCart.created_at >= from_date
            )

        if date_to:
            to_date = datetime.strptime(
                date_to,
                "%Y-%m-%d"
            ) + timedelta(days=1)

            query = query.filter(
                HeldCart.created_at < to_date
            )

        # Waiter filter
        if waiter:
            query = query.filter(HeldCart.waiter == waiter)
        
        # Cashier filter (stored in waiter field or separate field)
        if cashier:
            query = query.filter(HeldCart.cashier == waiter)
        
        # Department filter
        if department:
            if department == "bar":
                query = query.filter(HeldCart.contain_drink == "yes")
            elif department == "food":
                query = query.filter(HeldCart.contain_food == "yes")
            elif department == "dtf":
                query = query.filter(HeldCart.contain_dtf == "yes")
            elif department == "digital_printing":
                query = query.filter(HeldCart.contain_digital_printing == "yes")
            elif department == "large_format":
                query = query.filter(HeldCart.contain_large_format == "yes")
            elif department == "label":
                query = query.filter(HeldCart.contain_label == "yes")
        
        # Status filter
        if status:
            if status == "paid":
                query = query.filter(HeldCart.paid_status == "Success")
            elif status == "partial":
                query = query.filter(HeldCart.paid_status == "Partial")
            elif status == "pending":
                query = query.filter(HeldCart.paid_status == "Pending")
            elif status == "confirmed":
                query = query.filter(HeldCart.status == "Confirmed")
        
        # Order by created_at descending
        orders = query.order_by(desc(HeldCart.created_at)).all()
        
        report_data = []
        total_sales = 0
        total_balance = 0
        total_collected = 0
        total_discount = 0
        total_items = 0
        unique_customers = set()
        payment_methods = {}
        department_stats = {}
        waiter_stats = {}
        
        for order in orders:
            try:
                items = json.loads(order.items) if order.items else []
                
                # Calculate totals
                order_total = float(order.total) if order.total else 0
                order_balance = float(order.balance) if order.balance else 0
                order_collected = order_total - order_balance
                
                total_sales += order_total
                total_balance += order_balance
                total_collected += order_collected
                total_items += sum(item.get('qty', 0) for item in items)
                
                if order.customer:
                    unique_customers.add(order.customer)
                
                # Payment method stats
                method_key = order.paid_status or "Unknown"
                payment_methods[method_key] = payment_methods.get(method_key, 0) + order_collected
                
                # Department stats
                depts = []
                if order.contain_drink == "yes": depts.append("Bar")
                if order.contain_food == "yes": depts.append("Restaurant")
                if order.contain_dtf == "yes": depts.append("DTF")
                if order.contain_digital_printing == "yes": depts.append("Digital Printing")
                if order.contain_large_format == "yes": depts.append("Large Format")
                if order.contain_label == "yes": depts.append("Label")
                
                for dept in depts:
                    department_stats[dept] = department_stats.get(dept, 0) + order_collected
                
                # Waiter stats
                if order.waiter:
                    waiter_stats[order.waiter] = waiter_stats.get(order.waiter, 0) + order_collected
                
                report_data.append({
                    "id": order.id,
                    "items": items,
                    "total": order_total,
                    "balance": order_balance,
                    "collected": order_collected,
                    "waiter": order.waiter,
                    "customer": order.customer,
                    "note": order.note,
                    "status": order.status,
                    "paid_status": order.paid_status,
                    "created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else None,
                    "table": order.table,
                    "contain_drink": order.contain_drink,
                    "contain_food": order.contain_food,
                    "contain_dtf": order.contain_dtf,
                    "contain_digital_printing": order.contain_digital_printing,
                    "contain_large_format": order.contain_large_format,
                    "contain_label": order.contain_label,
                    "dtf_confirm": order.dtf_confirm,
                    "food_confirm": order.food_confirm,
                    "drink_confirm": order.drink_confirm,
                    "item_count": sum(item.get('qty', 0) for item in items)
                })
                
            except Exception as e:
                print(f"Error processing order {order.id}: {e}")
                continue
        
        # Calculate averages
        total_orders = len(report_data)
        average_order = total_sales / total_orders if total_orders > 0 else 0
        
        return jsonify({
            "success": True,
            "data": report_data,
            "summary": {
                "total_sales": total_sales,
                "total_balance": total_balance,
                "total_collected": total_collected,
                "total_orders": total_orders,
                "total_items": total_items,
                "average_order": average_order,
                "unique_customers": len(unique_customers),
                "payment_methods": payment_methods,
                "department_stats": department_stats,
                "waiter_stats": waiter_stats
            }
        }), 200
        
    except Exception as e:
        print(f"Error in held_cart_report: {str(e)}")
        db.session.rollback()
        return jsonify({"error": str(e)}), 500




@guest.route("/search_budget_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_budget_dates():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    # print(date)
    pay = Budget.query.filter(Budget.created_date.contains(date),Budget.company_name.contains(us.company_name) )
    lst = pay.order_by(desc(Budget.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)
from datetime import datetime, time
from sqlalchemy import desc

        

from sqlalchemy import func, desc

@guest.route("/searchdates_two", methods=["POST"])
@flask_praetorian.auth_required
def searchdates_two():
    current_user = flask_praetorian.current_user()
    us = User.query.filter_by(id=current_user.id).first()

    date = request.json.get("date")
    date_two = request.json.get("datetwo")

    if not date or not date_two:
        return jsonify({"error": "Both 'date' and 'date_two' must be provided"}), 400

    try:
        payments = Payment.query.filter(
            func.date(Payment.payment_date).between(date, date_two),
            Payment.company_name == us.company_name
        ).order_by(desc(Payment.payment_date)).all()

        result = pay_schema.dump(payments)
        return jsonify(result), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return jsonify({"error": "An error occurred while fetching data"}), 500




@guest.route("/search_purchase_date_two", methods=["POST"])
@flask_praetorian.auth_required
def search_purchase_date_two():
    current_user = flask_praetorian.current_user()
    us = User.query.filter_by(id=current_user.id).first()

    date = request.json.get("date")
    date_two = request.json.get("datetwo")

    if not date or not date_two:
        return jsonify({"error": "Both 'date' and 'date_two' must be provided"}), 400

    try:
        purchases = PurchaseOrder.query.filter(
            func.date(PurchaseOrder.created_date).between(date, date_two),
            PurchaseOrder.company_name == us.company_name
        ).order_by(desc(PurchaseOrder.created_date)).all()

        result = guest_schema.dump(purchases)
        return jsonify(result), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return jsonify({"error": "An error occurred while fetching data"}), 500


from sqlalchemy import func, desc

@guest.route("/search_refund_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_refund_dates_two():
    current_user = flask_praetorian.current_user()
    us = User.query.filter_by(id=current_user.id).first()

    date = request.json.get("date")
    date_two = request.json.get("datetwo")

    if not date or not date_two:
        return jsonify({"error": "Both 'date' and 'date_two' must be provided"}), 400

    try:
        refunds = Refund.query.filter(
            func.date(Refund.refund_time).between(date, date_two),
            Refund.company_name == us.company_name
        ).order_by(desc(Refund.refund_time)).all()

        result = refund_schema.dump(refunds)
        return jsonify(result), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()
        return jsonify({"error": "An error occurred while fetching data"}), 500

# @guest.route("/search_salary_dates",methods=["POST"])
# @flask_praetorian.auth_required
# def search_salary_dates():
#     date = request.json["date"]
    print(date)
#     pay = SalaryPayment.query.filter(SalaryPayment.payment_date.contains(date) )
#     lst = pay.order_by(desc(SalaryPayment.payment_date))
#     result = guest_schema.dump(lst)
#     return jsonify(result)


@guest.route("/search_expense_dates", methods=["POST"])
@flask_praetorian.auth_required

def search_expense_dates():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    """
    Searches for expense records by a specific date.
    """
    try:
        # Extract the date from the JSON request body
        date = request.json.get("date")
        
        if not date:
            return jsonify({"error": "Date is required"}), 400

        # Query the Expenses table for records containing the specified date
        expense_records = Expenses.query.filter(Expenses.date.contains(date),Expenses.company_name.contains(us.company_name))

        # Order the results by date in descending order
        ordered_records = expense_records.order_by(desc(Expenses.date))

        # Serialize the query result
        result = guest_schema.dump(ordered_records)

        # Return the serialized data as a JSON response
        return jsonify(result), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": str(e)}), 500
    




@guest.route("/search_gop_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_gop_dates():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    """
    Searches for expense records by a specific date.
    """
    try:
        # Extract the date from the JSON request body
        date = request.json.get("date")
        
        if not date:
            return jsonify({"error": "Date is required"}), 400

        # Query the Expenses table for records containing the specified date
        gop_records = GOP.query.filter(GOP.date.contains(date),GOP.company_name.contains(us.company_name))

        # Order the results by date in descending order
        ordered_records = gop_records.order_by(desc(GOP.date))

        # Serialize the query result
        result = guest_schema.dump(ordered_records)

        # Return the serialized data as a JSON response
        return jsonify(result), 200

    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": str(e)}), 500




@guest.route("/search_expense_budget_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_expense_budget_dates():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    # year =request.json["year"]
    type ="expense"
    # print(date)
    pay = Budget.query.filter(Budget.created_date.contains(date),Budget.company_name.contains(us.company_name),Budget.type.contains(type))
    lst = pay.order_by(desc(Budget.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)



@guest.route("/search_income_budget_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_income_budget_dates():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    # year =request.json["year"]
    type ="income"
    # print(date)
    pay = Budget.query.filter(Budget.created_date.contains(date),Budget.company_name.contains(us.company_name),Budget.type.contains(type))
    lst = pay.order_by(desc(Budget.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)





@guest.route("/search_expense_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_expense_dates_two():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json.get("date")
    date_two = request.json.get("datetwo")

    # if not date or not date_two:
    #     return jsonify({"error": "Both 'date' and 'datetwo' must be provided"}), 400

    try:
        pay = Expenses.query.filter(
            or_(
                Expenses.session.contains(date),
                Expenses.session.contains(date_two)
            )
        ).filter(Expenses.company_name.contains(us.company_name)).order_by(desc(Expenses.date)).all()

        result = guest_schema.dump(pay)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        db.session.rollback()








@guest.route("/add_store",methods=['POST'])
@flask_praetorian.auth_required
def add_store():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()

    name= request.json["name"]
    description =request.json["description"]
    category= request.json["category"]
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now()
    inc = Store(name=name,description=description,category=category,
                   created_date=created_date,company_name=user.company_name)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_store_list",methods=['GET'])
@flask_praetorian.auth_required
def get_store_list():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Store.query.all()
    result = guest_schema.dump(inc)
    return jsonify(result)




@guest.route("/update_store",methods=['PUT'])
@flask_praetorian.auth_required
def update_store():
    id = request.json["id"]
    sub_data = Store.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.description =request.json["description"]
    sub_data.Category =request.json["category"]

    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp




@guest.route("/delete_store/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_store(id):
      sub_data = Store.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp









@guest.route("/add_stock",methods=['POST'])
@flask_praetorian.auth_required
def add_stock():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    session = Session.query.filter_by(status="current").first()
    name= request.json["name"]
    store =request.json["store"]
    quantity= request.json["quantity"]
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now()
    st = Stock.query.filter_by(name=name).first()
    if st:
        st.quantity= int(st.quantity) + int(quantity)

    inc = Stock(name=name,store=store,quantity=quantity,company_name=user.company_name,
                   created_date=created_date)
    
      
    stu = StockUsage(name=name,operation="Added",store=store,quantity=quantity,created_date=created_date,company_name=user.company_name,
                     session=session.open_date
                      )
  
    db.session.add(inc)
    db.session.add(stu)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_stock_usuage",methods=['GET'])
@flask_praetorian.auth_required
def get_stock_usuage():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = StockUsage.query.filter_by(company_name=user.company_name).order_by(desc(StockUsage.created_date))
    result = guest_schema.dump(inc)
    return jsonify(result)



@guest.route("/get_stock_list",methods=['GET'])
@flask_praetorian.auth_required
def get_stock_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Stock.query.filter_by(company_name=user.company_name)
    result = guest_schema.dump(inc)
    return jsonify(result)




@guest.route("/update_stock",methods=['PUT'])
@flask_praetorian.auth_required
def update_stock():

    id = request.json["id"]
    quantity =request.json["quantity"]
    sub_data = Stock.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.store= request.json["store"]
    sub_data.quantity= int(quantity) + int(sub_data.quantity) 
    # sub_data.Category =request.json["category"]

    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp




@guest.route("/delete_stock/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_stock(id):
      sub_data = Stock.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp








@guest.route("/add_stock_transfer",methods=['POST'])
@flask_praetorian.auth_required
def add_stock_transfer():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    session = Session.query.filter_by(status="current").first()
    name= request.json["name"]
    department =request.json["department"]
    quantity= request.json["quantity"]
    
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now()
    inc = StockTransfer(name=name,quantity=quantity,department=department,
                   created_date=created_date,company_name=user.company_name)
    
    stu = StockUsage(name=name,operation="Transfer",store=department,quantity=quantity,created_date=created_date,company_name=user.company_name,
                     session=session.open_date
                      )
    
    store = Stock.query.filter_by(name=name).first()
    store.quantity = int(store.quantity) - int(quantity)

    item =Iteman.query.filter_by(name=name).first()
    item.quantity = int(item.quantity) + int(quantity)
  
    db.session.add(inc)
    db.session.add(stu)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp








@guest.route("/add_stock_transfer_outside",methods=['POST'])
@flask_praetorian.auth_required
def add_stock_transfer_outside():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    session = Session.query.filter_by(status="current").first()
    name= request.json["name"]
    department =request.json["department"]
    quantity= request.json["quantity"]
    
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now()
    inc = StockTransferOut(name=name,quantity=quantity,department=department,
                   created_date=created_date,company_name=user.company_name)
    
    stu = StockUsage(name=name,operation="Transfer",store=department,quantity=quantity,created_date=created_date,company_name=user.company_name,
                     session=session.open_date
                      )
    
    store = Stock.query.filter_by(name=name).first()
    store.quantity = int(store.quantity) - int(quantity)

    item =Iteman.query.filter_by(name=name).first()
    item.quantity = int(item.quantity) + int(quantity)
  
    db.session.add(inc)
    db.session.add(stu)
 
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp




@guest.route("/get_stock_transfer",methods=['GET'])
@flask_praetorian.auth_required
def get_stock_transfer():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = StockTransfer.query.filter_by(company_name=user.company_name)
    result = guest_schema.dump(inc)
    return jsonify(result)


@guest.route("/get_stock_transfer_outside",methods=['GET'])
@flask_praetorian.auth_required
def get_stock_transfer_outside():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = StockTransferOut.query.filter_by(company_name=user.company_name)
    result = guest_schema.dump(inc)
    return jsonify(result)


@guest.route("/update_stock_transfer",methods=['PUT'])
@flask_praetorian.auth_required
def update_stock_transfer():
    id = request.json["id"]
    sub_data = StockTransfer.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.description =request.json["description"]
    sub_data.quantity =request.json["quantity"]

    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp



@guest.route("/update_stock_transfer_outside",methods=['PUT'])
@flask_praetorian.auth_required
def update_stock_transfer_outside():
    id = request.json["id"]
    sub_data = StockTransferOut.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.description =request.json["description"]
    sub_data.quantity =request.json["quantity"]

    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp




@guest.route("/delete_stock_transfer/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_stock_transfer(id):
      sub_data = Store.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp






@guest.route("/add_vendor",methods=['POST'])
@flask_praetorian.auth_required
def add_vendor():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    phone =request.json["phone"]
    address= request.json["address"]
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now()
    inc = Vendor(name=name,address=address,phone=phone,
                   created_date=created_date,company_name=user.company_name)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_vendor_list",methods=['GET'])
@flask_praetorian.auth_required
def get_vendor_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Vendor.query.filter_by(company_name=user.company_name)
    result = guest_schema.dump(inc)
    print("hello")
    return jsonify(result)




@guest.route("/update_vendor",methods=['PUT'])
@flask_praetorian.auth_required
def update_vendor():
    id = request.json["id"]
    sub_data = Vendor.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.phone =request.json["phone"]
    sub_data.address =request.json["address"]

    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp




@guest.route("/delete_vendor/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_vendor(id):
      sub_data = Vendor.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp





@guest.route("/add_purchase",methods=['POST'])
@flask_praetorian.auth_required
def add_purchase():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    item= request.json["item"]
    quantity =request.json["quantity"]
    unit_price= request.json["unit_price"]
    total_cost = request.json["total_cost"]
    status ="Pending"
    department = request.json["department"]
    # unit_price= request.json["unitPrice"]
    total_cost = request.json["total_cost"]

    # department = request.json["department"]
 
    requested_by = user.firstname + " "+user.lastname
    store = request.json["store"]
    created_date=datetime.now()

    inc = PurchaseRequest(item=item,quantity=quantity,unit_price=unit_price,total_cost=total_cost,status=status,company_name=user.company_name,
                          department=department, requested_by=requested_by,store=store,created_date=created_date)
    
    # usr = user.firstname +" " + user.lastname

  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route('/add_purchase_bulk', methods=['POST'])
@flask_praetorian.auth_required
def add_purchase_bulk():
    user = flask_praetorian.current_user()
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({"error": "Expected a list of purchase items"}), 400

    try:
        # Step 1: Create a new Cart
        new_cart = Cart(
            requested_by=f"{user.firstname} {user.lastname}",
            company_name=user.company_name,
            created_date=datetime.now(),
            status='Pending'
        )
        db.session.add(new_cart)
        db.session.flush()  # so new_cart.id is available

        # Step 2: Add multiple PurchaseRequest items linked to the cart
        for item in data:
            new_request = PurchaseRequest(
                item=item.get('item'),
                quantity=item.get('quantity'),
                unit_price=item.get('unit_price'),
                total_cost=item.get('total_cost'),
                department=item.get('department'),
                store=item.get('store'),
                requested_by=new_cart.requested_by,
                created_date=new_cart.created_date,
                status='Pending',
                company_name=user.company_name,
                cart_id=new_cart.id  # link to parent cart
            )
            db.session.add(new_request)

        db.session.commit()
        return jsonify({"message": "Cart and items saved successfully", "cart_id": new_cart.id}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



@guest.route("/get_purchase_list",methods=['GET'])
@flask_praetorian.auth_required
def get_purchase_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = PurchaseRequest.query.filter_by(company_name=user.company_name)
    result = guest_schema.dump(inc)
    return jsonify(result)


@guest.route("/get_purchase_by_cart/<int:cart_id>", methods=['GET'])
@flask_praetorian.auth_required
def get_purchase_by_cart(cart_id):
    user = User.query.get(flask_praetorian.current_user().id)
    purchases = PurchaseRequest.query.filter_by(cart_id=cart_id).all()
    result = guest_schema.dump(purchases)
    return jsonify(result)



@guest.route("/get_order_list",methods=['GET'])
@flask_praetorian.auth_required
def get_order_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = PurchaseOrder.query.filter_by(company_name=user.company_name)
    result = guest_schema.dump(inc)
    return jsonify(result)



@guest.route("/update_purchase",methods=['PUT'])
@flask_praetorian.auth_required
def update_purchase():
    id = request.json["id"]
    sub_data = PurchaseRequest.query.filter_by(id=id).first()
    sub_data.item = request.json["item"]
    sub_data.quantity =request.json["quantity"]
    sub_data.unit_price =request.json["unit_price"]
    sub_data.Department = request.json["department"]
    sub_data.total_cost =request.json["total_cost"]
  


    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp



@guest.route("/approve_purchase", methods=['PUT', 'POST'])
@flask_praetorian.auth_required
def approve_purchase():
    try:
        # Get the current user
        user = User.query.filter_by(id=flask_praetorian.current_user().id).first()

        # Get the purchase request ID from the request body
        id = request.json["id"]

        # Retrieve the purchase request
        sub_data = PurchaseRequest.query.filter_by(id=id).first()
        if not sub_data:
            return {"message": "Purchase request not found"}, 404

        # Update the purchase request status
        sub_data.status = "Success"
        sub_data.approved_by = f"{user.firstname} {user.lastname}"
        sub_data.approved_date = datetime.now()

        # Create a new purchase order
        item = sub_data.item
        store = sub_data.store  # Assuming 'store' is a valid attribute in the model
        quantity = sub_data.quantity
        created_date = datetime.now()

        new_order = PurchaseOrder(item=item, store=store, created_date=created_date, quantity=quantity,company_name=user.company_name)

        # Add the new order to the session
        db.session.add(new_order)

        # Commit all changes
        db.session.commit()

        return {"message": "Purchase approved successfully"}, 200

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return {"error": str(e)}, 500




@guest.route("/approve_return_request", methods=['PUT', 'POST'])
@flask_praetorian.auth_required
def approve_return_request():
    try:
        # Get the current user
        user = User.query.filter_by(id=flask_praetorian.current_user().id).first()

        # Get the purchase request ID from the request body
        id = request.json["id"]

        # Retrieve the purchase request
        sub_data = returnRequest.query.filter_by(id=id).first()
        if not sub_data:
            return {"message": "Purchase request not found"}, 404

        # Update the purchase request status
        sub_data.status = "Success"
        sub_data.approved_by = f"{user.firstname} {user.lastname}"
        sub_data.approved_date = datetime.now()

        # Create a new purchase order
        item_id= request.json["item_id"]
        item = PurchaseOrder.query.filter_by(id=item_id).first()
        item.voided = "yes" # Assuming 'store' is a valid attribute in the model
       

        # Commit all changes
        db.session.commit()

        return {"message": "Purchase approved successfully"}, 200

    except Exception as e:
        db.session.rollback()  # Rollback in case of error
        return {"error": str(e)}, 500



@guest.route("/delete_purchase/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_purchase(id):
      sub_data = PurchaseRequest.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp








@guest.route("/add_department",methods=['POST'])
@flask_praetorian.auth_required
def add_department():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name = request.json["name"]
    description = request.json["description"]
    hod = request.json["hod"]
    # created_date = db.Column(db.String(400))
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now()
    inc = Department(name=name,description=description,hod=hod,
                   created_date=created_date,company_name=user.company_name)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_department_list",methods=['GET'])
@flask_praetorian.auth_required
def get_department_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Department.query.filter_by(company_name=user.company_name)
    result = guest_schema.dump(inc)
    return jsonify(result)




@guest.route("/update_department",methods=['PUT'])
@flask_praetorian.auth_required
def update_department():
    id = request.json["id"]
    sub_data = Department.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.description =request.json["description"]
    sub_data.Category =request.json["hod"]

    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp




@guest.route("/delete_department/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_department(id):
      sub_data = Department.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp




















@guest.route("/add_received_item", methods=['POST'])
@flask_praetorian.auth_required
def add_received_item():
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    name = request.json["name"]
    quantity = request.json["quantity"]
    expired_date = request.json["expired_date"]
    
    # Generate batch number based on today's date
    # Format example: BATCH-20251030
    batch_number = "BATCH-" + datetime.now().strftime("%Y%m%d")

    created_date = datetime.now()

    itm = ReceivedItem(
        name=name,
        quantity=quantity,
        company_name=user.company_name,
        created_date=created_date,
        expired_date=expired_date,
        batch_number=batch_number
    )

    db.session.add(itm)
    db.session.commit()
    db.session.close()

    resp = jsonify("success")
    resp.status_code = 200
    return resp


@guest.route("/get_received",methods=['GET'])
@flask_praetorian.auth_required
def get_received():    
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    itm = ReceivedItem.query.all()
    result = guest_schema.dump(itm)
    return jsonify(result)

@guest.route("/get_expiry", methods=["GET"])
@flask_praetorian.auth_required
def get_expiry():
    # Get the current logged-in user
    current_user = flask_praetorian.current_user()

    # Fetch items belonging to the user's company, ordered by expiry date (latest to earliest)
    items = (
        ReceivedItem.query
        .filter_by(company_name=current_user.company_name)
        .order_by(desc(ReceivedItem.expired_date))
        .all()
    )

    # Serialize the query result
    result = guest_schema.dump(items)

    return jsonify(result)


@guest.route("/update_received_item",methods=['PUT'])
@flask_praetorian.auth_required
def update_received_item():

    id = request.json["id"]
   
    sub_data = ReceivedItem.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.expired_date = request.json["expired_date"]
    # sub_data.quantity= request.json["store"]
    # sub_data.store= int(quantity) + int(sub_data.quantity) 
    # sub_data.Category =request.json["category"]

    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp




@guest.route("/delete_received_item/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_received_item(id):
      sub_data = ReceivedItem.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp


@guest.route("/add_return_request",methods=['POST'])
@flask_praetorian.auth_required
def add_return_request():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    item_id = request.json["id"]
    item = request.json["item"]
    qty = request.json["quantity"]
    reason = request.json["reason"]
    # itm = Iteman.query.filter_by(id=id).first()
    # itm.voided="yes"
    created_date=datetime.now()
    user = User.query.filter_by(id =flask_praetorian.current_user().id).first()
    request_by= user.firstname +" "+ user.lastname

    a = returnRequest(item_id=item_id,item=item,quantity=qty,reason=reason,created_date=created_date,request_by=request_by,status="Pending")
    db.session.add(a)
    db.session.commit()
    resp = jsonify("success")
    resp.status_code =200
    return resp








@guest.route("/add_gop",methods=['POST'])
@flask_praetorian.auth_required
def add_gop():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    amount =request.json["amount"]
    note= request.json["note"]
    date =request.json["date"]
    usr = user.firstname +" " + user.lastname
    created_date=datetime.now()
    gop = GOP(name=name,amount=amount,note=note,date=date,
                   user=usr,created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date,company_name=user.company_name)
  
    db.session.add(gop)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_gop_list",methods=['GET'])
@flask_praetorian.auth_required
def get_gop_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    gop = GOP.query.filter_by(company_name=user.company_name)
    result = guest_schema.dump(gop)
    return jsonify(result)



@guest.route("/get_gop/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_gop(id):

    gop = GOP.query.filter_by(id=id)
    result = guest_schema.dump(gop)
    return jsonify(result)




@guest.route("/update_gop",methods=['PUT'])
@flask_praetorian.auth_required
def update_gop():
    id = request.json["id"]
    sub_data = GOP.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.amount =request.json["amount"]
    sub_data.note = request.json["note"]
    sub_data.date =request.json["date"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@guest.route("/delete_gop/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_gop(id):
      sub_data = GOP.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp





from datetime import datetime
from flask import jsonify

@guest.route("/add_session", methods=['POST'])
@flask_praetorian.auth_required
def add_session():
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    session_data = Session.query.filter_by(status="current").first()
    
    if session_data:  # Fix: Using `session_data` instead of `session`
        session_data.status = "old"
    
    usr = f"{user.firstname} {user.lastname}"
    created_date = datetime.now()

    # Fix: Assign `None` instead of an empty string for close_date
    new_session = Session(
        open_date=created_date,
        close_date=None,  # Use `None` instead of `""`
        company_name=user.company_name,
        open_by=usr,
        status="current"
    )

    db.session.add(new_session)
    db.session.commit()
    db.session.close()

    return jsonify("success"), 200


@guest.route("/close_session",methods=['PUT'])
@flask_praetorian.auth_required
def close_session():
    id = request.json["id"]
   

    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
  
    usr = user.firstname +" " + user.lastname
    created_date=datetime.now()
    session_data = Session.query.filter_by(id=id).first()
    session_data.status="old"
    session_data.close_by=usr
    session_data.close_date=created_date
  
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp


@guest.route("/get_current_session")
@flask_praetorian.auth_required
def get_current_session():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    session_data =  Session.query.filter_by(status="current").all()
    results = guest_schema.dump(session_data)
    return jsonify(results)



@guest.route("/get_all_session")
@flask_praetorian.auth_required
def get_all_session():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    session_data =  Session.query.all()
    results = guest_schema.dump(session_data)
    return jsonify(results)


@guest.route("/get_wifi_code", methods=["POST"])
@flask_praetorian.auth_required
def get_wifi_code():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    data = request.json  # Get full JSON data
    print("Received dassta:", data)  # Debugging log
    days = data.get("days")  # Use .get() to avoid KeyError
    
    if not days:
        return jsonify({"error": "Missing 'days' in request"}), 400  # Return error if days is missing

    print("Days:", days)  # Confirm 'days' value is received

    # Query for an available WiFi code
    wifi_code = Wifi.query.filter_by(state="available", duration=days,company_name=user.company_name).order_by(func.random()).first()

    if not wifi_code:
        return jsonify({"error": "No available WiFi codes"}), 404  # Return 404 if no matching code is found

    results = pay_schema.dump(wifi_code, many=False) 
     # Serialize result
    print(wifi_code.code)
    print("WiFi Code Found:", results)  # Debugging log
    
    return jsonify(results)

import json








@guest.route('/get_orders', methods=['GET'])
@flask_praetorian.auth_required
def get_orders():
    user = flask_praetorian.current_user()
    orders = OrderItem.query.filter_by(company_name=user.company_name,family="food",status="Pending").order_by(OrderItem.id.desc()).all()
    return jsonify(orders_schema.dump(orders))


@guest.route('/update_order_status/<int:order_id>', methods=['PUT'])
@flask_praetorian.auth_required
def update_order_status(order_id):
    data = request.json
    new_status = data.get("status")

    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404

    order.order_status = new_status
    db.session.commit()

    return jsonify({"message": f"Order {order_id} updated to {new_status}"}), 200



from datetime import datetime, timedelta
from sqlalchemy import func
import json

# # ===================== HELD ORDERS =====================



# @guest.route('/hold_order', methods=['POST'])
# @flask_praetorian.auth_required
# def hold_order():
#     try:
#         user = current_user()
#         data = request.get_json()
#         session = Session.query.filter_by(status="current").first()

#         if not data or 'cartItems' not in data or 'total' not in data:
#             return jsonify({"error": "Invalid request. 'cartItems' and 'total' are required."}), 400

#         hold_id = data.get('id')
#         existing_hold = None

#         if isinstance(hold_id, str) and hold_id.strip() == "":
#             hold_id = None
#         elif hold_id is not None:
#             try:
#                 hold_id = int(hold_id)
#                 existing_hold = HeldCart.query.filter_by(id=hold_id, user_id=user.id).first()
#             except ValueError:
#                 return jsonify({"error": "Invalid hold ID"}), 400

#         if existing_hold:
#             try:
#                 existing_items = json.loads(existing_hold.items)
#             except json.JSONDecodeError:
#                 existing_items = []

#             existing_items_dict = {int(item['id']): item for item in existing_items}
#             updated_items = []

#             # Keep confirmed items and add/update unconfirmed items
#             for item in data['cartItems']:
#                 try:
#                     item_id = int(item["id"])
#                     item_qty = int(item["qty"])
#                 except (ValueError, TypeError):
#                     return jsonify({"error": f"Invalid item ID or quantity: {item}"}), 400

#                 if item_id in existing_items_dict and existing_items_dict[item_id].get("confirmed", False):
#                     updated_items.append(existing_items_dict[item_id])
#                 else:
#                     updated_items.append({
#                         "id": item_id,
#                         "qty": item_qty,
#                         "description": item.get("description", ""),
#                         "name": item["name"],
#                         "price": item["price"],
#                         "family": str(item.get("family", "")).strip(),
#                         "category": str(item.get("category", "")).strip(),
#                         "confirmed": False,
#                         "is_vip": item.get("is_vip", "no")
#                     })

#             contain_drink = any(item.get("family") == "drink" for item in updated_items)
#             contain_food = any(item.get("family") == "food" for item in updated_items)
#             contain_dtf = any(item.get("family") == "dtf" for item in updated_items)
#             contain_digital_printing = any(item.get("family") == "digital_printing" for item in updated_items)
#             contain_large_format = any(item.get("family") == "large_format" for item in updated_items)
#             contain_label = any(item.get("family") == "label" for item in updated_items)
            
#             existing_hold.items = json.dumps(updated_items)
#             existing_hold.total = float(data['total'])
#             existing_hold.contain_drink = "yes" if contain_drink else "no"
#             existing_hold.contain_food = "yes" if contain_food else "no"
#             existing_hold.contain_dtf = "yes" if contain_dtf else "no"
#             existing_hold.contain_digital_printing = "yes" if contain_digital_printing else "no"
#             existing_hold.contain_large_format = "yes" if contain_large_format else "no"
#             existing_hold.contain_label = "yes" if contain_label else "no"

#             order_id = existing_hold.id

#         else:
#             # New held order
#             try:
#                 cart_items = [{
#                     "id": int(item["id"]),
#                     "qty": int(item["qty"]),
#                     "name": item["name"],
#                     "price": item["price"],
#                     "description": item.get("description", ""),
#                     "family": str(item.get("family", "")).strip(),
#                     "category": str(item.get("category", "")).strip(),
#                     "confirmed": False,
#                     "is_vip": item.get("is_vip", "no")
#                 } for item in data["cartItems"]]
#             except (ValueError, TypeError, KeyError):
#                 return jsonify({"error": "Invalid cart items format"}), 400

#             contain_drink = any(item.get("family") == "drink" for item in cart_items)
#             contain_food = any(item.get("family") == "food" for item in cart_items)
#             contain_dtf = any(item.get("family") == "dtf" for item in cart_items)
#             contain_digital_printing = any(item.get("family") == "digital_printing" for item in cart_items)
#             contain_large_format = any(item.get("family") == "large_format" for item in cart_items)
#             contain_label = any(item.get("family") == "label" for item in cart_items)
#             note = data.get("note", "")

#             existing_hold = HeldCart(
#                 user_id=user.id,
#                 items=json.dumps(cart_items),
#                 total=float(data['total']),
#                 customer=data.get('customer', ''),
#                 company_name=user.company_name,
#                 status="Pending",
#                 paid_status="Pending",
#                 onetime="yes",
#                 waiter=f"{user.firstname} {user.lastname}",
#                 contain_drink="yes" if contain_drink else "no",
#                 contain_food="yes" if contain_food else "no",
#                 contain_dtf="yes" if contain_dtf else "no",
#                 contain_digital_printing="yes" if contain_digital_printing else "no",
#                 contain_large_format="yes" if contain_large_format else "no",
#                 contain_label="yes" if contain_label else "no",
#                 food_confirm="no",
#                 drink_confirm="no",
#                 label_confirm="no",
#                 dtf_confirm="no",
#                 large_format_confirm="no",
#                 digital_printing_confirm="no",
#                 session=session.open_date if session else None,
#                 table=data.get('table', ''),
#                 note=note,
#                 balance="0"
#             )
#             db.session.add(existing_hold)
#             db.session.flush()
#             order_id = existing_hold.id

#         db.session.commit()
        
#         return jsonify({
#             "message": "Order held successfully",
#             "id": order_id,
#             "order_id": order_id
#         }), 200

#     except Exception as e:
#         db.session.rollback()
#         print(f"Error in hold_order: {str(e)}")
#         return jsonify({"error": "An error occurred while holding the order", "details": str(e)}), 500


# ===================== CREATE ORDERS WITH BALANCE =====================
@guest.route('/create_orders', methods=['POST'])
@flask_praetorian.auth_required
def create_orders():
    try:
        us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        session = Session.query.filter_by(status="current").first()
        data = request.json

        if not data or 'cartItems' not in data or 'total' not in data:
            return jsonify({"error": "Invalid request"}), 400

        # Get cashier
        cashier = User.query.filter_by(username=data.get("cashier", "")).first()
        if not cashier:
            return jsonify({"error": "Cashier not found"}), 404

        # Get customer - handle both ID and customer_id
        customer_input = data.get("customer")
        customer_name = None
        customer_obj = None
        if customer_input:
            if str(customer_input).isdigit():
                customer_obj = Customer.query.filter_by(id=int(customer_input)).first()
            if not customer_obj:
                customer_obj = Customer.query.filter_by(customer_id=str(customer_input)).first()
            if customer_obj:
                customer_name = f"{customer_obj.firstname} {customer_obj.lastname}"

        phone = data.get("phone", "")
        items = json.dumps(data.get('cartItems', []))
        
        # Get amount paid from request
        amount_paid = float(data.get('amount_paid', 0))
        
        # ✅ Check if this is a balance payment
        is_balance_payment = data.get('is_balance_payment', False)
        balance_to_pay = float(data.get('balance_to_pay', 0))
        
        # Get held cart ID if exists
        held_cart_id = data.get("id")
        held_cart = None
        existing_balance = 0
        held_cart_total = 0
        
        # Check if this is a held order with existing balance
        if held_cart_id:
            held_cart = HeldCart.query.filter_by(id=held_cart_id).first()
            if held_cart:
                held_cart_total = float(held_cart.total) if held_cart.total else 0
                
                try:
                    existing_balance = float(held_cart.balance) if held_cart.balance else 0
                    print(f"🔍 DEBUG: existing_balance={existing_balance}")
                except (ValueError, TypeError):
                    existing_balance = 0
                
                # ✅ CORRECT BALANCE CALCULATION WITH BALANCE PAYMENT SUPPORT
                if is_balance_payment and existing_balance > 0:
                    total_amount = existing_balance
                    new_balance = existing_balance - amount_paid
                    if new_balance < 0:
                        new_balance = 0
                    balance = new_balance
                    print(f"🔍 BALANCE PAYMENT: existing_balance={existing_balance}, amount_paid={amount_paid}, new_balance={new_balance}")
                else:
                    if existing_balance > 0:
                        new_balance = existing_balance - amount_paid
                    else:
                        new_balance = held_cart_total - amount_paid
                    
                    if new_balance < 0:
                        new_balance = 0
                    
                    total_amount = held_cart_total
                    balance = new_balance
                
                print(f"🔍 DEBUG create_orders: held_cart_id={held_cart_id}, held_cart_total={held_cart_total}, existing_balance={existing_balance}, amount_paid={amount_paid}, new_balance={new_balance}")
            else:
                total_amount = float(data['total'])
                balance = total_amount - amount_paid
                if balance < 0:
                    balance = 0
        else:
            total_amount = float(data['total'])
            balance = total_amount - amount_paid
            if balance < 0:
                balance = 0

        # Create new order
        new_order = Order(
            user_id=us.id,
            items=items,
            total=total_amount,
            waiter=us.firstname,
            order_status="Pending",
            status="paid" if balance <= 0 else "pending",
            session=session.open_date if session else None
        )
        db.session.add(new_order)
        db.session.flush()

        # Process each cart item
        for cart_item in data['cartItems']:
            item_name = cart_item.get('name')
            item_quantity = int(cart_item.get('qty', 0))
            category = cart_item.get('category')
            family = cart_item.get('family')
            price = float(cart_item.get('price', 0))
            total_price = price * item_quantity
            
            item = Iteman.query.filter_by(name=item_name).first()
            if not item:
                db.session.rollback()
                return jsonify({"error": f"Item '{item_name}' not found"}), 404

            order_item = OrderItem(
                item_name=item_name,
                order_id=new_order.id,
                item_id=item.id,
                quantity=item_quantity,
                category=category,
                waiter=f"{us.firstname} {us.lastname}",
                status="Pending",
                created_date=datetime.now(),
                family=family,
                session=session.open_date if session else None,
                table=data.get('table', '')
            )
            db.session.add(order_item)

            # Calculate prorated amount for each item based on payment ratio
            if total_amount > 0:
                item_amount_paid = (amount_paid / total_amount) * total_price
            else:
                item_amount_paid = 0

            pos_payment = PosPayment(
                name=item_name,
                amount=item_amount_paid,
                method=data.get("method", "Cash"),
                quantity=item_quantity,
                attendant=f"{us.firstname} {us.lastname}",
                created_by_id=us.id,
                cashier=f"{cashier.firstname} {cashier.lastname}",
                payment_date=datetime.now(),
                session=session.open_date if session else None,
                category=family,
                cat=category,
                customer=customer_name,
                phone=phone
            )
            db.session.add(pos_payment)

            income = Income(
                name=item_name,
                attendant=f"{us.firstname} {us.lastname}",
                amount=item_amount_paid,
                date=datetime.now(),
                discount=data.get("discount", 0),
                note="Pos Payment" + (" (Pending)" if balance > 0 else ""),
                created_date=datetime.now(),
                created_by_id=us.id,
                cashier=f"{cashier.firstname} {cashier.lastname}",
                session=session.open_date if session else None,
                method=data.get("method", "Cash"),
                category=family,
                cat=category,
                customer=customer_name,
                phone=phone
            )
            db.session.add(income)

        # ✅ UPDATE ALL pending held carts for this user
        held_carts = HeldCart.query.filter_by(user_id=us.id, paid_status="Pending").all()
        for held_cart in held_carts:
            if balance <= 0:
                # held_cart.status = "Confirmed"
                held_cart.paid_status = "Success"
                held_cart.balance = "0"
                print(f"✅ Held cart {held_cart.id} marked as SUCCESS (balance: {balance})")
            else:
                held_cart.status = "Pending"
                held_cart.paid_status = "Pending"
                held_cart.balance = str(balance)
                print(f"⏳ Held cart {held_cart.id} marked as PENDING (balance: {balance})")
            
            if customer_obj:
                held_cart.customer = customer_name

        db.session.commit()

        return jsonify({
            "id": new_order.id,
            "company_name": new_order.company_name,
            "created_at": new_order.created_at.strftime('%Y-%m-%d %H:%M:%S') if new_order.created_at else None,
            "items": items,
            "order_status": new_order.order_status,
            "total": total_amount,
            "balance": balance,
            "amount_paid": amount_paid,
            "existing_balance": existing_balance,
            "held_cart_total": held_cart_total,
            "user_id": new_order.user_id,
            "waiter": new_order.waiter,
            "is_balance_payment": is_balance_payment
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error in create_orders: {str(e)}")
        return jsonify({"error": str(e)}), 500


# @guest.route('/create_orders_all', methods=['POST'])
# @flask_praetorian.auth_required
# def create_orders_all():
#     try:
#         us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
#         session = Session.query.filter_by(status="current").first()
#         data = request.json

#         if not data or 'cartItems' not in data or 'total' not in data:
#             return jsonify({"error": "Invalid request"}), 400

#         # Get cashier
#         cashier = User.query.filter_by(username=data.get("cashier", "")).first()
#         if not cashier:
#             return jsonify({"error": "Cashier not found"}), 404

#         # Get customer - handle both ID and customer_id
#         customer_input = data.get("customer")
#         customer_name = None
#         if customer_input:
#             customer = None
#             if str(customer_input).isdigit():
#                 customer = Customer.query.filter_by(id=int(customer_input)).first()
#             if not customer:
#                 customer = Customer.query.filter_by(customer_id=str(customer_input)).first()
#             if customer:
#                 customer_name = f"{customer.firstname} {customer.lastname}"

#         phone = data.get("phone", "")
#         items = json.dumps(data.get('cartItems', []))
        
#         # Get amount paid and calculate balance
#         total_amount = float(data['total'])
#         amount_paid = float(data.get('amount_paid', total_amount))
#         balance = total_amount - amount_paid
        
#         if amount_paid > total_amount:
#             amount_paid = total_amount
#             balance = 0

#         # Create new order
#         new_order = Order(
#             user_id=us.id,
#             items=items,
#             total=total_amount,
#             waiter=us.firstname,
#             order_status="Pending",
#             status="paid" if balance <= 0 else "Pending",
#             session=session.open_date if session else None
#         )
#         db.session.add(new_order)
#         db.session.flush()

#         # Process each cart item
#         for cart_item in data['cartItems']:
#             item_name = cart_item.get('name')
#             item_quantity = int(cart_item.get('qty', 0))
#             category = cart_item.get('category')
#             family = cart_item.get('family')
#             price = float(cart_item.get('price', 0))
#             total_price = price * item_quantity
            
#             item = Iteman.query.filter_by(name=item_name).first()
#             if not item:
#                 db.session.rollback()
#                 return jsonify({"error": f"Item '{item_name}' not found"}), 404

#             order_item = OrderItem(
#                 item_name=item_name,
#                 order_id=new_order.id,
#                 item_id=item.id,
#                 quantity=item_quantity,
#                 category=category,
#                 waiter=f"{us.firstname} {us.lastname}",
#                 status="Pending",
#                 created_date=datetime.now(),
#                 family=family,
#                 session=session.open_date if session else None,
#                 table=data.get('table', '')
#             )
#             db.session.add(order_item)

#             if total_amount > 0:
#                 item_amount_paid = (amount_paid / total_amount) * total_price
#             else:
#                 item_amount_paid = 0

#             pos_payment = PosPayment(
#                 name=item_name,
#                 amount=item_amount_paid,
#                 method=data.get("method", "Cash"),
#                 quantity=item_quantity,
#                 attendant=f"{us.firstname} {us.lastname}",
#                 created_by_id=us.id,
#                 cashier=f"{cashier.firstname} {cashier.lastname}",
#                 payment_date=datetime.now(),
#                 session=session.open_date if session else None,
#                 category=family,
#                 cat=category,
#                 customer=customer_name,
#                 phone=phone
#             )
#             db.session.add(pos_payment)

#             income = Income(
#                 name=item_name,
#                 amount=item_amount_paid,
#                 date=datetime.now(),
#                 note="Pos Payment" + (" (Pending)" if balance > 0 else ""),
#                 created_date=datetime.now(),
#                 created_by_id=us.id,
#                 cashier=f"{cashier.firstname} {cashier.lastname}",
#                 session=session.open_date if session else None,
#                 method=data.get("method", "Cash"),
#                 category=family,
#                 cat=category,
#                 customer=customer_name,
#                 phone=phone
#             )
#             db.session.add(income)

#         # Update ALL pending held carts for this user
#         held_carts = HeldCart.query.filter_by(user_id=us.id, paid_status="Pending").all()
#         for held_cart in held_carts:
#             held_cart.status = "Confirmed" if balance <= 0 else "Pending"
#             held_cart.paid_status = "Success" if balance <= 0 else "Pending"
#             held_cart.balance = str(balance) if balance > 0 else "0"

#         db.session.commit()

#         return jsonify({
#             "id": new_order.id,
#             "company_name": new_order.company_name,
#             "created_at": new_order.created_at.strftime('%Y-%m-%d %H:%M:%S') if new_order.created_at else None,
#             "items": items,
#             "order_status": new_order.order_status,
#             "total": new_order.total,
#             "balance": balance,
#             "amount_paid": amount_paid,
#             "user_id": new_order.user_id,
#             "waiter": new_order.waiter
#         }), 201

#     except Exception as e:
#         db.session.rollback()
#         print(f"Error in create_orders_all: {str(e)}")
#         return jsonify({"error": str(e)}), 500


# @guest.route('/create_orders_two', methods=['POST'])
# @flask_praetorian.auth_required
# def create_orders_two():
#     try:
#         us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
#         session = Session.query.filter_by(status="current").first()
#         data = request.json

#         if not data or 'cartItems' not in data or 'total' not in data:
#             return jsonify({"error": "Invalid request"}), 400

#         # Get cashier
#         cashier = User.query.filter_by(username=data.get("cashier", "")).first()
#         if not cashier:
#             return jsonify({"error": "Cashier not found"}), 404

#         # Get customer - handle both ID and customer_id
#         customer_input = data.get("customer")
#         customer_name = None
#         if customer_input:
#             customer = None
#             if str(customer_input).isdigit():
#                 customer = Customer.query.filter_by(id=int(customer_input)).first()
#             if not customer:
#                 customer = Customer.query.filter_by(customer_id=str(customer_input)).first()
#             if customer:
#                 customer_name = f"{customer.firstname} {customer.lastname}"

#         phone = data.get("phone", "")
#         items = json.dumps(data.get('cartItems', []))
        
#         # Get amount paid and calculate balance
#         total_amount = float(data['total'])
#         amount_paid = float(data.get('amount_paid', total_amount))
#         balance = total_amount - amount_paid
        
#         if amount_paid > total_amount:
#             amount_paid = total_amount
#             balance = 0

#         # Create new order
#         new_order = Order(
#             user_id=us.id,
#             items=items,
#             total=total_amount,
#             waiter=us.firstname,
#             order_status="Pending",
#             status="paid" if balance <= 0 else "Pending",
#             session=session.open_date if session else None
#         )
#         db.session.add(new_order)
#         db.session.flush()

#         # Process each cart item
#         for cart_item in data['cartItems']:
#             item_name = cart_item.get('name')
#             item_quantity = int(cart_item.get('qty', 0))
#             category = cart_item.get('category')
#             family = cart_item.get('family')
#             price = float(cart_item.get('price', 0))
#             total_price = price * item_quantity
            
#             item = Iteman.query.filter_by(name=item_name).first()
#             if not item:
#                 db.session.rollback()
#                 return jsonify({"error": f"Item '{item_name}' not found"}), 404

#             order_item = OrderItem(
#                 item_name=item_name,
#                 order_id=new_order.id,
#                 item_id=item.id,
#                 quantity=item_quantity,
#                 category=category,
#                 waiter=f"{us.firstname} {us.lastname}",
#                 status="Pending",
#                 table=data.get('table', ''),
#                 created_date=datetime.now(),
#                 family=family,
#                 session=session.open_date if session else None
#             )
#             db.session.add(order_item)

#             if total_amount > 0:
#                 item_amount_paid = (amount_paid / total_amount) * total_price
#             else:
#                 item_amount_paid = 0

#             pos_payment = PosPayment(
#                 name=item_name,
#                 amount=item_amount_paid,
#                 method=data.get("method", "Cash"),
#                 quantity=item_quantity,
#                 attendant=f"{us.firstname} {us.lastname}",
#                 created_by_id=us.id,
#                 cashier=f"{cashier.firstname} {cashier.lastname}",
#                 payment_date=datetime.now(),
#                 session=session.open_date if session else None,
#                 category=family,
#                 cat=category,
#                 customer=customer_name,
#                 phone=phone
#             )
#             db.session.add(pos_payment)

#             income = Income(
#                 name=item_name,
#                 attendant=f"{us.firstname} {us.lastname}",
#                 amount=item_amount_paid,
#                 date=datetime.now(),
#                 discount=data.get("discount", 0),
#                 note="Pos Payment" + (" (Pending)" if balance > 0 else ""),
#                 created_date=datetime.now(),
#                 created_by_id=us.id,
#                 cashier=f"{cashier.firstname} {cashier.lastname}",
#                 session=session.open_date if session else None,
#                 method=data.get("method", "Cash"),
#                 category=family,
#                 cat=category,
#                 customer=customer_name,
#                 phone=phone
#             )
#             db.session.add(income)

#             # Update held cart
#             held_cart_id = data.get("id")
#             if held_cart_id:
#                 held_cart = HeldCart.query.filter_by(id=held_cart_id).first()
#                 if held_cart:
#                     held_cart.status = "Confirmed" if balance <= 0 else "Pending"
#                     held_cart.paid_status = "Success" if balance <= 0 else "Pending"
#                     held_cart.balance = str(balance) if balance > 0 else "0"

#         db.session.commit()

#         return jsonify({
#             "id": new_order.id,
#             "company_name": new_order.company_name,
#             "created_at": new_order.created_at.strftime('%Y-%m-%d %H:%M:%S') if new_order.created_at else None,
#             "items": items,
#             "order_status": new_order.order_status,
#             "total": new_order.total,
#             "balance": balance,
#             "amount_paid": amount_paid,
#             "user_id": new_order.user_id,
#             "waiter": new_order.waiter
#         }), 201

#     except Exception as e:
#         db.session.rollback()
#         print(f"Error in create_orders_two: {str(e)}")
#         return jsonify({"error": str(e)}), 500


# @guest.route('/create_orders_two_all', methods=['POST'])
# @flask_praetorian.auth_required
# def create_orders_two_all():
#     try:
#         us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
#         session = Session.query.filter_by(status="current").first()
#         data = request.json

#         if not data or 'cartItems' not in data or 'total' not in data:
#             return jsonify({"error": "Invalid request"}), 400

#         # Get cashier
#         cashier = User.query.filter_by(username=data.get("cashier", "")).first()
#         if not cashier:
#             return jsonify({"error": "Cashier not found"}), 404

#         # Get customer - handle both ID and customer_id
#         customer_input = data.get("customer")
#         customer_name = None
#         if customer_input:
#             customer = None
#             if str(customer_input).isdigit():
#                 customer = Customer.query.filter_by(id=int(customer_input)).first()
#             if not customer:
#                 customer = Customer.query.filter_by(customer_id=str(customer_input)).first()
#             if customer:
#                 customer_name = f"{customer.firstname} {customer.lastname}"

#         phone = data.get("phone", "")
#         items = json.dumps(data.get('cartItems', []))
        
#         # Get amount paid and calculate balance
#         total_amount = float(data['total'])
#         amount_paid = float(data.get('amount_paid', total_amount))
#         balance = total_amount - amount_paid
        
#         if amount_paid > total_amount:
#             amount_paid = total_amount
#             balance = 0

#         # Create new order
#         new_order = Order(
#             user_id=us.id,
#             items=items,
#             total=total_amount,
#             waiter=us.firstname,
#             order_status="Pending",
#             status="paid" if balance <= 0 else "Pending",
#             session=session.open_date if session else None
#         )
#         db.session.add(new_order)
#         db.session.flush()

#         # Process each cart item
#         for cart_item in data['cartItems']:
#             item_name = cart_item.get('name')
#             item_quantity = int(cart_item.get('qty', 0))
#             category = cart_item.get('category')
#             family = cart_item.get('family')
#             price = float(cart_item.get('price', 0))
#             total_price = price * item_quantity
            
#             item = Iteman.query.filter_by(name=item_name).first()
#             if not item:
#                 db.session.rollback()
#                 return jsonify({"error": f"Item '{item_name}' not found"}), 404

#             order_item = OrderItem(
#                 item_name=item_name,
#                 order_id=new_order.id,
#                 item_id=item.id,
#                 quantity=item_quantity,
#                 category=category,
#                 waiter=f"{us.firstname} {us.lastname}",
#                 status="Pending",
#                 created_date=datetime.now(),
#                 family=family,
#                 session=session.open_date if session else None,
#                 table=data.get('table', '')
#             )
#             db.session.add(order_item)

#             if total_amount > 0:
#                 item_amount_paid = (amount_paid / total_amount) * total_price
#             else:
#                 item_amount_paid = 0

#             pos_payment = PosPayment(
#                 name=item_name,
#                 amount=item_amount_paid,
#                 method=data.get("method", "Cash"),
#                 quantity=item_quantity,
#                 attendant=f"{us.firstname} {us.lastname}",
#                 created_by_id=us.id,
#                 cashier=f"{cashier.firstname} {cashier.lastname}",
#                 payment_date=datetime.now(),
#                 session=session.open_date if session else None,
#                 category=family,
#                 cat=category,
#                 customer=customer_name,
#                 phone=phone
#             )
#             db.session.add(pos_payment)

#             income = Income(
#                 name=item_name,
#                 amount=item_amount_paid,
#                 date=datetime.now(),
#                 note="Pos Payment" + (" (Pending)" if balance > 0 else ""),
#                 created_date=datetime.now(),
#                 created_by_id=us.id,
#                 cashier=f"{cashier.firstname} {cashier.lastname}",
#                 session=session.open_date if session else None,
#                 method=data.get("method", "Cash"),
#                 category=family,
#                 cat=category,
#                 customer=customer_name,
#                 phone=phone
#             )
#             db.session.add(income)

#         # Update ALL pending held carts for this user
#         held_carts = HeldCart.query.filter_by(user_id=us.id, paid_status="Pending").all()
#         for held_cart in held_carts:
#             held_cart.status = "Confirmed" if balance <= 0 else "Pending"
#             held_cart.paid_status = "Success" if balance <= 0 else "Pending"
#             held_cart.balance = str(balance) if balance > 0 else "0"

#         db.session.commit()

#         return jsonify({
#             "id": new_order.id,
#             "company_name": new_order.company_name,
#             "created_at": new_order.created_at.strftime('%Y-%m-%d %H:%M:%S') if new_order.created_at else None,
#             "items": items,
#             "order_status": new_order.order_status,
#             "total": new_order.total,
#             "balance": balance,
#             "amount_paid": amount_paid,
#             "user_id": new_order.user_id,
#             "waiter": new_order.waiter
#         }), 201

#     except Exception as e:
#         db.session.rollback()
#         print(f"Error in create_orders_two_all: {str(e)}")
#         return jsonify({"error": str(e)}), 500


# # ===================== CREDIT PAYMENT =====================

# @guest.route('/credit', methods=['POST'])
# @flask_praetorian.auth_required
# def credit():
#     try:
#         us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
#         session = Session.query.filter_by(status="current").first()
#         data = request.json

#         if not data or 'cartItems' not in data or 'total' not in data:
#             return jsonify({"error": "Invalid request"}), 400

#         # Get cashier
#         cashier = User.query.filter_by(username=data.get("cashier", "")).first()
#         if not cashier:
#             return jsonify({"error": "Cashier not found"}), 404

#         # Get customer - handle both ID and customer_id
#         customer_input = data.get("customer")
#         customer_name = None
#         if customer_input:
#             customer = None
#             if str(customer_input).isdigit():
#                 customer = Customer.query.filter_by(id=int(customer_input)).first()
#             if not customer:
#                 customer = Customer.query.filter_by(customer_id=str(customer_input)).first()
#             if customer:
#                 customer_name = f"{customer.firstname} {customer.lastname}"

#         phone = data.get("phone", "")
#         items = json.dumps(data.get('cartItems', []))
        
#         # Get amount paid and calculate balance
#         total_amount = float(data['total'])
#         amount_paid = float(data.get('amount_paid', total_amount))
#         balance = total_amount - amount_paid
        
#         if amount_paid > total_amount:
#             amount_paid = total_amount
#             balance = 0

#         # Create new order
#         new_order = Order(
#             user_id=us.id,
#             items=items,
#             total=total_amount,
#             waiter=us.firstname,
#             order_status="Pending",
#             status="paid" if balance <= 0 else "Pending",
#             session=session.open_date if session else None
#         )
#         db.session.add(new_order)
#         db.session.flush()

#         # Create credit record
#         credit = Credit(
#             user_id=us.id,
#             items=items,
#             total=total_amount,
#             waiter=us.firstname,
#             order_status="Success",
#             status="credit" if balance <= 0 else "Pending_credit",
#             customer=customer_name,
#             phone=phone,
#             session=session.open_date if session else None,
#             balance=str(balance) if balance > 0 else "0"
#         )
#         db.session.add(credit)

#         # Process each cart item
#         for cart_item in data['cartItems']:
#             item_name = cart_item.get('name')
#             item_quantity = int(cart_item.get('qty', 0))
#             category = cart_item.get('category')
#             family = cart_item.get('family')
#             price = float(cart_item.get('price', 0))
#             total_price = price * item_quantity
            
#             item = Iteman.query.filter_by(name=item_name).first()
#             if not item:
#                 db.session.rollback()
#                 return jsonify({"error": f"Item '{item_name}' not found"}), 404

#             order_item = OrderItem(
#                 item_name=item_name,
#                 order_id=new_order.id,
#                 item_id=item.id,
#                 quantity=item_quantity,
#                 category=category,
#                 waiter=f"{us.firstname} {us.lastname}",
#                 status="Pending",
#                 created_date=datetime.now(),
#                 family=family,
#                 session=session.open_date if session else None,
#                 table=data.get('table', '')
#             )
#             db.session.add(order_item)

#             if total_amount > 0:
#                 item_amount_paid = (amount_paid / total_amount) * total_price
#             else:
#                 item_amount_paid = 0

#             pos_payment = PosPayment(
#                 name=item_name,
#                 amount=item_amount_paid,
#                 method="Credit" + (" (Pending)" if balance > 0 else ""),
#                 quantity=item_quantity,
#                 attendant=f"{us.firstname} {us.lastname}",
#                 created_by_id=us.id,
#                 cashier=f"{cashier.firstname} {cashier.lastname}",
#                 payment_date=datetime.now(),
#                 session=session.open_date if session else None,
#                 category=family,
#                 cat=category,
#                 customer=customer_name,
#                 phone=phone
#             )
#             db.session.add(pos_payment)

#         # Update ALL pending held carts for this user
#         held_carts = HeldCart.query.filter_by(user_id=us.id, paid_status="Pending").all()
#         for held_cart in held_carts:
#             held_cart.status = "Confirmed" if balance <= 0 else "Pending"
#             held_cart.paid_status = "Success" if balance <= 0 else "Pending"
#             held_cart.balance = str(balance) if balance > 0 else "0"

#         db.session.commit()

#         return jsonify({
#             "id": new_order.id,
#             "company_name": new_order.company_name,
#             "created_at": new_order.created_at.strftime('%Y-%m-%d %H:%M:%S') if new_order.created_at else None,
#             "items": items,
#             "order_status": new_order.order_status,
#             "total": new_order.total,
#             "balance": balance,
#             "amount_paid": amount_paid,
#             "user_id": new_order.user_id,
#             "waiter": new_order.waiter
#         }), 201

#     except Exception as e:
#         db.session.rollback()
#         print(f"Error in credit: {str(e)}")
#         return jsonify({"error": str(e)}), 500


from datetime import datetime, timedelta
from sqlalchemy import func
import json

# ===================== HELD ORDERS =====================

@guest.route('/load_held_order_all', methods=['GET'])
@flask_praetorian.auth_required
def load_held_order_all():
    try:
        us = flask_praetorian.current_user()
        held_orders = HeldCart.query.filter_by(user_id=us.id, paid_status="Pending").all()

        if not held_orders:
            return jsonify([]), 200

        result = []
        for order in held_orders:
            try:
                items = json.loads(order.items) if order.items else []
            except:
                items = []
            
            result.append({
                "id": order.id,
                "items": items,
                "total": order.total,
                "customer": order.customer,
                "balance": order.balance or "0",
                "created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else None
            })

        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@guest.route('/hold_order', methods=['POST'])
@flask_praetorian.auth_required
def hold_order():
    try:
        user = current_user()
        data = request.get_json()
        session = Session.query.filter_by(status="current").first()
        customer = Customer.query.filter_by(id=data.get('customer')).first() if data.get('customer') else None

        if not data or 'cartItems' not in data or 'total' not in data:
            return jsonify({"error": "Invalid request. 'cartItems' and 'total' are required."}), 400

        hold_id = data.get('id')
        existing_hold = None

        if isinstance(hold_id, str) and hold_id.strip() == "":
            hold_id = None
        elif hold_id is not None:
            try:
                hold_id = int(hold_id)
                existing_hold = HeldCart.query.filter_by(id=hold_id, user_id=user.id).first()
            except ValueError:
                return jsonify({"error": "Invalid hold ID"}), 400

        # Get amount paid from request (for Pending payments)
        amount_paid = data.get('amount_paid', 0)
        try:
            amount_paid = float(amount_paid) if amount_paid else 0
        except (ValueError, TypeError):
            amount_paid = 0

        # Calculate total
        total = float(data.get('total', 0))

        # Get existing balance if updating an existing hold
        existing_balance = 0
        if existing_hold:
            try:
                existing_balance = float(existing_hold.balance) if existing_hold.balance else 0
            except (ValueError, TypeError):
                existing_balance = 0

        # Calculate new balance
        if amount_paid > 0:
            new_balance = total - amount_paid
        else:
            new_balance = total

        if existing_balance > 0:
            new_balance = new_balance + existing_balance

        if new_balance < 0:
            new_balance = 0

        if existing_hold:
            try:
                existing_items = json.loads(existing_hold.items)
            except json.JSONDecodeError:
                existing_items = []

            existing_items_dict = {int(item['id']): item for item in existing_items}
            updated_items = []

            for item in data['cartItems']:
                try:
                    item_id = int(item["id"])
                    item_qty = int(item["qty"])
                except (ValueError, TypeError):
                    return jsonify({"error": f"Invalid item ID or quantity: {item}"}), 400

                if item_id in existing_items_dict and existing_items_dict[item_id].get("confirmed", False):
                    updated_items.append(existing_items_dict[item_id])
                else:
                    updated_items.append({
                        "id": item_id,
                        "qty": item_qty,
                        "description": item.get("description", ""),
                        "name": item["name"],
                        "price": item["price"],
                        "family": str(item.get("family", "")).strip(),
                        "is_checked": str(item.get("is_checked", "no")).strip(),
                        "checked_by": str(flask_praetorian.current_user().firstname+" "+flask_praetorian.current_user().lastname) if item.get("is_checked", "no") == "yes" else "",
                        "category": str(item.get("category", "")).strip(),
                        "confirmed": False,
                        "is_vip": item.get("is_vip", "no")
                    })

            contain_drink = any(item.get("family") == "drink" for item in updated_items)
            contain_food = any(item.get("family") == "food" for item in updated_items)
            contain_dtf = any(item.get("family") == "dtf" for item in updated_items)
            contain_digital_printing = any(item.get("family") == "digital_printing" for item in updated_items)
            contain_large_format = any(item.get("family") == "large_format" for item in updated_items)
            contain_label = any(item.get("family") == "label" for item in updated_items)
            
            existing_hold.items = json.dumps(updated_items)
            existing_hold.total = total
            existing_hold.balance = str(new_balance)
            existing_hold.contain_drink = "yes" if contain_drink else "no"
            existing_hold.contain_food = "yes" if contain_food else "no"
            existing_hold.contain_dtf = "yes" if contain_dtf else "no"
            existing_hold.contain_digital_printing = "yes" if contain_digital_printing else "no"
            existing_hold.contain_large_format = "yes" if contain_large_format else "no"
            existing_hold.contain_label = "yes" if contain_label else "no"

            if new_balance <= 0:
                existing_hold.status = "Confirmed"
                existing_hold.paid_status = "Success"
            else:
                existing_hold.status = "Pending"
                existing_hold.paid_status = "Pending"

            if data.get('customer'):
                existing_hold.customer = data.get('customer')
            
            if data.get('note'):
                existing_hold.note = data.get('note')
            
            if data.get('table'):
                existing_hold.table = data.get('table')

            order_id = existing_hold.id

        else:
            # New held order
            try:
                cart_items = [{
                    "id": int(item["id"]),
                    "qty": int(item["qty"]),
                    "name": item["name"],
                    "price": item["price"],
                    "description": item.get("description", ""),
                    "family": str(item.get("family", "")).strip(),
                    "category": str(item.get("category", "")).strip(),
                    "confirmed": False,
                    "is_checked": "no",
                    "checked_by": "",
                    "is_vip": item.get("is_vip", "no")
                } for item in data["cartItems"]]
            except (ValueError, TypeError, KeyError):
                return jsonify({"error": "Invalid cart items format"}), 400

            contain_drink = any(item.get("family") == "drink" for item in cart_items)
            contain_food = any(item.get("family") == "food" for item in cart_items)
            contain_dtf = any(item.get("family") == "dtf" for item in cart_items)
            contain_digital_printing = any(item.get("family") == "digital_printing" for item in cart_items)
            contain_large_format = any(item.get("family") == "large_format" for item in cart_items)
            contain_label = any(item.get("family") == "label" for item in cart_items)
            note = data.get("note", "")

            existing_hold = HeldCart(
                user_id=user.id,
                items=json.dumps(cart_items),
                total=total,
                balance="0",
                customer=data.get('customer', ''),
                company_name=user.company_name,
                status="Pending" if new_balance > 0 else "Confirmed",
                paid_status="Pending" if new_balance > 0 else "Success",
                onetime="yes",
                waiter=f"{user.firstname} {user.lastname}",
                contain_drink="yes" if contain_drink else "no",
                contain_food="yes" if contain_food else "no",
                contain_dtf="yes" if contain_dtf else "no",
                contain_digital_printing="yes" if contain_digital_printing else "no",
                contain_large_format="yes" if contain_large_format else "no",
                contain_label="yes" if contain_label else "no",
                food_confirm="no",
                drink_confirm="no",
                label_confirm="no",
                dtf_confirm="no",
                large_format_confirm="no",
                digital_printing_confirm="no",
                customer_id=customer.id,
                session=session.open_date if session else None,
                table=data.get('table', ''),
                note=note
            )
            db.session.add(existing_hold)
            db.session.flush()
            order_id = existing_hold.id

        db.session.commit()
        
        # --- SEND EMAIL IF CUSTOMER HAS EMAIL ---
        customer_email = None
        customer_name = "Valued Customer"
        
        if customer:
            customer_email = getattr(customer, 'email', None)
            customer_name = getattr(customer, 'firstname', '') + ' ' + getattr(customer, 'lastname', '')
            if not customer_name or customer_name.strip() == '':
                customer_name = "Valued Customer"
        
        # Also check if customer data was passed directly in request
        if not customer_email and data.get('customer_email'):
            customer_email = data.get('customer_email')
        
        if not customer_name and data.get('customer_name'):
            customer_name = data.get('customer_name')
        
        # Send email if we have a customer email and it's a valid email address
        if customer_email and '@' in str(customer_email):
            try:
                # Prepare order items for email
                order_items = []
                if existing_hold:
                    try:
                        items_list = json.loads(existing_hold.items)
                        for item in items_list:
                            # Ensure price and qty are numbers
                            price = float(item.get('price', 0))
                            qty = int(item.get('qty', 0))
                            order_items.append({
                                'name': str(item.get('name', 'Item')),
                                'qty': qty,
                                'price': price,
                                'family': str(item.get('family', '')),
                                'category': str(item.get('category', ''))
                            })
                    except Exception as e:
                        print(f"⚠️ Error parsing items: {str(e)}")
                        order_items = []
                
                # Determine order type
                order_type = "Order"
                if contain_food and contain_drink:
                    order_type = "Food & Drink Order"
                elif contain_food:
                    order_type = "Food Order"
                elif contain_drink:
                    order_type = "Drink Order"
                elif contain_dtf:
                    order_type = "DTF Print Order"
                elif contain_digital_printing:
                    order_type = "Digital Printing Order"
                elif contain_large_format:
                    order_type = "Large Format Order"
                elif contain_label:
                    order_type = "Label Order"
                
                # Build email HTML with safe string formatting
                from datetime import datetime
                now = datetime.now()
                
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Order Confirmation - Asempahfie Graphics</title>
                    <style>
                        body {{
                            font-family: 'Segoe UI', Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            background-color: #f8f9fa;
                            color: #333;
                        }}
                        .email-container {{
                            max-width: 600px;
                            margin: 20px auto;
                            background-color: #ffffff;
                            border-radius: 12px;
                            overflow: hidden;
                            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                        }}
                        .header {{
                            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                            padding: 30px 20px;
                            text-align: center;
                            border-bottom: 4px solid #e94560;
                        }}
                        .header h1 {{
                            color: #ffffff;
                            font-size: 24px;
                            margin: 0;
                            font-weight: 700;
                            letter-spacing: 1px;
                        }}
                        .header .subtitle {{
                            color: #e0e0e0;
                            font-size: 14px;
                            margin: 5px 0 0;
                            opacity: 0.9;
                        }}
                        .content {{
                            padding: 30px;
                        }}
                        .greeting {{
                            font-size: 18px;
                            color: #1a1a2e;
                            margin-bottom: 15px;
                            font-weight: 600;
                        }}
                        .greeting span {{
                            color: #e94560;
                        }}
                        .order-status {{
                            background: linear-gradient(135deg, #fff5f5 0%, #fff0f0 100%);
                            border-left: 4px solid #e94560;
                            padding: 12px 18px;
                            border-radius: 6px;
                            margin: 20px 0;
                            display: flex;
                            align-items: center;
                            justify-content: space-between;
                        }}
                        .order-status .label {{
                            font-weight: 600;
                            color: #1a1a2e;
                        }}
                        .order-status .value {{
                            background: #e94560;
                            color: white;
                            padding: 4px 14px;
                            border-radius: 20px;
                            font-size: 13px;
                            font-weight: 600;
                            text-transform: uppercase;
                            letter-spacing: 0.5px;
                        }}
                        .order-details {{
                            background: #f8f9fa;
                            border-radius: 8px;
                            padding: 15px 20px;
                            margin: 20px 0;
                            border: 1px solid #e9ecef;
                        }}
                        .order-details p {{
                            margin: 6px 0;
                            font-size: 14px;
                            color: #555;
                        }}
                        .order-details strong {{
                            color: #1a1a2e;
                            font-weight: 600;
                        }}
                        .items-table {{
                            width: 100%;
                            border-collapse: collapse;
                            margin: 20px 0;
                            font-size: 14px;
                        }}
                        .items-table th {{
                            background: #1a1a2e;
                            color: white;
                            padding: 12px 15px;
                            text-align: left;
                            font-weight: 600;
                            font-size: 13px;
                            text-transform: uppercase;
                            letter-spacing: 0.5px;
                        }}
                        .items-table td {{
                            padding: 12px 15px;
                            border-bottom: 1px solid #e9ecef;
                            color: #333;
                        }}
                        .items-table tr:last-child td {{
                            border-bottom: none;
                        }}
                        .items-table .family-badge {{
                            display: inline-block;
                            background: #e9ecef;
                            padding: 2px 10px;
                            border-radius: 12px;
                            font-size: 11px;
                            color: #555;
                            font-weight: 600;
                            text-transform: uppercase;
                        }}
                        .total-section {{
                            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                            color: white;
                            padding: 20px;
                            border-radius: 8px;
                            margin: 20px 0;
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                        }}
                        .total-section .total-label {{
                            font-size: 16px;
                            font-weight: 600;
                            opacity: 0.9;
                        }}
                        .total-section .total-amount {{
                            font-size: 24px;
                            font-weight: 700;
                            color: #ffd700;
                        }}
                        .payment-info {{
                            background: #f0f7ff;
                            border-radius: 8px;
                            padding: 15px 20px;
                            margin: 15px 0;
                            border: 1px solid #d4e4ff;
                        }}
                        .payment-info p {{
                            margin: 4px 0;
                            font-size: 14px;
                            color: #1a3a5c;
                        }}
                        .footer {{
                            background: #f8f9fa;
                            padding: 25px 30px;
                            text-align: center;
                            border-top: 1px solid #e9ecef;
                            font-size: 13px;
                            color: #888;
                        }}
                        .footer .shop-name {{
                            font-size: 16px;
                            font-weight: 700;
                            color: #1a1a2e;
                            margin-bottom: 5px;
                        }}
                        .footer .shop-info {{
                            color: #666;
                            margin: 3px 0;
                        }}
                        @media (max-width: 600px) {{
                            .content {{
                                padding: 20px 15px;
                            }}
                            .items-table th,
                            .items-table td {{
                                padding: 8px 10px;
                                font-size: 12px;
                            }}
                            .header h1 {{
                                font-size: 20px;
                            }}
                            .total-section {{
                                flex-direction: column;
                                text-align: center;
                            }}
                            .total-section .total-amount {{
                                margin-top: 5px;
                                font-size: 22px;
                            }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="header">
                            <h1>Asempahfie Graphics</h1>
                            <div class="subtitle">📍 Kokomlemle, Accra • 📞 0243210009</div>
                        </div>
                        
                        <div class="content">
                            <div class="greeting">Dear <span>{customer_name}</span>,</div>
                            
                            <p style="color: #555; font-size: 15px; line-height: 1.6;">
                                Thank you for choosing <strong>Asempahfie Graphics</strong>! 🎉
                                We are delighted to confirm that your <strong>{order_type}</strong> has been received 
                                and is currently being processed.
                            </p>
                            
                            <div class="order-status">
                                <span class="label">📋 Order Status:</span>
                                <span class="value">Processing</span>
                            </div>
                            
                            <div class="order-details">
                                <p><strong>🆔 Order ID:</strong> #{order_id}</p>
                                <p><strong>📅 Date:</strong> {now.strftime('%A, %B %d, %Y at %I:%M %p')}</p>
                                <p><strong>👤 Prepared By:</strong> {user.firstname} {user.lastname}</p>
                                <p><strong>📋 Order Type:</strong> {order_type}</p>
                                <p><strong>💰 Balance:</strong> {'GHS ' + str(new_balance) if new_balance > 0 else 'Fully Paid ✅'}</p>
                            </div>
                            
                            <h3 style="color: #1a1a2e; margin: 25px 0 15px; font-size: 16px;">🛒 Order Items</h3>
                            
                            <table class="items-table">
                                <thead>
                                    <tr>
                                        <th>Item</th>
                                        <th>Category</th>
                                        <th style="text-align: center;">Qty</th>
                                        <th style="text-align: right;">Price</th>
                                        <th style="text-align: right;">Total</th>
                                    </tr>
                                </thead>
                                <tbody>
                """
                
                # Build items table - FIXED: use separate variable for subtotal
                subtotal = 0.0
                for item in order_items:
                    item_total = float(item['qty']) * float(item['price'])
                    subtotal = subtotal + item_total  # FIXED: use separate variable
                    html_content += f"""
                                    <tr>
                                        <td><strong>{item['name']}</strong></td>
                                        <td><span class="family-badge">{item.get('family', 'General')}</span></td>
                                        <td style="text-align: center;">{item['qty']}</td>
                                        <td style="text-align: right;">GHS {item['price']:.2f}</td>
                                        <td style="text-align: right;">GHS {item_total:.2f}</td>
                                    </tr>
                    """
                
                html_content += f"""
                                </tbody>
                            </table>
                            
                            <div class="total-section">
                                <span class="total-label">Order Total</span>
                                <span class="total-amount">GHS {total:.2f}</span>
                            </div>
                            
                            <div class="payment-info">
                                <p><strong>💳 Payment Status:</strong> {'Paid in Full ✅' if new_balance <= 0 else 'Pending - Balance of GHS ' + str(new_balance)}</p>
                                <p><strong>📝 Note:</strong> {data.get('note', 'No special instructions')}</p>
                            </div>
                            
                            <p style="color: #555; font-size: 14px; line-height: 1.6; margin-top: 20px;">
                                💖 We truly appreciate your business! Our team is working diligently to ensure 
                                your order is prepared with the utmost care and quality. You will receive another 
                                notification when your order is ready for pickup or delivery.
                            </p>
                            
                            <p style="color: #1a1a2e; font-size: 14px; margin: 15px 0 5px; font-weight: 600;">
                                📢 Need assistance? Reach out to us!
                            </p>
                            <p style="color: #666; font-size: 13px; margin: 0;">
                                📞 Call: 0243210009 • 📧 Email: info@asempahfiegraphics.com
                            </p>
                            <p style="color: #666; font-size: 13px; margin: 5px 0;">
                                📍 Visit us: Kokomlemle, Accra (Opposite the Police Station)
                            </p>
                        </div>
                        
                        <div class="footer">
                            <div class="shop-name">✨ Asempahfie Graphics ✨</div>
                            <div class="shop-info">📍 Kokomlemle, Accra</div>
                            <div class="shop-info">📞 0243210009</div>
                            <div class="shop-info">📧 info@asempahfiegraphics.com</div>
                            <p style="margin-top: 15px; font-size: 12px; color: #aaa;">
                                © {now.year} Asempahfie Graphics. All rights reserved.
                            </p>
                            <p style="font-size: 11px; color: #bbb; margin: 5px 0 0;">
                                This is an automated confirmation. Please do not reply to this email.
                            </p>
                        </div>
                    </div>
                </body>
                </html>
                """
                
                # Send email
                from flask_mail import Mail, Message
                from flask import current_app
                
                # Initialize mail with current app context
                # mail = Mail(current_app)
                
                msg = Message(
                    subject=f"🎉 Order Confirmed! #{order_id} - Asempahfie Graphics",
                    recipients=[str(customer_email)],
                    html=html_content, sender="afgghana@gmail.com"
                )
                
                mail.send(msg)
                
                # Log email sent
                print(f"✅ Order confirmation email sent to {customer_email} for order #{order_id}")
                email_sent = True
                
            except Exception as email_error:
                # Log the error but don't fail the request
                print(f"⚠️ Failed to send email to {customer_email}: {str(email_error)}")
                print(f"⚠️ Email error details: {type(email_error).__name__}")
                # Continue execution - email failure shouldn't break the order
                email_sent = False
        else:
            # No email provided - just continue silently
            if customer_email:
                print(f"ℹ️ Invalid email format for order #{order_id}: {customer_email}")
            else:
                print(f"ℹ️ No email provided for order #{order_id}, skipping email notification")
            email_sent = False
        
        return jsonify({
            "message": "Order held successfully",
            "id": order_id,
            "order_id": order_id,
            "balance": str(new_balance),
            "total": str(total),
            "amount_paid": str(amount_paid),
            "email_sent": bool(customer_email and '@' in str(customer_email) and email_sent)
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error in hold_order: {str(e)}")
        print(f"❌ Error details: {type(e).__name__}")
        return jsonify({"error": str(e)}), 500






@guest.route('/hold_order_customer', methods=['POST'])
@flask_praetorian.auth_required
def hold_order_customer():
    try:
        user = current_user()
        data = request.get_json()
        session = Session.query.filter_by(status="current").first()
        
        if not data or 'cartItems' not in data or 'total' not in data:
            return jsonify({"error": "Invalid request. 'cartItems' and 'total' are required."}), 400

        hold_id = data.get('id')
        existing_hold = None

        if isinstance(hold_id, str) and hold_id.strip() == "":
            hold_id = None
        elif hold_id is not None:
            try:
                hold_id = int(hold_id)
                existing_hold = HeldCart.query.filter_by(id=hold_id, user_id=user.id).first()
            except ValueError:
                return jsonify({"error": "Invalid hold ID"}), 400

        # Get amount paid from request
        amount_paid = data.get('amount_paid', 0)
        try:
            amount_paid = float(amount_paid) if amount_paid else 0
        except (ValueError, TypeError):
            amount_paid = 0

        # Calculate total
        total = float(data.get('total', 0))

        # Get existing balance if updating an existing hold
        existing_balance = 0
        if existing_hold:
            try:
                existing_balance = float(existing_hold.balance) if existing_hold.balance else 0
            except (ValueError, TypeError):
                existing_balance = 0

        # Calculate new balance
        if amount_paid > 0:
            new_balance = total - amount_paid
        else:
            new_balance = total

        if existing_balance > 0:
            new_balance = new_balance + existing_balance

        if new_balance < 0:
            new_balance = 0

        if existing_hold:
            try:
                existing_items = json.loads(existing_hold.items)
            except json.JSONDecodeError:
                existing_items = []

            existing_items_dict = {int(item['id']): item for item in existing_items}
            updated_items = []

            for item in data['cartItems']:
                try:
                    item_id = int(item["id"])
                    item_qty = int(item["qty"])
                except (ValueError, TypeError):
                    return jsonify({"error": f"Invalid item ID or quantity: {item}"}), 400

                if item_id in existing_items_dict and existing_items_dict[item_id].get("confirmed", False):
                    updated_items.append(existing_items_dict[item_id])
                else:
                    # Include attachment data if present
                    attachment_data = None
                    if item.get('attachment'):
                        attachment_data = {
                            "base64": item['attachment'].get('base64', ''),
                            "name": item['attachment'].get('name', ''),
                            "type": item['attachment'].get('type', ''),
                            "size": item['attachment'].get('size', 0)
                        }
                    
                    updated_items.append({
                        "id": item_id,
                        "qty": item_qty,
                        "description": item.get("description", ""),
                        "name": item["name"],
                        "price": item["price"],
                        "family": str(item.get("family", "")).strip(),
                        "is_checked": str(item.get("is_checked", "no")).strip(),
                        "checked_by": str(flask_praetorian.current_user().firstname + " " + flask_praetorian.current_user().lastname) if item.get("is_checked", "no") == "yes" else "",
                        "category": str(item.get("category", "")).strip(),
                        "confirmed": False,
                        "is_vip": item.get("is_vip", "no"),
                        "attachment": attachment_data
                    })

            contain_drink = any(item.get("family") == "drink" for item in updated_items)
            contain_food = any(item.get("family") == "food" for item in updated_items)
            contain_dtf = any(item.get("family") == "dtf" for item in updated_items)
            contain_digital_printing = any(item.get("family") == "digital_printing" for item in updated_items)
            contain_large_format = any(item.get("family") == "large_format" for item in updated_items)
            contain_label = any(item.get("family") == "label" for item in updated_items)
            
            existing_hold.items = json.dumps(updated_items)
            existing_hold.total = total
            existing_hold.balance = str(new_balance)
            existing_hold.contain_drink = "yes" if contain_drink else "no"
            existing_hold.contain_food = "yes" if contain_food else "no"
            existing_hold.contain_dtf = "yes" if contain_dtf else "no"
            existing_hold.contain_digital_printing = "yes" if contain_digital_printing else "no"
            existing_hold.contain_large_format = "yes" if contain_large_format else "no"
            existing_hold.contain_label = "yes" if contain_label else "no"

            if new_balance <= 0:
                existing_hold.status = "Confirmed"
                existing_hold.paid_status = "Success"
            else:
                existing_hold.status = "Pending"
                existing_hold.paid_status = "Pending"

            if data.get('customer'):
                existing_hold.customer = data.get('customer')
            
            if data.get('note'):
                existing_hold.note = data.get('note')
            
            if data.get('table'):
                existing_hold.table = data.get('table')
            
            if data.get('payment_method'):
                existing_hold.payment_method = data.get('payment_method')

            order_id = existing_hold.id

        else:
            # NEW HELD ORDER - FIXED CUSTOMER HANDLING
            try:
                cart_items = []
                for item in data["cartItems"]:
                    attachment_data = None
                    if item.get('attachment'):
                        attachment_data = {
                            "base64": item['attachment'].get('base64', ''),
                            "name": item['attachment'].get('name', ''),
                            "type": item['attachment'].get('type', ''),
                            "size": item['attachment'].get('size', 0)
                        }
                    
                    # Ensure we use the correct ID
                    item_id = item.get("id")
                    if isinstance(item_id, str) and item_id.isdigit():
                        item_id = int(item_id)
                    elif not isinstance(item_id, int):
                        # If ID is not a number, use a fallback
                        item_id = hash(item.get("name", "")) % 1000000
                    
                    cart_items.append({
                        "id": item_id,
                        "qty": int(item.get("qty", 1)),
                        "name": str(item.get("name", "")),
                        "price": float(item.get("price", 0)),
                        "description": str(item.get("description", "")),
                        "family": str(item.get("family", "")).strip(),
                        "category": str(item.get("category", "")).strip(),
                        "confirmed": False,
                        "is_checked": "no",
                        "checked_by": "",
                        "is_vip": item.get("is_vip", "no"),
                        "attachment": attachment_data
                    })
            except Exception as e:
                print(f"Error processing cart items: {str(e)}")
                return jsonify({"error": f"Invalid cart items format: {str(e)}"}), 400

            contain_drink = any(item.get("family") == "drink" for item in cart_items)
            contain_food = any(item.get("family") == "food" for item in cart_items)
            contain_dtf = any(item.get("family") == "dtf" for item in cart_items)
            contain_digital_printing = any(item.get("family") == "digital_printing" for item in cart_items)
            contain_large_format = any(item.get("family") == "large_format" for item in cart_items)
            contain_label = any(item.get("family") == "label" for item in cart_items)
            note = data.get("note", "")

            # ✅ FIX: Use the authenticated user's ID, NOT the customer name
            # The customer name is stored as a string field, not as the ID
            customer_name = data.get('customer', f"{user.firstname} {user.lastname}")

            existing_hold = HeldCart(
                user_id=user.id,  # This is the authenticated user's ID (integer)
                items=json.dumps(cart_items),
                total=total,
                balance=str(new_balance),
                customer=customer_name, 
                customer_id=user.id,  # This is the customer ID (string)
                company_name=user.company_name if hasattr(user, 'company_name') else '',
                status="Pending" if new_balance > 0 else "Confirmed",
                paid_status="Pending" if new_balance > 0 else "Success",
                onetime="yes",
                waiter=f"{user.firstname} {user.lastname}",
                contain_drink="yes" if contain_drink else "no",
                contain_food="yes" if contain_food else "no",
                contain_dtf="yes" if contain_dtf else "no",
                contain_digital_printing="yes" if contain_digital_printing else "no",
                contain_large_format="yes" if contain_large_format else "no",
                contain_label="yes" if contain_label else "no",
                food_confirm="no",
                drink_confirm="no",
                label_confirm="no",
                dtf_confirm="no",
                large_format_confirm="no",
                digital_printing_confirm="no",
                session=session.open_date if session else None,
                table=data.get('table', ''),
                note=note,
                payment_method=data.get('payment_method', '')
            )
            db.session.add(existing_hold)
            db.session.flush()
            order_id = existing_hold.id

        db.session.commit()
        
        # ===================== SEND EMAIL =====================
        customer_email = None
        customer_name = data.get('customer', f"{user.firstname} {user.lastname}")
        
        # Try to get email from user
        if user and hasattr(user, 'email') and user.email:
            customer_email = user.email
        
        # Also check if customer email was passed directly in request
        if data.get('customer_email'):
            customer_email = data.get('customer_email')
        
        # Send email if we have a customer email and it's a valid email address
        email_sent = False
        if customer_email and '@' in str(customer_email):
            try:
                # Prepare order items for email
                order_items = []
                if existing_hold:
                    try:
                        items_list = json.loads(existing_hold.items)
                        for item in items_list:
                            price = float(item.get('price', 0))
                            qty = int(item.get('qty', 0))
                            order_items.append({
                                'name': str(item.get('name', 'Item')),
                                'qty': qty,
                                'price': price,
                                'family': str(item.get('family', '')),
                                'category': str(item.get('category', ''))
                            })
                    except Exception as e:
                        print(f"⚠️ Error parsing items: {str(e)}")
                        order_items = []
                
                # Determine order type
                order_type = "Order"
                if contain_food and contain_drink:
                    order_type = "Food & Drink Order"
                elif contain_food:
                    order_type = "Food Order"
                elif contain_drink:
                    order_type = "Drink Order"
                elif contain_dtf:
                    order_type = "DTF Print Order"
                elif contain_digital_printing:
                    order_type = "Digital Printing Order"
                elif contain_large_format:
                    order_type = "Large Format Order"
                elif contain_label:
                    order_type = "Label Order"
                
                # Build email HTML
                from datetime import datetime
                now = datetime.now()
                
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Order Confirmation - Asempahfie Graphics</title>
                    <style>
                        body {{
                            font-family: 'Segoe UI', Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            background-color: #f8f9fa;
                            color: #333;
                        }}
                        .email-container {{
                            max-width: 600px;
                            margin: 20px auto;
                            background-color: #ffffff;
                            border-radius: 12px;
                            overflow: hidden;
                            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                        }}
                        .header {{
                            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                            padding: 30px 20px;
                            text-align: center;
                            border-bottom: 4px solid #e94560;
                        }}
                        .header h1 {{
                            color: #ffffff;
                            font-size: 24px;
                            margin: 0;
                            font-weight: 700;
                            letter-spacing: 1px;
                        }}
                        .header .subtitle {{
                            color: #e0e0e0;
                            font-size: 14px;
                            margin: 5px 0 0;
                            opacity: 0.9;
                        }}
                        .content {{
                            padding: 30px;
                        }}
                        .greeting {{
                            font-size: 18px;
                            color: #1a1a2e;
                            margin-bottom: 15px;
                            font-weight: 600;
                        }}
                        .greeting span {{
                            color: #e94560;
                        }}
                        .order-status {{
                            background: linear-gradient(135deg, #fff5f5 0%, #fff0f0 100%);
                            border-left: 4px solid #e94560;
                            padding: 12px 18px;
                            border-radius: 6px;
                            margin: 20px 0;
                            display: flex;
                            align-items: center;
                            justify-content: space-between;
                        }}
                        .order-status .label {{
                            font-weight: 600;
                            color: #1a1a2e;
                        }}
                        .order-status .value {{
                            background: #e94560;
                            color: white;
                            padding: 4px 14px;
                            border-radius: 20px;
                            font-size: 13px;
                            font-weight: 600;
                            text-transform: uppercase;
                            letter-spacing: 0.5px;
                        }}
                        .order-details {{
                            background: #f8f9fa;
                            border-radius: 8px;
                            padding: 15px 20px;
                            margin: 20px 0;
                            border: 1px solid #e9ecef;
                        }}
                        .order-details p {{
                            margin: 6px 0;
                            font-size: 14px;
                            color: #555;
                        }}
                        .order-details strong {{
                            color: #1a1a2e;
                            font-weight: 600;
                        }}
                        .items-table {{
                            width: 100%;
                            border-collapse: collapse;
                            margin: 20px 0;
                            font-size: 14px;
                        }}
                        .items-table th {{
                            background: #1a1a2e;
                            color: white;
                            padding: 12px 15px;
                            text-align: left;
                            font-weight: 600;
                            font-size: 13px;
                            text-transform: uppercase;
                            letter-spacing: 0.5px;
                        }}
                        .items-table td {{
                            padding: 12px 15px;
                            border-bottom: 1px solid #e9ecef;
                            color: #333;
                        }}
                        .items-table tr:last-child td {{
                            border-bottom: none;
                        }}
                        .items-table .family-badge {{
                            display: inline-block;
                            background: #e9ecef;
                            padding: 2px 10px;
                            border-radius: 12px;
                            font-size: 11px;
                            color: #555;
                            font-weight: 600;
                            text-transform: uppercase;
                        }}
                        .attachment-note {{
                            background: #f0f7ff;
                            border-radius: 6px;
                            padding: 10px 15px;
                            margin: 10px 0;
                            border-left: 3px solid #3498db;
                        }}
                        .attachment-note small {{
                            color: #555;
                            font-size: 12px;
                        }}
                        .total-section {{
                            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                            color: white;
                            padding: 20px;
                            border-radius: 8px;
                            margin: 20px 0;
                            display: flex;
                            justify-content: space-between;
                            align-items: center;
                        }}
                        .total-section .total-label {{
                            font-size: 16px;
                            font-weight: 600;
                            opacity: 0.9;
                        }}
                        .total-section .total-amount {{
                            font-size: 24px;
                            font-weight: 700;
                            color: #ffd700;
                        }}
                        .payment-info {{
                            background: #f0f7ff;
                            border-radius: 8px;
                            padding: 15px 20px;
                            margin: 15px 0;
                            border: 1px solid #d4e4ff;
                        }}
                        .payment-info p {{
                            margin: 4px 0;
                            font-size: 14px;
                            color: #1a3a5c;
                        }}
                        .footer {{
                            background: #f8f9fa;
                            padding: 25px 30px;
                            text-align: center;
                            border-top: 1px solid #e9ecef;
                            font-size: 13px;
                            color: #888;
                        }}
                        .footer .shop-name {{
                            font-size: 16px;
                            font-weight: 700;
                            color: #1a1a2e;
                            margin-bottom: 5px;
                        }}
                        .footer .shop-info {{
                            color: #666;
                            margin: 3px 0;
                        }}
                        @media (max-width: 600px) {{
                            .content {{
                                padding: 20px 15px;
                            }}
                            .items-table th,
                            .items-table td {{
                                padding: 8px 10px;
                                font-size: 12px;
                            }}
                            .header h1 {{
                                font-size: 20px;
                            }}
                            .total-section {{
                                flex-direction: column;
                                text-align: center;
                            }}
                            .total-section .total-amount {{
                                margin-top: 5px;
                                font-size: 22px;
                            }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="header">
                            <h1>Asempahfie Graphics</h1>
                            <div class="subtitle">📍 Kokomlemle, Accra • 📞 0243210009</div>
                        </div>
                        
                        <div class="content">
                            <div class="greeting">Dear <span>{customer_name}</span>,</div>
                            
                            <p style="color: #555; font-size: 15px; line-height: 1.6;">
                                Thank you for choosing <strong>Asempahfie Graphics</strong>! 🎉
                                We are delighted to confirm that your <strong>{order_type}</strong> has been received 
                                and is currently being processed.
                            </p>
                            
                            <div class="order-status">
                                <span class="label">📋 Order Status:</span>
                                <span class="value">Processing</span>
                            </div>
                            
                            <div class="order-details">
                                <p><strong>🆔 Order ID:</strong> #{order_id}</p>
                                <p><strong>📅 Date:</strong> {now.strftime('%A, %B %d, %Y at %I:%M %p')}</p>
                                <p><strong>👤 Prepared By:</strong> {user.firstname} {user.lastname}</p>
                                <p><strong>📋 Order Type:</strong> {order_type}</p>
                                <p><strong>💰 Payment Method:</strong> {data.get('payment_method', 'Not specified').upper()}</p>
                                <p><strong>💳 Balance:</strong> {'GHS ' + str(new_balance) if new_balance > 0 else 'Fully Paid ✅'}</p>
                            </div>
                            
                            <h3 style="color: #1a1a2e; margin: 25px 0 15px; font-size: 16px;">🛒 Order Items</h3>
                            
                            <table class="items-table">
                                <thead>
                                    <tr>
                                        <th>Item</th>
                                        <th>Category</th>
                                        <th style="text-align: center;">Qty</th>
                                        <th style="text-align: right;">Price</th>
                                        <th style="text-align: right;">Total</th>
                                    </tr>
                                </thead>
                                <tbody>
                """
                
                # Build items table
                subtotal = 0.0
                has_attachments = False
                for item in order_items:
                    item_total = float(item['qty']) * float(item['price'])
                    subtotal = subtotal + item_total
                    
                    # Check if this item has an attachment
                    if existing_hold:
                        try:
                            items_list = json.loads(existing_hold.items)
                            for cart_item in items_list:
                                if cart_item.get('name') == item['name'] and cart_item.get('attachment'):
                                    has_attachments = True
                                    break
                        except:
                            pass
                    
                    html_content += f"""
                                    <tr>
                                        <td><strong>{item['name']}</strong></td>
                                        <td><span class="family-badge">{item.get('family', 'General')}</span></td>
                                        <td style="text-align: center;">{item['qty']}</td>
                                        <td style="text-align: right;">GHS {item['price']:.2f}</td>
                                        <td style="text-align: right;">GHS {item_total:.2f}</td>
                                    </tr>
                    """
                
                html_content += f"""
                                </tbody>
                            </table>
                """
                
                # Show attachment notice if any items have attachments
                if has_attachments:
                    html_content += """
                            <div class="attachment-note">
                                <strong>📎 Attachments:</strong>
                                <p style="margin: 5px 0 0 0; font-size: 13px; color: #555;">
                                    Some items in your order include file attachments. These will be reviewed by our team.
                                </p>
                                <small>Supported formats: Images, PDFs, and Documents</small>
                            </div>
                    """
                
                html_content += f"""
                            <div class="total-section">
                                <span class="total-label">Order Total</span>
                                <span class="total-amount">GHS {total:.2f}</span>
                            </div>
                            
                            <div class="payment-info">
                                <p><strong>💳 Payment Status:</strong> {'Paid in Full ✅' if new_balance <= 0 else 'Pending - Balance of GHS ' + str(new_balance)}</p>
                                <p><strong>💳 Payment Method:</strong> {data.get('payment_method', 'Not specified').upper()}</p>
                                <p><strong>📝 Note:</strong> {data.get('note', 'No special instructions')}</p>
                            </div>
                            
                            <p style="color: #555; font-size: 14px; line-height: 1.6; margin-top: 20px;">
                                💖 We truly appreciate your business! Our team is working diligently to ensure 
                                your order is prepared with the utmost care and quality. You will receive another 
                                notification when your order is ready for pickup or delivery.
                            </p>
                            
                            <p style="color: #1a1a2e; font-size: 14px; margin: 15px 0 5px; font-weight: 600;">
                                📢 Need assistance? Reach out to us!
                            </p>
                            <p style="color: #666; font-size: 13px; margin: 0;">
                                📞 Call: 0243210009 • 📧 Email: info@asempahfiegraphics.com
                            </p>
                            <p style="color: #666; font-size: 13px; margin: 5px 0;">
                                📍 Visit us: Kokomlemle, Accra (Opposite the Police Station)
                            </p>
                        </div>
                        
                        <div class="footer">
                            <div class="shop-name">✨ Asempahfie Graphics ✨</div>
                            <div class="shop-info">📍 Kokomlemle, Accra</div>
                            <div class="shop-info">📞 0243210009</div>
                            <div class="shop-info">📧 info@asempahfiegraphics.com</div>
                            <p style="margin-top: 15px; font-size: 12px; color: #aaa;">
                                © {now.year} Asempahfie Graphics. All rights reserved.
                            </p>
                            <p style="font-size: 11px; color: #bbb; margin: 5px 0 0;">
                                This is an automated confirmation. Please do not reply to this email.
                            </p>
                        </div>
                    </div>
                </body>
                </html>
                """
                
                # Send email
                from flask_mail import Message
                from flask import current_app
                
                mail = current_app.extensions.get('mail')
                if mail is None:
                    from flask_mail import Mail
                    mail = Mail(current_app)
                
                msg = Message(
                    subject=f"🎉 Order Confirmed! #{order_id} - Asempahfie Graphics",
                    recipients=[str(customer_email)],
                    html=html_content,
                    sender="afgghana@gmail.com"
                )
                
                mail.send(msg)
                print(f"✅ Order confirmation email sent to {customer_email} for order #{order_id}")
                email_sent = True
                
            except Exception as email_error:
                print(f"⚠️ Failed to send email to {customer_email}: {str(email_error)}")
                import traceback
                traceback.print_exc()
                email_sent = False
        else:
            print(f"ℹ️ No valid email provided for order #{order_id}, skipping email notification")
            email_sent = False
        
        # ===================== RETURN RESPONSE =====================
        return jsonify({
            "message": "Order held successfully",
            "id": order_id,
            "order_id": order_id,
            "balance": str(new_balance),
            "total": str(total),
            "amount_paid": str(amount_paid),
            "payment_method": data.get('payment_method', ''),
            "email_sent": email_sent,
            "customer_email": customer_email
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error in hold_order: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500





@guest.route('/create_orders_all', methods=['POST'])
@flask_praetorian.auth_required
def create_orders_all():
    try:
        us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        session = Session.query.filter_by(status="current").first()
        data = request.json

        if not data or 'cartItems' not in data or 'total' not in data:
            return jsonify({"error": "Invalid request"}), 400

        # Get cashier
        cashier = User.query.filter_by(username=data.get("cashier", "")).first()
        if not cashier:
            return jsonify({"error": "Cashier not found"}), 404

        # Get customer - handle both ID and customer_id
        customer_input = data.get("customer")
        customer_name = None
        customer_obj = None
        if customer_input:
            if str(customer_input).isdigit():
                customer_obj = Customer.query.filter_by(id=int(customer_input)).first()
            if not customer_obj:
                customer_obj = Customer.query.filter_by(customer_id=str(customer_input)).first()
            if customer_obj:
                customer_name = f"{customer_obj.firstname} {customer_obj.lastname}"

        phone = data.get("phone", "")
        items = json.dumps(data.get('cartItems', []))
        
        # Get amount paid from request
        amount_paid = float(data.get('amount_paid', 0))
        
        # ✅ Check if this is a balance payment
        is_balance_payment = data.get('is_balance_payment', False)
        balance_to_pay = float(data.get('balance_to_pay', 0))
        
        # Get held cart ID if exists
        held_cart_id = data.get("id")
        held_cart = None
        existing_balance = 0
        held_cart_total = 0
        
        # Check if this is a held order with existing balance
        if held_cart_id:
            held_cart = HeldCart.query.filter_by(id=held_cart_id).first()
            if held_cart:
                held_cart_total = float(held_cart.total) if held_cart.total else 0
                
                try:
                    existing_balance = float(held_cart.balance) if held_cart.balance else 0
                    print(f"🔍 DEBUG: existing_balance={existing_balance}")
                except (ValueError, TypeError):
                    existing_balance = 0
                
                # ✅ CORRECT BALANCE CALCULATION WITH BALANCE PAYMENT SUPPORT
                if is_balance_payment and existing_balance > 0:
                    total_amount = existing_balance
                    new_balance = existing_balance - amount_paid
                    if new_balance < 0:
                        new_balance = 0
                    balance = new_balance
                    print(f"🔍 BALANCE PAYMENT: existing_balance={existing_balance}, amount_paid={amount_paid}, new_balance={new_balance}")
                else:
                    if existing_balance > 0:
                        new_balance = existing_balance - amount_paid
                    else:
                        new_balance = held_cart_total - amount_paid
                    
                    if new_balance < 0:
                        new_balance = 0
                    
                    total_amount = held_cart_total
                    balance = new_balance
                
                print(f"🔍 DEBUG create_orders_all: held_cart_id={held_cart_id}, held_cart_total={held_cart_total}, existing_balance={existing_balance}, amount_paid={amount_paid}, new_balance={new_balance}")
            else:
                total_amount = float(data['total'])
                balance = total_amount - amount_paid
                if balance < 0:
                    balance = 0
        else:
            total_amount = float(data['total'])
            balance = total_amount - amount_paid
            if balance < 0:
                balance = 0

        # Create new order
        new_order = Order(
            user_id=us.id,
            items=items,
            total=total_amount,
            waiter=us.firstname,
            order_status="Pending",
            status="paid" if balance <= 0 else "pending",
            session=session.open_date if session else None
        )
        db.session.add(new_order)
        db.session.flush()

        # Process each cart item
        for cart_item in data['cartItems']:
            item_name = cart_item.get('name')
            item_quantity = int(cart_item.get('qty', 0))
            category = cart_item.get('category')
            family = cart_item.get('family')
            price = float(cart_item.get('price', 0))
            total_price = price * item_quantity
            
            item = Iteman.query.filter_by(name=item_name).first()
            if not item:
                db.session.rollback()
                return jsonify({"error": f"Item '{item_name}' not found"}), 404

            order_item = OrderItem(
                item_name=item_name,
                order_id=new_order.id,
                item_id=item.id,
                quantity=item_quantity,
                category=category,
                waiter=f"{us.firstname} {us.lastname}",
                status="Pending",
                created_date=datetime.now(),
                family=family,
                session=session.open_date if session else None,
                table=data.get('table', '')
            )
            db.session.add(order_item)

            if total_amount > 0:
                item_amount_paid = (amount_paid / total_amount) * total_price
            else:
                item_amount_paid = 0

            pos_payment = PosPayment(
                name=item_name,
                amount=item_amount_paid,
                method=data.get("method", "Cash"),
                quantity=item_quantity,
                attendant=f"{us.firstname} {us.lastname}",
                created_by_id=us.id,
                cashier=f"{cashier.firstname} {cashier.lastname}",
                payment_date=datetime.now(),
                session=session.open_date if session else None,
                category=family,
                cat=category,
                customer=customer_name,
                phone=phone
            )
            db.session.add(pos_payment)

            income = Income(
                name=item_name,
                amount=item_amount_paid,
                date=datetime.now(),
                note="Pos Payment" + (" (Pending)" if balance > 0 else ""),
                created_date=datetime.now(),
                created_by_id=us.id,
                cashier=f"{cashier.firstname} {cashier.lastname}",
                session=session.open_date if session else None,
                method=data.get("method", "Cash"),
                category=family,
                cat=category,
                customer=customer_name,
                phone=phone
            )
            db.session.add(income)

        # ✅ UPDATE ALL pending held carts for this user
        held_carts = HeldCart.query.filter_by(user_id=us.id, paid_status="Pending").all()
        for held_cart in held_carts:
            if balance <= 0:
                held_cart.status = "Confirmed"
                held_cart.paid_status = "Success"
                held_cart.balance = "0"
                print(f"✅ Held cart {held_cart.id} marked as SUCCESS (balance: {balance})")
            else:
                held_cart.status = "Pending"
                held_cart.paid_status = "Pending"
                held_cart.balance = str(balance)
                print(f"⏳ Held cart {held_cart.id} marked as PENDING (balance: {balance})")
            
            if customer_obj:
                held_cart.customer = customer_name

        db.session.commit()

        return jsonify({
            "id": new_order.id,
            "company_name": new_order.company_name,
            "created_at": new_order.created_at.strftime('%Y-%m-%d %H:%M:%S') if new_order.created_at else None,
            "items": items,
            "order_status": new_order.order_status,
            "total": total_amount,
            "balance": balance,
            "amount_paid": amount_paid,
            "existing_balance": existing_balance,
            "held_cart_total": held_cart_total,
            "user_id": new_order.user_id,
            "waiter": new_order.waiter,
            "is_balance_payment": is_balance_payment
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error in create_orders_all: {str(e)}")
        return jsonify({"error": str(e)}), 500


@guest.route('/create_orders_two', methods=['POST'])
@flask_praetorian.auth_required
def create_orders_two():
    try:
        us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        session = Session.query.filter_by(status="current").first()
        data = request.json

        if not data or 'cartItems' not in data or 'total' not in data:
            return jsonify({"error": "Invalid request"}), 400

        # Get cashier
        cashier = User.query.filter_by(username=data.get("cashier", "")).first()
        if not cashier:
            return jsonify({"error": "Cashier not found"}), 404

        # Get customer - handle both ID and customer_id
        customer_input = data.get("customer")
        customer_name = None
        customer_obj = None
        if customer_input:
            if str(customer_input).isdigit():
                customer_obj = Customer.query.filter_by(id=int(customer_input)).first()
            if not customer_obj:
                customer_obj = Customer.query.filter_by(customer_id=str(customer_input)).first()
            if customer_obj:
                customer_name = f"{customer_obj.firstname} {customer_obj.lastname}"

        phone = data.get("phone", "")
        items = json.dumps(data.get('cartItems', []))
        
        # Get amount paid from request
        amount_paid = float(data.get('amount_paid', 0))
        
        # ✅ Check if this is a balance payment
        is_balance_payment = data.get('is_balance_payment', False)
        balance_to_pay = float(data.get('balance_to_pay', 0))
        
        # Get held cart ID if exists
        held_cart_id = data.get("id")
        held_cart = None
        existing_balance = 0
        held_cart_total = 0
        
        # Check if this is a held order with existing balance
        if held_cart_id:
            held_cart = HeldCart.query.filter_by(id=held_cart_id).first()
            if held_cart:
                held_cart_total = float(held_cart.total) if held_cart.total else 0
                
                try:
                    existing_balance = float(held_cart.balance) if held_cart.balance else 0
                    print(f"🔍 DEBUG: existing_balance={existing_balance}")
                except (ValueError, TypeError):
                    existing_balance = 0
                
                # ✅ CORRECT BALANCE CALCULATION WITH BALANCE PAYMENT SUPPORT
                if is_balance_payment and existing_balance > 0:
                    total_amount = existing_balance
                    new_balance = existing_balance - amount_paid
                    if new_balance < 0:
                        new_balance = 0
                    balance = new_balance
                    print(f"🔍 BALANCE PAYMENT: existing_balance={existing_balance}, amount_paid={amount_paid}, new_balance={new_balance}")
                else:
                    if existing_balance > 0:
                        new_balance = existing_balance - amount_paid
                    else:
                        new_balance = held_cart_total - amount_paid
                    
                    if new_balance < 0:
                        new_balance = 0
                    
                    total_amount = held_cart_total
                    balance = new_balance
                
                print(f"🔍 DEBUG create_orders_two: held_cart_id={held_cart_id}, held_cart_total={held_cart_total}, existing_balance={existing_balance}, amount_paid={amount_paid}, new_balance={new_balance}")
            else:
                total_amount = float(data['total'])
                balance = total_amount - amount_paid
                if balance < 0:
                    balance = 0
        else:
            total_amount = float(data['total'])
            balance = total_amount - amount_paid
            if balance < 0:
                balance = 0

        # Create new order
        new_order = Order(
            user_id=us.id,
            items=items,
            total=total_amount,
            waiter=us.firstname,
            order_status="Pending",
            status="paid" if balance <= 0 else "pending",
            session=session.open_date if session else None
        )
        db.session.add(new_order)
        db.session.flush()

        # Process each cart item
        for cart_item in data['cartItems']:
            item_name = cart_item.get('name')
            item_quantity = int(cart_item.get('qty', 0))
            category = cart_item.get('category')
            family = cart_item.get('family')
            price = float(cart_item.get('price', 0))
            total_price = price * item_quantity
            
            item = Iteman.query.filter_by(name=item_name).first()
            if not item:
                db.session.rollback()
                return jsonify({"error": f"Item '{item_name}' not found"}), 404

            order_item = OrderItem(
                item_name=item_name,
                order_id=new_order.id,
                item_id=item.id,
                quantity=item_quantity,
                category=category,
                waiter=f"{us.firstname} {us.lastname}",
                status="Pending",
                table=data.get('table', ''),
                created_date=datetime.now(),
                family=family,
                session=session.open_date if session else None
            )
            db.session.add(order_item)

            if total_amount > 0:
                item_amount_paid = (amount_paid / total_amount) * total_price
            else:
                item_amount_paid = 0

            pos_payment = PosPayment(
                name=item_name,
                amount=item_amount_paid,
                method=data.get("method", "Cash"),
                quantity=item_quantity,
                attendant=f"{us.firstname} {us.lastname}",
                created_by_id=us.id,
                cashier=f"{cashier.firstname} {cashier.lastname}",
                payment_date=datetime.now(),
                session=session.open_date if session else None,
                category=family,
                cat=category,
                customer=customer_name,
                phone=phone
            )
            db.session.add(pos_payment)

            income = Income(
                name=item_name,
                attendant=f"{us.firstname} {us.lastname}",
                amount=item_amount_paid,
                date=datetime.now(),
                discount=data.get("discount", 0),
                note="Pos Payment" + (" (Pending)" if balance > 0 else ""),
                created_date=datetime.now(),
                created_by_id=us.id,
                cashier=f"{cashier.firstname} {cashier.lastname}",
                session=session.open_date if session else None,
                method=data.get("method", "Cash"),
                category=family,
                cat=category,
                customer=customer_name,
                phone=phone
            )
            db.session.add(income)

        # ✅ UPDATE HELD CART - FIXED STATUS LOGIC
        if held_cart_id and held_cart:
            # ✅ Debug: Log before update
            print(f"🔍 BEFORE UPDATE create_orders_two: held_cart_id={held_cart_id}, balance={balance}, current_status={held_cart.status}, current_paid_status={held_cart.paid_status}")
            
            if balance <= 0:
                held_cart.status = "Confirmed"
                held_cart.paid_status = "Success"
                held_cart.balance = "0"
                print(f"✅ Held cart {held_cart_id} marked as SUCCESS (balance: {balance})")
            else:
                held_cart.status = "Pending"
                held_cart.paid_status = "Pending"
                held_cart.balance = str(balance)
                print(f"⏳ Held cart {held_cart_id} marked as PENDING (balance: {balance})")
            
            # ✅ Debug: Log after update
            print(f"🔍 AFTER UPDATE create_orders_two: held_cart_id={held_cart_id}, status={held_cart.status}, paid_status={held_cart.paid_status}, balance={held_cart.balance}")
            
            if customer_obj:
                held_cart.customer = customer_name
            
            if data.get('note'):
                held_cart.note = data.get('note')
            
            if data.get('table'):
                held_cart.table = data.get('table')

        db.session.commit()

        return jsonify({
            "id": new_order.id,
            "company_name": new_order.company_name,
            "created_at": new_order.created_at.strftime('%Y-%m-%d %H:%M:%S') if new_order.created_at else None,
            "items": items,
            "order_status": new_order.order_status,
            "total": total_amount,
            "balance": balance,
            "amount_paid": amount_paid,
            "existing_balance": existing_balance,
            "held_cart_total": held_cart_total,
            "user_id": new_order.user_id,
            "waiter": new_order.waiter,
            "held_cart_status": held_cart.status if held_cart else None,
            "held_cart_paid_status": held_cart.paid_status if held_cart else None,
            "is_balance_payment": is_balance_payment
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error in create_orders_two: {str(e)}")
        return jsonify({"error": str(e)}), 500


@guest.route('/create_orders_two_all', methods=['POST'])
@flask_praetorian.auth_required
def create_orders_two_all():
    try:
        us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        session = Session.query.filter_by(status="current").first()
        data = request.json

        if not data or 'cartItems' not in data or 'total' not in data:
            return jsonify({"error": "Invalid request"}), 400

        # Get cashier
        cashier = User.query.filter_by(username=data.get("cashier", "")).first()
        if not cashier:
            return jsonify({"error": "Cashier not found"}), 404

        # Get customer - handle both ID and customer_id
        customer_input = data.get("customer")
        customer_name = None
        customer_obj = None
        if customer_input:
            if str(customer_input).isdigit():
                customer_obj = Customer.query.filter_by(id=int(customer_input)).first()
            if not customer_obj:
                customer_obj = Customer.query.filter_by(customer_id=str(customer_input)).first()
            if customer_obj:
                customer_name = f"{customer_obj.firstname} {customer_obj.lastname}"

        phone = data.get("phone", "")
        items = json.dumps(data.get('cartItems', []))
        
        # Get amount paid from request
        amount_paid = float(data.get('amount_paid', 0))
        
        # ✅ Check if this is a balance payment
        is_balance_payment = data.get('is_balance_payment', False)
        balance_to_pay = float(data.get('balance_to_pay', 0))
        
        # Get held cart ID if exists
        held_cart_id = data.get("id")
        held_cart = None
        existing_balance = 0
        held_cart_total = 0
        
        # Check if this is a held order with existing balance
        if held_cart_id:
            held_cart = HeldCart.query.filter_by(id=held_cart_id).first()
            if held_cart:
                held_cart_total = float(held_cart.total) if held_cart.total else 0
                
                try:
                    existing_balance = float(held_cart.balance) if held_cart.balance else 0
                    print(f"🔍 DEBUG: existing_balance={existing_balance}")
                except (ValueError, TypeError):
                    existing_balance = 0
                
                # ✅ CORRECT BALANCE CALCULATION WITH BALANCE PAYMENT SUPPORT
                if is_balance_payment and existing_balance > 0:
                    total_amount = existing_balance
                    new_balance = existing_balance - amount_paid
                    if new_balance < 0:
                        new_balance = 0
                    balance = new_balance
                    print(f"🔍 BALANCE PAYMENT: existing_balance={existing_balance}, amount_paid={amount_paid}, new_balance={new_balance}")
                else:
                    if existing_balance > 0:
                        new_balance = existing_balance - amount_paid
                    else:
                        new_balance = held_cart_total - amount_paid
                    
                    if new_balance < 0:
                        new_balance = 0
                    
                    total_amount = held_cart_total
                    balance = new_balance
                
                print(f"🔍 DEBUG create_orders_two_all: held_cart_id={held_cart_id}, held_cart_total={held_cart_total}, existing_balance={existing_balance}, amount_paid={amount_paid}, new_balance={new_balance}")
            else:
                total_amount = float(data['total'])
                balance = total_amount - amount_paid
                if balance < 0:
                    balance = 0
        else:
            total_amount = float(data['total'])
            balance = total_amount - amount_paid
            if balance < 0:
                balance = 0

        # Create new order
        new_order = Order(
            user_id=us.id,
            items=items,
            total=total_amount,
            waiter=us.firstname,
            order_status="Pending",
            status="paid" if balance <= 0 else "pending",
            session=session.open_date if session else None
        )
        db.session.add(new_order)
        db.session.flush()

        # Process each cart item
        for cart_item in data['cartItems']:
            item_name = cart_item.get('name')
            item_quantity = int(cart_item.get('qty', 0))
            category = cart_item.get('category')
            family = cart_item.get('family')
            price = float(cart_item.get('price', 0))
            total_price = price * item_quantity
            
            item = Iteman.query.filter_by(name=item_name).first()
            if not item:
                db.session.rollback()
                return jsonify({"error": f"Item '{item_name}' not found"}), 404

            order_item = OrderItem(
                item_name=item_name,
                order_id=new_order.id,
                item_id=item.id,
                quantity=item_quantity,
                category=category,
                waiter=f"{us.firstname} {us.lastname}",
                status="Pending",
                created_date=datetime.now(),
                family=family,
                session=session.open_date if session else None,
                table=data.get('table', '')
            )
            db.session.add(order_item)

            if total_amount > 0:
                item_amount_paid = (amount_paid / total_amount) * total_price
            else:
                item_amount_paid = 0

            pos_payment = PosPayment(
                name=item_name,
                amount=item_amount_paid,
                method=data.get("method", "Cash"),
                quantity=item_quantity,
                attendant=f"{us.firstname} {us.lastname}",
                created_by_id=us.id,
                cashier=f"{cashier.firstname} {cashier.lastname}",
                payment_date=datetime.now(),
                session=session.open_date if session else None,
                category=family,
                cat=category,
                customer=customer_name,
                phone=phone
            )
            db.session.add(pos_payment)

            income = Income(
                name=item_name,
                amount=item_amount_paid,
                date=datetime.now(),
                note="Pos Payment" + (" (Pending)" if balance > 0 else ""),
                created_date=datetime.now(),
                created_by_id=us.id,
                cashier=f"{cashier.firstname} {cashier.lastname}",
                session=session.open_date if session else None,
                method=data.get("method", "Cash"),
                category=family,
                cat=category,
                customer=customer_name,
                phone=phone
            )
            db.session.add(income)

        # ✅ UPDATE ALL pending held carts for this user
        held_carts = HeldCart.query.filter_by(user_id=us.id, paid_status="Pending").all()
        for held_cart in held_carts:
            if balance <= 0:
                held_cart.status = "Confirmed"
                held_cart.paid_status = "Success"
                held_cart.balance = "0"
                print(f"✅ Held cart {held_cart.id} marked as SUCCESS (balance: {balance})")
            else:
                held_cart.status = "Pending"
                held_cart.paid_status = "Pending"
                held_cart.balance = str(balance)
                print(f"⏳ Held cart {held_cart.id} marked as PENDING (balance: {balance})")
            
            if customer_obj:
                held_cart.customer = customer_name

        db.session.commit()

        return jsonify({
            "id": new_order.id,
            "company_name": new_order.company_name,
            "created_at": new_order.created_at.strftime('%Y-%m-%d %H:%M:%S') if new_order.created_at else None,
            "items": items,
            "order_status": new_order.order_status,
            "total": total_amount,
            "balance": balance,
            "amount_paid": amount_paid,
            "existing_balance": existing_balance,
            "held_cart_total": held_cart_total,
            "user_id": new_order.user_id,
            "waiter": new_order.waiter,
            "is_balance_payment": is_balance_payment
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error in create_orders_two_all: {str(e)}")
        return jsonify({"error": str(e)}), 500


# ===================== CREDIT PAYMENT =====================

@guest.route('/credit', methods=['POST'])
@flask_praetorian.auth_required
def credit():
    try:
        us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        session = Session.query.filter_by(status="current").first()
        data = request.json

        if not data or 'cartItems' not in data or 'total' not in data:
            return jsonify({"error": "Invalid request"}), 400

        # Get cashier
        cashier = User.query.filter_by(username=data.get("cashier", "")).first()
        if not cashier:
            return jsonify({"error": "Cashier not found"}), 404

        # Get customer - handle both ID and customer_id
        customer_input = data.get("customer")
        customer_name = None
        customer_obj = None
        if customer_input:
            if str(customer_input).isdigit():
                customer_obj = Customer.query.filter_by(id=int(customer_input)).first()
            if not customer_obj:
                customer_obj = Customer.query.filter_by(customer_id=str(customer_input)).first()
            if customer_obj:
                customer_name = f"{customer_obj.firstname} {customer_obj.lastname}"

        phone = data.get("phone", "")
        items = json.dumps(data.get('cartItems', []))
        
        # Get amount paid from request
        amount_paid = float(data.get('amount_paid', 0))
        
        # ✅ Check if this is a balance payment
        is_balance_payment = data.get('is_balance_payment', False)
        balance_to_pay = float(data.get('balance_to_pay', 0))
        
        # Get held cart ID if exists
        held_cart_id = data.get("id")
        held_cart = None
        existing_balance = 0
        held_cart_total = 0
        
        # Check if this is a held order with existing balance
        if held_cart_id:
            held_cart = HeldCart.query.filter_by(id=held_cart_id).first()
            if held_cart:
                held_cart_total = float(held_cart.total) if held_cart.total else 0
                
                try:
                    existing_balance = float(held_cart.balance) if held_cart.balance else 0
                    print(f"🔍 DEBUG: existing_balance={existing_balance}")
                except (ValueError, TypeError):
                    existing_balance = 0
                
                # ✅ CORRECT BALANCE CALCULATION WITH BALANCE PAYMENT SUPPORT
                if is_balance_payment and existing_balance > 0:
                    total_amount = existing_balance
                    new_balance = existing_balance - amount_paid
                    if new_balance < 0:
                        new_balance = 0
                    balance = new_balance
                    print(f"🔍 BALANCE PAYMENT: existing_balance={existing_balance}, amount_paid={amount_paid}, new_balance={new_balance}")
                else:
                    if existing_balance > 0:
                        new_balance = existing_balance - amount_paid
                    else:
                        new_balance = held_cart_total - amount_paid
                    
                    if new_balance < 0:
                        new_balance = 0
                    
                    total_amount = held_cart_total
                    balance = new_balance
                
                print(f"🔍 DEBUG credit: held_cart_id={held_cart_id}, held_cart_total={held_cart_total}, existing_balance={existing_balance}, amount_paid={amount_paid}, new_balance={new_balance}")
            else:
                total_amount = float(data['total'])
                balance = total_amount - amount_paid
                if balance < 0:
                    balance = 0
        else:
            total_amount = float(data['total'])
            balance = total_amount - amount_paid
            if balance < 0:
                balance = 0

        # Create new order
        new_order = Order(
            user_id=us.id,
            items=items,
            total=total_amount,
            waiter=us.firstname,
            order_status="Pending",
            status="paid" if balance <= 0 else "pending",
            session=session.open_date if session else None
        )
        db.session.add(new_order)
        db.session.flush()

        # Create credit record
        credit = Credit(
            user_id=us.id,
            items=items,
            total=total_amount,
            waiter=us.firstname,
            order_status="Success",
            status="credit" if balance <= 0 else "pending_credit",
            customer=customer_name,
            phone=phone,
            session=session.open_date if session else None,
            balance=str(balance) if balance > 0 else "0"
        )
        db.session.add(credit)

        # Process each cart item
        for cart_item in data['cartItems']:
            item_name = cart_item.get('name')
            item_quantity = int(cart_item.get('qty', 0))
            category = cart_item.get('category')
            family = cart_item.get('family')
            price = float(cart_item.get('price', 0))
            total_price = price * item_quantity
            
            item = Iteman.query.filter_by(name=item_name).first()
            if not item:
                db.session.rollback()
                return jsonify({"error": f"Item '{item_name}' not found"}), 404

            order_item = OrderItem(
                item_name=item_name,
                order_id=new_order.id,
                item_id=item.id,
                quantity=item_quantity,
                category=category,
                waiter=f"{us.firstname} {us.lastname}",
                status="Pending",
                created_date=datetime.now(),
                family=family,
                session=session.open_date if session else None,
                table=data.get('table', '')
            )
            db.session.add(order_item)

            if total_amount > 0:
                item_amount_paid = (amount_paid / total_amount) * total_price
            else:
                item_amount_paid = 0

            pos_payment = PosPayment(
                name=item_name,
                amount=item_amount_paid,
                method="Credit" + (" (Pending)" if balance > 0 else ""),
                quantity=item_quantity,
                attendant=f"{us.firstname} {us.lastname}",
                created_by_id=us.id,
                cashier=f"{cashier.firstname} {cashier.lastname}",
                payment_date=datetime.now(),
                session=session.open_date if session else None,
                category=family,
                cat=category,
                customer=customer_name,
                phone=phone
            )
            db.session.add(pos_payment)

        # ✅ UPDATE HELD CART - FIXED STATUS LOGIC
        if held_cart_id and held_cart:
            if balance <= 0:
                held_cart.status = "Confirmed"
                held_cart.paid_status = "Success"
                held_cart.balance = "0"
                print(f"✅ Credit held cart {held_cart_id} marked as SUCCESS (balance: {balance})")
            else:
                held_cart.status = "Pending"
                held_cart.paid_status = "Pending"
                held_cart.balance = str(balance)
                print(f"⏳ Credit held cart {held_cart_id} marked as PENDING (balance: {balance})")
            
            if customer_obj:
                held_cart.customer = customer_name

        db.session.commit()

        return jsonify({
            "id": new_order.id,
            "company_name": new_order.company_name,
            "created_at": new_order.created_at.strftime('%Y-%m-%d %H:%M:%S') if new_order.created_at else None,
            "items": items,
            "order_status": new_order.order_status,
            "total": total_amount,
            "balance": balance,
            "amount_paid": amount_paid,
            "existing_balance": existing_balance,
            "held_cart_total": held_cart_total,
            "user_id": new_order.user_id,
            "waiter": new_order.waiter,
            "held_cart_status": held_cart.status if held_cart else None,
            "held_cart_paid_status": held_cart.paid_status if held_cart else None,
            "is_balance_payment": is_balance_payment
        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error in credit: {str(e)}")
        return jsonify({"error": str(e)}), 500
@guest.route('/held_orders', methods=['GET'])
@flask_praetorian.auth_required
def get_held_orders():
    try:
        user_id = flask_praetorian.current_user().id
        
        # Get all pending held orders with balance
        held_orders = HeldCart.query.filter(
            HeldCart.user_id == user_id
        ).filter(
            or_(HeldCart.paid_status == "Partial", HeldCart.paid_status == "Pending")
        ).all()
        
        # Format response with balance information
        result = []
        for order in held_orders:
            try:
                items = json.loads(order.items) if order.items else []
            except:
                items = []
            
            # Calculate balance if not set
            balance = order.balance
            if balance is None or balance == "":
                balance = "0"
            
            result.append({
                "id": order.id,
                "items": items,
                "total": float(order.total),
                "balance": float(balance),
                "has_balance": float(balance) > 0,
                "customer": order.customer or "Walk-in",
                "waiter": order.waiter,
                "table": order.table,
                "note": order.note,
                "status": order.status,
                "paid_status": order.paid_status,
                "created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else None,
                "contain_food": order.contain_food == "yes",
                "contain_drink": order.contain_drink == "yes",
                "contain_digital_printing": order.contain_digital_printing == "yes",
                "contain_large_format": order.contain_large_format == "yes",
                "contain_label": order.contain_label == "yes",
                "contain_dtf": order.contain_dtf == "yes",
                "delivery_status": order.delivery_status
            })
        
        return jsonify({
            "success": True,
            "count": len(result),
            "orders": result
        }), 200
        
    except Exception as e:
        print(f"Error in get_held_orders: {str(e)}")
        return jsonify({"error": str(e)}), 500
from flask import jsonify, request
import json
from flask_praetorian import auth_required, current_user

@guest.route('/get_helding_orders', methods=['GET'])
@flask_praetorian.auth_required
def get_helding_orders():
    user = flask_praetorian.current_user()
    us = User.query.filter_by(id=user.id).first()

    if not us:
        return jsonify({"error": "User not found"}), 404

    # Query for held orders that contain food and have unconfirmed food
    held_orders = HeldCart.query.filter_by(
        
        contain_digital_printing="yes",  # Only orders with food
         # Only unconfirmed food orders
    ).all()

    orders_list = []

    for order in held_orders:
        try:
            items = json.loads(order.items)  # Convert JSON string to list
            print(f"Order {order.id} items:", items)  # Debugging

            # Filter items by "food" family and unconfirmed status
            filtered_items = [item for item in items if item.get("family") == "digital_printing" and item.get("confirmed") == False]  
            print(f"Filtered items for order {order.id}:", filtered_items)  # Debugging

            if filtered_items:  # Only include orders with unconfirmed food items
                orders_list.append({
                    "id": order.id,
                    "items": filtered_items,
                    "total": order.total,
                    "balance":order.balance,
                    "note": order.note,
                    "waiter": order.waiter,
                    "company_name": order.company_name,
                    "status": order.status,
                    "digital_printing_status": order.contain_digital_printing,
                    "working_on": order.working_on,
                    "working_on_id": order.working_on_id,
                    "working_on_label": order.working_on_label,
                    "working_on_id_label": order.working_on_id_label,
                    "working_on_large_format": order.working_on_large_format,
                    "working_on_id_large_format": order.working_on_id_large_format,
                    "working_on_dtf": order.working_on_dtf,
                    "working_on_id_dtf": order.working_on_id_dtf,
                    "working_on_digital_printing": order.working_on_digital_printing,
                    "working_on_id_digital_printing": order.working_on_id_digital_printing,
                    "customer":order.customer,

                    "created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format the datetime
                })

        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decodings JSON for order {order.id}: {e}")  # Debugging

    return jsonify(orders_list), 200




@guest.route('/get_helding_ordersa', methods=['GET'])
@flask_praetorian.auth_required
def get_helding_ordersa():
    user = flask_praetorian.current_user()
    us = User.query.filter_by(id=user.id).first()

    if not us:
        return jsonify({"error": "User not found"}), 404

    # Query for held orders that contain food and have unconfirmed food
    held_orders = HeldCart.query.filter_by(
        
        contain_digital_printing="yes",  # Only orders with food
         # Only unconfirmed food orders
    ).all()

    orders_list = []

    for order in held_orders:
        try:
            items = json.loads(order.items)  # Convert JSON string to list
            print(f"Order {order.id} items:", items)  # Debugging

            # Filter items by "food" family and unconfirmed status
            filtered_items = [item for item in items if item.get("family") == "digital_printing" and (item.get("confirmed") == True or item.get("confirmed") in [
                    "ready for pickup",
                    "delivered",
                    "printed","in_delivery"
                ])]  
            print(f"Filtered items for order {order.id}:", filtered_items)  # Debugging

            if filtered_items:  # Only include orders with unconfirmed food items
                orders_list.append({
                   "id": order.id,
                                       "items": filtered_items,
                                       "total": order.total,
                                       "balance":order.balance,
                                       "created_at":order.created_at,
                                       "note": order.note,
                                       "waiter": order.waiter,
                                       "company_name": order.company_name,
                                       "status": order.status,
                                       "digital_printing_status": order.contain_digital_printing,
                                       "working_on": order.working_on,
                                       "working_on_id": order.working_on_id,
                                       "working_on_label": order.working_on_label,
                                       "working_on_id_label": order.working_on_id_label,
                                       "working_on_large_format": order.working_on_large_format,
                                       "working_on_id_large_format": order.working_on_id_large_format,
                                       "working_on_dtf": order.working_on_dtf,
                                       "working_on_id_dtf": order.working_on_id_dtf,
                                       "working_on_digital_printing": order.working_on_digital_printing,
                                        "customer":order.customer,
                                       "working_on_id_digital_printing": order.working_on_id_digital_printing, # Format the datetime
                })

        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON for orders {order.id}: {e}")  # Debugging

    return jsonify(orders_list), 200

@guest.route('/get_helding_orders_drinks', methods=['GET'])
@flask_praetorian.auth_required
def get_helding_orders_drinks():
    user = flask_praetorian.current_user()
    us = User.query.filter_by(id=user.id).first()

    if not us:
        return jsonify({"error": "User not found"}), 404

    # Adjusting the query to get only held orders containing drinks and with unconfirmed drinks
    held_orders = HeldCart.query.filter_by(
    
    ).filter(
        HeldCart.contain_large_format == "yes",  # Orders with drinks
      # Unconfirmed drinks
    ).all()

    orders_list = []

    for order in held_orders:
        try:
            print(f"Raw items JSON for order {order.id}:", order.items)  # Debug
            items = json.loads(order.items)

            # Filter items to include only drinks
            filtered_items = [item for item in items if item.get("family") == "large_format" and item.get("confirmed") == False]
            print(f"Filtered items for order {order.id}:", filtered_items)

            if filtered_items:
                orders_list.append({
                   "id": order.id,
                                       "items": filtered_items,
                                       "total": order.total,
                                       "balance":order.balance,
                                       "note": order.note,
                                       "waiter": order.waiter,
                                       "company_name": order.company_name,
                                       "status": order.status,
                                       "large_format_status": order.contain_large_format,
                                       "working_on": order.working_on,
                                       "working_on_id": order.working_on_id,
                                       "working_on_label": order.working_on_label,
                                       "working_on_id_label": order.working_on_id_label,
                                       "working_on_large_format": order.working_on_large_format,
                                       "working_on_id_large_format": order.working_on_id_large_format,
                                       "working_on_dtf": order.working_on_dtf,
                                       "working_on_id_dtf": order.working_on_id_dtf,
                                       "working_on_digital_printing": order.working_on_digital_printing,
                                       "working_on_id_digital_printing": order.working_on_id_digital_printing,
                                        "customer":order.customer,
                                        "created_at":order.created_at

                })

        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON for order {order.id}: {e}")

    return jsonify(orders_list), 200






@guest.route('/get_helding_orders_processed_drinks', methods=['GET'])
@flask_praetorian.auth_required
def get_helding_orders_processed_drinks():
    user = flask_praetorian.current_user()
    us = User.query.filter_by(id=user.id).first()

    if not us:
        return jsonify({"error": "User not found"}), 404

    # Adjusting the query to get only held orders containing drinks and with unconfirmed drinks
    held_orders = HeldCart.query.filter_by(
    
    ).filter(
        HeldCart.contain_large_format == "yes",  # Orders with drinks
      # Unconfirmed drinks
    ).all()

    orders_list = []

    for order in held_orders:
        try:
            print(f"Raw items JSON for order {order.id}:", order.items)  # Debug
            items = json.loads(order.items)

            # Filter items to include only drinks
            filtered_items = [item for item in items if item.get("family") == "large_format" and item.get("confirmed") == True or item.get("confirmed") in [
                    "ready for pickup", "delivered", "printed","in_delivery"
                ]]
            print(f"Filtered items for order {order.id}:", filtered_items)

            if filtered_items:
                orders_list.append({
                    "id": order.id,
                                        "items": filtered_items,
                                        "total": order.total,
                                        "balance":order.balance,
                                        "note": order.note,
                                        "waiter": order.waiter,
                                        "company_name": order.company_name,
                                        "status": order.status,
                                        "large_format_status": order.contain_large_format,
                                        "working_on": order.working_on,
                                        "working_on_id": order.working_on_id,
                                        "working_on_label": order.working_on_label,
                                        "working_on_id_label": order.working_on_id_label,
                                        "working_on_large_format": order.working_on_large_format,
                                        "working_on_id_large_format": order.working_on_id_large_format,
                                        "working_on_dtf": order.working_on_dtf,
                                        "working_on_id_dtf": order.working_on_id_dtf,
                                        "working_on_digital_printing": order.working_on_digital_printing,
                                        "working_on_id_digital_printing": order.working_on_id_digital_printing,
                                        "customer": order.customer,
                                        "created_at":order.created_at,
                                })

        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON for order {order.id}: {e}")

    return jsonify(orders_list), 200




    

@guest.route('/get_helding_orders_label', methods=['GET'])
@flask_praetorian.auth_required
def get_helding_orders_label():
    user = flask_praetorian.current_user()
    us = User.query.filter_by(id=user.id).first()

    if not us:
        return jsonify({"error": "User not found"}), 404

    # Adjusting the query to get only held orders containing drinks and with unconfirmed drinks
    held_orders = HeldCart.query.filter_by(
    
    ).filter(
        HeldCart.contain_label == "yes",  # Orders with drinks
      # Unconfirmed drinks
    ).all()

    orders_list = []

    for order in held_orders:
        try:
            print(f"Raw items JSON for order {order.id}:", order.items)  # Debug
            items = json.loads(order.items)

            # Filter items to include only drinks
            filtered_items = [item for item in items if item.get("family") == "label" and item.get("confirmed") == False]
            print(f"Filtered items for order {order.id}:", filtered_items)

            if filtered_items:
                orders_list.append({
                    "id": order.id,
                                        "items": filtered_items,
                                        "total": order.total,
                                        "balance":order.balance,
                                        "note": order.note,
                                        "waiter": order.waiter,
                                        "company_name": order.company_name,
                                        "status": order.status,
                                        "label_status": order.contain_label,
                                        "working_on": order.working_on,
                                        "working_on_id": order.working_on_id,
                                        "working_on_label": order.working_on_label,
                                        "working_on_id_label": order.working_on_id_label,
                                        "working_on_large_format": order.working_on_large_format,
                                        "working_on_id_large_format": order.working_on_id_large_format,
                                        "working_on_dtf": order.working_on_dtf,
                                        "working_on_id_dtf": order.working_on_id_dtf,
                                        "working_on_digital_printing": order.working_on_digital_printing,
                                        "working_on_id_digital_printing": order.working_on_id_digital_printing,
                                         "customer":order.customer
                })

        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON for order {order.id}: {e}")

    return jsonify(orders_list), 200





@guest.route('/get_helding_orders_label_processed', methods=['GET'])
@flask_praetorian.auth_required
def get_helding_orders_label_processed():
    user = flask_praetorian.current_user()
    us = User.query.filter_by(id=user.id).first()

    if not us:
        return jsonify({"error": "User not found"}), 404

    # Adjusting the query to get only held orders containing drinks and with unconfirmed drinks
    held_orders = HeldCart.query.filter_by(
    
    ).filter(
        HeldCart.contain_label == "yes",  # Orders with drinks
      # Unconfirmed drinks
    ).all()

    orders_list = []

    for order in held_orders:
        try:
            print(f"Raw items JSON for order {order.id}:", order.items)  # Debug
            items = json.loads(order.items)

            # Filter items to include only drinks
            filtered_items = [item for item in items if item.get("family") == "label" and item.get("confirmed") == True or item.get("confirmed") in [
                    "ready for pickup", "delivered", "printed","in_delivery"]]
            print(f"Filtered items for order {order.id}:", filtered_items)

            if filtered_items:
                orders_list.append({
                   "id": order.id,
                                       "items": filtered_items,
                                       "total": order.total,
                                       "balance":order.balance,
                                       "note": order.note,
                                       "waiter": order.waiter,
                                       "company_name": order.company_name,
                                       "status": order.status,
                                       "label_status": order.contain_label,
                                       "working_on": order.working_on,
                                       "working_on_id": order.working_on_id,
                                       "working_on_label": order.working_on_label,
                                       "working_on_id_label": order.working_on_id_label,
                                       "working_on_large_format": order.working_on_large_format,
                                       "working_on_id_large_format": order.working_on_id_large_format,
                                       "working_on_dtf": order.working_on_dtf,
                                       "working_on_id_dtf": order.working_on_id_dtf,
                                       "working_on_digital_printing": order.working_on_digital_printing,
                                       "working_on_id_digital_printing": order.working_on_id_digital_printing,  # Format the datetime
                                        "customer":order.customer,
                                           "created_at":order.created_at
                })

        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON for order {order.id}: {e}")

    return jsonify(orders_list), 200

   

@guest.route('/get_helding_orders_dtf', methods=['GET'])
@flask_praetorian.auth_required
def get_helding_orders_dtf():
    user = flask_praetorian.current_user()
    us = User.query.filter_by(id=user.id).first()

    if not us:
        return jsonify({"error": "User not found"}), 404

    # Adjusting the query to get only held orders containing drinks and with unconfirmed drinks
    held_orders = HeldCart.query.filter_by(
    
    ).filter(
        HeldCart.contain_dtf == "yes",  # Orders with drinks
      # Unconfirmed drinks
    ).all()

    orders_list = []

    for order in held_orders:
        try:
            print(f"Raw items JSON for order {order.id}:", order.items)  # Debug
            items = json.loads(order.items)

            # Filter items to include only drinks
            filtered_items = [item for item in items if item.get("family") == "dtf" and item.get("confirmed") == False]
            print(f"Filtered items for order {order.id}:", filtered_items)

            if filtered_items:
                orders_list.append({
                    "id": order.id,
                                        "items": filtered_items,
                                        "total": order.total,
                                        "balance":order.balance,
                                        "note": order.note,
                                        "waiter": order.waiter,
                                        "company_name": order.company_name,
                                        "status": order.status,
                                        "dtf_status": order.contain_dtf,
                                        "working_on": order.working_on,
                                        "working_on_id": order.working_on_id,
                                        "working_on_label": order.working_on_label,
                                        "working_on_id_label": order.working_on_id_label,
                                        "working_on_large_format": order.working_on_large_format,
                                        "working_on_id_large_format": order.working_on_id_large_format,
                                        "working_on_dtf": order.working_on_dtf,
                                        "working_on_id_dtf": order.working_on_id_dtf,
                                        "working_on_digital_printing": order.working_on_digital_printing,
                                        "working_on_id_digital_printing": order.working_on_id_digital_printing,
                                         "customer":order.customer,
                })

        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON for order {order.id}: {e}")

    return jsonify(orders_list), 200


@guest.route('/update_delivery_status', methods=['POST'])
@flask_praetorian.auth_required
def update_delivery_status():
    try:
        data = request.json
        order_ids = data.get('order_ids')  # For bulk update
        order_id = data.get('id')  # For single update
        delivered_by = data.get('delivered_by')
        contact = data.get('contact')
        address = data.get('address')
        note = data.get('note')
        status = data.get('status', 'delivered')  # Default to delivered
        item_index = data.get('item_index')  # For updating specific item

        # Helper function to update items in an order
        def update_order_items(held_cart, item_index=None):
            try:
                items = json.loads(held_cart.items) if held_cart.items else []
                
                if item_index is not None:
                    # Update by index (specific item)
                    if 0 <= item_index < len(items):
                        items[item_index]['confirmed'] = "delivered"
                        # items[item_index]['checked_by'] = str(current_user.firstname + " " + current_user.lastname)
                        items[item_index]['cutting_status'] = "delivered"
                        updated_item = items[item_index]
                        item_found = True
                    else:
                        item_found = False
                        updated_item = None
                else:
                    # Update all items in the order
                    for item in items:
                        item['confirmed'] = "delivered"
                        item['cutting_status'] = "delivered"
                    updated_item = items[0] if items else None
                    item_found = True
                
                held_cart.items = json.dumps(items)
                return item_found, updated_item
                
            except (json.JSONDecodeError, Exception) as e:
                print(f"⚠️ Failed to update items for order {held_cart.id}: {str(e)}")
                return False, None

        # Handle bulk update
        if order_ids and isinstance(order_ids, list):
            updated_orders = []
            not_found_orders = []
            email_sent_count = 0
            
            for order_id in order_ids:
                held_cart = HeldCart.query.filter_by(id=order_id).first()
                
                if held_cart:
                    # Update items in the order
                    item_found, updated_item = update_order_items(held_cart, item_index)
                    
                    if not item_found and item_index is not None:
                        not_found_orders.append(order_id)
                        continue
                    
                    # Update delivery fields
                    held_cart.delivered_by = delivered_by
                    held_cart.delivery_contact = contact
                    held_cart.delivery_address = address
                    held_cart.delivery_note = note
                    held_cart.delivery_status = status
                    
                    if status == 'delivered':
                        held_cart.delivery_date = datetime.now()
                        held_cart.status = "Delivered"  # Update main status
                    
                    updated_orders.append(order_id)
                    
                    # --- SEND DELIVERY EMAIL FOR THIS ORDER ---
                    if status == 'delivered':
                        customer_email = None
                        customer_name = "Valued Customer"
                        
                        # Get customer from order
                        if held_cart.customer_id:
                            customer = Customer.query.filter_by(id=held_cart.customer_id).first()
                            if customer:
                                customer_email = getattr(customer, 'email', None)
                                customer_name = getattr(customer, 'firstname', '') + ' ' + getattr(customer, 'lastname', '')
                                if not customer_name or customer_name.strip() == '':
                                    customer_name = "Valued Customer"
                        
                        # Send delivery email if we have a customer email
                        if customer_email:
                            try:
                                send_delivery_email(order_id, customer_name, customer_email, delivered_by, contact, address, note)
                                email_sent_count += 1
                            except Exception as email_error:
                                print(f"⚠️ Failed to send delivery email to {customer_email}: {str(email_error)}")
                else:
                    not_found_orders.append(order_id)
            
            db.session.commit()
            
            return jsonify({
                "success": True,
                "message": f"Updated {len(updated_orders)} orders",
                "updated_orders": updated_orders,
                "not_found_orders": not_found_orders,
                "status": status,
                "email_sent_count": email_sent_count
            }), 200
        
        # Handle single update (original functionality)
        elif order_id:
            held_cart = HeldCart.query.filter_by(id=order_id).first()
            
            if not held_cart:
                return jsonify({"error": "Order not found"}), 404

            # Update items in the order
            item_found, updated_item = update_order_items(held_cart, item_index)
            
            if not item_found and item_index is not None:
                return jsonify({"error": f"Item at index {item_index} not found in order"}), 404

            # Update delivery fields
            held_cart.delivered_by = delivered_by
            held_cart.delivery_contact = contact
            held_cart.delivery_address = address
            held_cart.delivery_note = note
            held_cart.delivery_status = status
            
            if status == 'delivered':
                held_cart.delivery_date = datetime.now()
                held_cart.status = "Delivered"  # Update main status

            db.session.commit()
            
            # --- SEND DELIVERY EMAIL FOR SINGLE ORDER ---
            email_sent = False
            
            if status == 'delivered':
                customer_email = None
                customer_name = "Valued Customer"
                
                # Get customer from order
                if held_cart.customer_id:
                    customer = Customer.query.filter_by(id=held_cart.customer_id).first()
                    if customer:
                        customer_email = getattr(customer, 'email', None)
                        customer_name = getattr(customer, 'firstname', '') + ' ' + getattr(customer, 'lastname', '')
                        if not customer_name or customer_name.strip() == '':
                            customer_name = "Valued Customer"
                
                # Send delivery email if we have a customer email
                if customer_email:
                    try:
                        send_delivery_email(order_id, customer_name, customer_email, delivered_by, contact, address, note)
                        email_sent = True
                    except Exception as email_error:
                        print(f"⚠️ Failed to send delivery email to {customer_email}: {str(email_error)}")

            return jsonify({
                "success": True,
                "message": "Delivery status updated",
                "order_id": order_id,
                "status": status,
                "item_updated": updated_item,
                "item_index": item_index,
                "email_sent": email_sent
            }), 200
        
        else:
            return jsonify({"error": "Order ID or Order IDs required"}), 400

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error in update_delivery_status: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

# Helper function to send delivery email
def send_delivery_email(order_id, customer_name, customer_email, delivered_by, contact, address, note):
    """Send a delivery confirmation email for an order"""
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Order Delivered - Asempahfie Graphics</title>
        <style>
            body {{
                font-family: 'Segoe UI', Arial, sans-serif;
                margin: 0;
                padding: 0;
                background-color: #f8f9fa;
                color: #333;
            }}
            .email-container {{
                max-width: 500px;
                margin: 20px auto;
                background-color: #ffffff;
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            }}
            .header {{
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                padding: 25px 20px;
                text-align: center;
                border-bottom: 4px solid #28a745;
            }}
            .header h1 {{
                color: #ffffff;
                font-size: 22px;
                margin: 0;
                font-weight: 700;
                letter-spacing: 1px;
            }}
            .header .subtitle {{
                color: #e0e0e0;
                font-size: 13px;
                margin: 5px 0 0;
                opacity: 0.9;
            }}
            .content {{
                padding: 25px 30px;
            }}
            .greeting {{
                font-size: 17px;
                color: #1a1a2e;
                margin-bottom: 15px;
                font-weight: 600;
            }}
            .greeting span {{
                color: #28a745;
            }}
            .delivery-badge {{
                background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
                border: 2px solid #28a745;
                padding: 15px 20px;
                border-radius: 10px;
                text-align: center;
                margin: 20px 0;
            }}
            .delivery-badge .status-icon {{
                font-size: 40px;
                display: block;
                margin-bottom: 5px;
            }}
            .delivery-badge .status-text {{
                font-size: 20px;
                font-weight: 700;
                color: #155724;
                letter-spacing: 1px;
            }}
            .delivery-badge .status-sub {{
                font-size: 13px;
                color: #155724;
                opacity: 0.8;
            }}
            .order-ref {{
                background: #f8f9fa;
                border-radius: 8px;
                padding: 15px 20px;
                margin: 20px 0;
                text-align: center;
                border: 2px dashed #dee2e6;
            }}
            .order-ref .order-number {{
                font-size: 28px;
                font-weight: 700;
                color: #1a1a2e;
                letter-spacing: 2px;
            }}
            .order-ref .order-label {{
                font-size: 13px;
                color: #888;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            .delivery-details {{
                background: #f8f9fa;
                border-radius: 8px;
                padding: 15px 20px;
                margin: 20px 0;
                border-left: 4px solid #28a745;
            }}
            .delivery-details p {{
                margin: 6px 0;
                font-size: 13px;
                color: #555;
            }}
            .delivery-details strong {{
                color: #1a1a2e;
                font-weight: 600;
            }}
            .delivery-details .detail-icon {{
                margin-right: 5px;
            }}
            .progress-steps {{
                display: flex;
                justify-content: space-between;
                margin: 25px 0;
                position: relative;
            }}
            .progress-steps::before {{
                content: '';
                position: absolute;
                top: 15px;
                left: 10%;
                right: 10%;
                height: 2px;
                background: #dee2e6;
                z-index: 0;
            }}
            .step {{
                text-align: center;
                flex: 1;
                position: relative;
                z-index: 1;
            }}
            .step .step-icon {{
                width: 30px;
                height: 30px;
                border-radius: 50%;
                background: #dee2e6;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 14px;
                font-weight: 700;
                margin-bottom: 5px;
            }}
            .step.active .step-icon {{
                background: #28a745;
            }}
            .step.completed .step-icon {{
                background: #28a745;
            }}
            .step .step-label {{
                font-size: 11px;
                color: #888;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
            .step.active .step-label {{
                color: #28a745;
                font-weight: 600;
            }}
            .step.completed .step-label {{
                color: #28a745;
                font-weight: 600;
            }}
            .thank-you {{
                background: linear-gradient(135deg, #fff5f5 0%, #fff0f0 100%);
                border-radius: 8px;
                padding: 15px 20px;
                margin: 20px 0;
                text-align: center;
                border: 1px solid #f5c6cb;
            }}
            .thank-you p {{
                margin: 5px 0;
                color: #721c24;
                font-size: 14px;
            }}
            .footer {{
                background: #f8f9fa;
                padding: 20px 30px;
                text-align: center;
                border-top: 1px solid #e9ecef;
                font-size: 12px;
                color: #888;
            }}
            .footer .shop-name {{
                font-size: 15px;
                font-weight: 700;
                color: #1a1a2e;
                margin-bottom: 3px;
            }}
            .footer .shop-info {{
                color: #666;
                margin: 2px 0;
                font-size: 12px;
            }}
            @media (max-width: 600px) {{
                .content {{
                    padding: 20px 15px;
                }}
                .order-ref .order-number {{
                    font-size: 22px;
                }}
                .progress-steps {{
                    flex-wrap: wrap;
                }}
                .step {{
                    flex: 0 0 33%;
                    margin-bottom: 10px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <h1>🎨 Asempahfie Graphics</h1>
                <div class="subtitle">📍 Kokomlemle, Accra • 📞 0243210009</div>
            </div>
            
            <div class="content">
                <div class="greeting">Dear <span>{customer_name}</span>,</div>
                
                <p style="color: #555; font-size: 14px; line-height: 1.6;">
                    Great news! 🎉 Your order has been successfully delivered!
                </p>
                
                <div class="delivery-badge">
                    <span class="status-icon">✅</span>
                    <div class="status-text">DELIVERED</div>
                    <div class="status-sub">Status: Delivered</div>
                </div>
                
                <div class="order-ref">
                    <div class="order-label">📦 Order Reference</div>
                    <div class="order-number">#{order_id}</div>
                </div>
                
                <div class="delivery-details">
                    <p><strong><span class="detail-icon">👤</span> Delivered By:</strong> {delivered_by if delivered_by else 'N/A'}</p>
                    <p><strong><span class="detail-icon">📞</span> Contact:</strong> {contact if contact else 'N/A'}</p>
                    <p><strong><span class="detail-icon">📍</span> Delivery Address:</strong> {address if address else 'N/A'}</p>
                    <p><strong><span class="detail-icon">📝</span> Delivery Note:</strong> {note if note else 'No special instructions'}</p>
                    <p><strong><span class="detail-icon">📅</span> Delivered On:</strong> {datetime.now().strftime('%A, %B %d, %Y at %I:%M %p')}</p>
                </div>
                
                <div class="progress-steps">
                    <div class="step completed">
                        <div class="step-icon">✓</div>
                        <div class="step-label">Order Placed</div>
                    </div>
                    <div class="step completed">
                        <div class="step-icon">✓</div>
                        <div class="step-label">Printed</div>
                    </div>
                    <div class="step completed">
                        <div class="step-icon">✂</div>
                        <div class="step-label">Cutting</div>
                    </div>
                    <div class="step active">
                        <div class="step-icon">📦</div>
                        <div class="step-label">Delivered</div>
                    </div>
                </div>
                
                <div class="thank-you">
                    <p>🙏 Thank you for choosing <strong>Asempahfie Graphics</strong>!</p>
                    <p style="font-size: 13px; margin-top: 8px;">We hope you love your order. We look forward to serving you again!</p>
                </div>
                
                <p style="color: #1a1a2e; font-size: 13px; margin: 15px 0 5px; font-weight: 600; text-align: center;">
                    📢 Questions or feedback? Call us: 0243210009
                </p>
            </div>
            
            <div class="footer">
                <div class="shop-name">✨ Asempahfie Graphics ✨</div>
                <div class="shop-info">📍 Kokomlemle, Accra • 📞 0243210009</div>
                <div class="shop-info">📧 info@asempahfiegraphics.com</div>
                <p style="margin-top: 10px; font-size: 11px; color: #bbb;">
                    © {datetime.now().year} Asempahfie Graphics. All rights reserved.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Send email
    from flask_mail import Mail, Message
    from flask import current_app
    
    # mail = Mail(current_app)
    
    msg = Message(
        subject=f"✅ Order #{order_id} Delivered! - Asempahfie Graphics", html=html_content, sender="afgghana@gmail.com",
        recipients=[customer_email], 
       
    )
    
    mail.send(msg)
    print(f"✅ Delivery email sent to {customer_email} for order #{order_id}")

@guest.route('/get_helding_orders_givers', methods=['GET'])
@flask_praetorian.auth_required
def get_helding_orders_givers():
    user = flask_praetorian.current_user()
    us = User.query.filter_by(id=user.id).first()

    if not us:
        return jsonify({"error": "User not found"}), 404

    # Get only pending delivery orders
    held_orders = HeldCart.query.filter(
                HeldCart.delivery_status.in_([
                    "pending",
                    "Cutting",
                    "in_delivery"
                ])
            ).all()
    orders_list = []

    for order in held_orders:
        try:
            print(f"Raw items JSON for order {order.id}:", order.items)
            items = json.loads(order.items)

            # ✅ Use the parsed 'items' variable, not 'held_orders'
            orders_list.append({
                "id": order.id,
                "items": items,  # ✅ Fixed: use parsed items
                "total": order.total,
                "balance": order.balance,
                "note": order.note,
                "waiter": order.waiter,
                "company_name": order.company_name,
                "status": order.status,
                "digital_printing_status": order.contain_digital_printing,
                "working_on": order.working_on,
                "working_on_id": order.working_on_id,
                "working_on_label": order.working_on_label,
                "working_on_id_label": order.working_on_id_label,
                "working_on_large_format": order.working_on_large_format,
                "working_on_id_large_format": order.working_on_id_large_format,
                "working_on_dtf": order.working_on_dtf,
                "working_on_id_dtf": order.working_on_id_dtf,
                "working_on_digital_printing": order.working_on_digital_printing,
                "working_on_id_digital_printing": order.working_on_id_digital_printing,
            })

        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON for order {order.id}: {e}")

    return jsonify(orders_list), 200


@guest.route('/get_helding_orders_givers_processed', methods=['GET'])
@flask_praetorian.auth_required
def get_helding_orders_givers_processed():
    user = flask_praetorian.current_user()
    us = User.query.filter_by(id=user.id).first()

    if not us:
        return jsonify({"error": "User not found"}), 404

    # Get delivered or in_delivery orders
    held_orders = HeldCart.query.filter(
        HeldCart.delivery_status.in_(['delivered', 'in_delivery'])
    ).all()

    orders_list = []

    for order in held_orders:
        try:
            print(f"Raw items JSON for order {order.id}:", order.items)
            items = json.loads(order.items)

            # ✅ Include ALL items, no filtering
            orders_list.append({
                "id": order.id,
                "items": items,  # All items included
                "total": order.total,
                "note": order.note,
                "waiter": order.waiter,
                "customer": order.customer,
                "company_name": order.company_name,
                "status": order.status,
                "balance":order.balance,
                "delivery_status": getattr(order, 'delivery_status', 'delivered'),
                "delivered_by": getattr(order, 'delivered_by', None),
                "delivery_contact": getattr(order, 'delivery_contact', None),
                "delivery_address": getattr(order, 'delivery_address', None),
                "delivery_note": getattr(order, 'delivery_note', None),
                "delivery_date": getattr(order, 'delivery_date', None),
                "created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else None,
                "dtf_confirm": order.dtf_confirm,
                "working_on": order.working_on,
                "working_on_id": order.working_on_id
            })

        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON for order {order.id}: {e}")

    return jsonify(orders_list), 200

@guest.route('/get_helding_orders_dtf_processed', methods=['GET'])
@flask_praetorian.auth_required
def get_helding_orders_dtf_processed():
    user = flask_praetorian.current_user()
    us = User.query.filter_by(id=user.id).first()

    if not us:
        return jsonify({"error": "User not found"}), 404

    # Adjusting the query to get only held orders containing drinks and with unconfirmed drinks
    held_orders = HeldCart.query.filter_by(
    
    ).filter(
        HeldCart.contain_dtf == "yes",  # Orders with drinks
      # Unconfirmed drinks
    ).all()

    orders_list = []

    for order in held_orders:
        try:
            print(f"Raw items JSON for order {order.id}:", order.items)  # Debug
            items = json.loads(order.items)

            # Filter items to include only drinks
            filtered_items = [item for item in items if item.get("family") == "dtf" and item.get("confirmed") == True or item.get("confirmed") in [
                    "ready for pickup", "delivered", "printed","in_delivery"
                ]]
            print(f"Filtered items for order {order.id}:", filtered_items)

            if filtered_items:
                orders_list.append({
                    "id": order.id,
                                        "items": filtered_items,
                                        "total": order.total,
                                        "balance":order.balance,
                                        "note": order.note,
                                        "waiter": order.waiter,
                                        "company_name": order.company_name,
                                        "status": order.status,
                                        "digital_printing_status": order.contain_digital_printing,
                                        "working_on": order.working_on,
                                        "working_on_id": order.working_on_id,
                                        "working_on_label": order.working_on_label,
                                        "working_on_id_label": order.working_on_id_label,
                                        "working_on_large_format": order.working_on_large_format,
                                        "working_on_id_large_format": order.working_on_id_large_format,
                                        "working_on_dtf": order.working_on_dtf,
                                        "working_on_id_dtf": order.working_on_id_dtf,
                                        "working_on_digital_printing": order.working_on_digital_printing,
                                        "working_on_id_digital_printing": order.working_on_id_digital_printing, # Format the datetime
                                        "order.customer": order.customer,
                                        "created_at":order.created_at,
                })

        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON for order {order.id}: {e}")

    return jsonify(orders_list), 200


import json
from flask import request, jsonify
from datetime import datetime

@guest.route('/remove_held_order', methods=['POST'])
@flask_praetorian.auth_required
def remove_held_order():
    # held_order = HeldCart.query.filter_by(id=hold_id).first()
    user = flask_praetorian.current_user()
    session = Session.query.filter_by(status="current").first()

    name=request.json["name"]
    price=request.json["price"]
    # Create a cancel order entry for that product
    cancel_order = CanceldOrder(
        name=name,
        amount=price,
        date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        attendant=f"{user.firstname} {user.lastname}" if user else None,
        company_name=user.company_name if user else None,
        created_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        session=session.open_date if session else None
    )
    db.session.add(cancel_order)

    # Remove from items list
   

    db.session.commit()

    return jsonify({
        "message": "sucess",
        
    }), 200



@guest.route('/load_held_order/<int:hold_id>', methods=['GET'])
@flask_praetorian.auth_required
def load_held_order(hold_id):
    try:
        user = current_user()
        held_order = HeldCart.query.filter_by(
            id=hold_id,
            user_id=user.id
        ).first()
        
        if not held_order:
            return jsonify({"error": "Held order not found"}), 404
        
        # Parse items
        try:
            items = json.loads(held_order.items) if held_order.items else []
            for item in items:
                if 'description' not in item:
                    item['description'] = ''
                if 'confirmed' not in item:
                    item['confirmed'] = None
        except json.JSONDecodeError:
            items = []
        
        # Get balance
        balance = 0.0
        try:
            if held_order.balance and held_order.balance != "":
                balance = float(held_order.balance)
        except (ValueError, TypeError):
            balance = 0.0
        
        return jsonify({
            "id": held_order.id,
            "items": items,
            "total": held_order.total,
            "balance": balance,  # ✅ Added balance field
            "customer": held_order.customer_id,
            "note": held_order.note,
            "table": held_order.table,
            "waiter": held_order.waiter,
            "status": held_order.status,
            "paid_status": held_order.paid_status,
            "onetime": held_order.onetime,
            "created_at": held_order.created_at.isoformat() if held_order.created_at else None,
            "contain_food": held_order.contain_food,
            "contain_drink": held_order.contain_drink,
            "contain_digital_printing": held_order.contain_digital_printing,
            "contain_large_format": held_order.contain_large_format,
            "contain_label": held_order.contain_label,
            "contain_dtf": held_order.contain_dtf
        }), 200
        
    except Exception as e:
        print(f"Error loading held order: {str(e)}")
        return jsonify({"error": str(e)}), 500


@guest.route('/get_held_order_by_customer/<string:customer_id>', methods=['GET'])
@flask_praetorian.auth_required
def get_held_order_by_customer(customer_id):
    try:
        user = current_user()
        
        # Find held order by customer
        held_order = HeldCart.query.filter_by(
            customer=customer_id,
            company_name=user.company_name,
            paid_status="Pending"
        ).first()
        
        if not held_order:
            return jsonify({"error": "No held order found for this customer"}), 404
        
        # Parse items
        items = []
        try:
            if held_order.items:
                items = json.loads(held_order.items)
                for item in items:
                    if 'description' not in item:
                        item['description'] = ''
                    if 'confirmed' not in item:
                        item['confirmed'] = None
        except json.JSONDecodeError:
            items = []
        
        # Get balance
        balance = 0.0
        try:
            if held_order.balance and held_order.balance != "":
                balance = float(held_order.balance)
        except (ValueError, TypeError):
            balance = 0.0
        
        return jsonify({
            "id": held_order.id,
            "items": items,
            "total": held_order.total,
            "balance": balance,  # ✅ Added balance field
            "has_balance": balance > 0,
            "customer": held_order.customer,
            "note": held_order.note,
            "table": held_order.table,
            "waiter": held_order.waiter,
            "status": held_order.status,
            "paid_status": held_order.paid_status,
            "onetime": held_order.onetime,
            "created_at": held_order.created_at.isoformat() if held_order.created_at else None,
            "contain_food": held_order.contain_food,
            "contain_drink": held_order.contain_drink,
            "contain_digital_printing": held_order.contain_digital_printing,
            "contain_large_format": held_order.contain_large_format,
            "contain_label": held_order.contain_label,
            "contain_dtf": held_order.contain_dtf,
            "food_confirm": held_order.food_confirm,
            "drink_confirm": held_order.drink_confirm,
            "digital_printing_confirm": held_order.digital_printing_confirm,
            "large_format_confirm": held_order.large_format_confirm,
            "label_confirm": held_order.label_confirm,
            "dtf_confirm": held_order.dtf_confirm
        }), 200
        
    except Exception as e:
        print(f"Error getting held order by customer: {str(e)}")
        return jsonify({"error": str(e)}), 500


@guest.route('/load_held_orders_batch', methods=['POST'])
@flask_praetorian.auth_required
def load_held_orders_batch():
    try:
        user = current_user()
        data = request.json
        hold_ids = data.get('hold_ids', [])
        
        if not hold_ids:
            return jsonify({"error": "Hold IDs are required"}), 400
        
        held_orders = HeldCart.query.filter(
            HeldCart.id.in_(hold_ids),
            HeldCart.company_name == user.company_name
        ).all()
        
        result = []
        for held_order in held_orders:
            try:
                items = json.loads(held_order.items) if held_order.items else []
                for item in items:
                    if 'description' not in item:
                        item['description'] = ''
                    if 'confirmed' not in item:
                        item['confirmed'] = None
            except (json.JSONDecodeError, TypeError):
                items = []
            
            # Get balance
            balance = 0.0
            try:
                if held_order.balance and held_order.balance != "":
                    balance = float(held_order.balance)
            except (ValueError, TypeError):
                balance = 0.0
            
            result.append({
                "id": held_order.id,
                "items": items,
                "total": held_order.total,
                "balance": balance,  # ✅ Added balance field
                "has_balance": balance > 0,
                "customer": held_order.customer,
                "note": held_order.note,
                "table": held_order.table,
                "waiter": held_order.waiter,
                "status": held_order.status,
                "paid_status": held_order.paid_status,
                "created_at": held_order.created_at.isoformat() if held_order.created_at else None,
                "contain_food": held_order.contain_food,
                "contain_drink": held_order.contain_drink,
                "contain_digital_printing": held_order.contain_digital_printing,
                "contain_large_format": held_order.contain_large_format,
                "contain_label": held_order.contain_label,
                "contain_dtf": held_order.contain_dtf
            })
        
        # Calculate summary
        total_balance = sum(o["balance"] for o in result)
        total_amount = sum(o["total"] for o in result)
        
        return jsonify({
            "success": True,
            "count": len(result),
            "total_balance": total_balance,
            "total_amount": total_amount,
            "orders": result
        }), 200
        
    except Exception as e:
        print(f"Error loading held orders batch: {str(e)}")
        return jsonify({"error": str(e)}), 500


@guest.route('/merge_orders', methods=['POST'])
@flask_praetorian.auth_required
def merge_orders():
    data = request.json
    order_ids = data.get("order_ids", [])

    if not order_ids:
        return jsonify({"error": "No orders selected"}), 400

    orders = HeldCart.query.filter(HeldCart.id.in_(order_ids)).all()
    merged_items = []
    total = 0

    for order in orders:
        merged_items.extend(json.loads(order.items))
        total += order.total

    new_held = HeldCart(
        user_id=flask_praetorian.current_user().id,
        items=json.dumps(merged_items),paid_status="Pending",
        total=total,
        company_name=flask_praetorian.current_user().company_name
    )
    db.session.add(new_held)

    # Delete old held carts
    for order in orders:
        db.session.delete(order)

    db.session.commit()
    return jsonify({"message": "Orders merged successfully", "id": new_held.id}), 200


from collections import Counter
from flask import request, jsonify
@guest.route("/search_most_item", methods=["POST"])
@flask_praetorian.auth_required
def search_most_item():
    try:
        # Get the current user
        user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        
        # Get the date from request
        date_filter = request.json.get("date")
        
        # Validate user
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Validate input
        if not date_filter:
            return jsonify({"error": "Date is required"}), 400

        # ✅ Query HeldCart for orders on the specified date
        held_orders = HeldCart.query.filter(
            db.func.date(HeldCart.created_at) == date_filter,
            HeldCart.company_name == user.company_name
        ).all()

        # Count item occurrences across all held orders
        from collections import Counter
        item_counts = Counter()
        
        for order in held_orders:
            try:
                items = json.loads(order.items) if order.items else []
                for item in items:
                    item_name = item.get('name', 'Unknown')
                    qty = int(item.get('qty', 0))
                    item_counts[item_name] += qty
            except Exception as e:
                print(f"Error processing order {order.id}: {e}")
                continue

        # Format result - sort by count descending
        result = [
            {"name": name, "count": count} 
            for name, count in item_counts.most_common()
        ]

        return jsonify(result), 200

    except Exception as e:
        print(f"Error in search_most_item: {str(e)}")
        return jsonify({"error": str(e)}), 500


from collections import Counter
from flask import request, jsonify


@guest.route("/search_most_item_food", methods=["POST"])
@flask_praetorian.auth_required
def search_most_item_food():
    # Get current user
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()

    # Get session/date input
    session_filter = request.json.get("date")

    # Validate user
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Validate input
    if not session_filter:
        return jsonify({"error": "Session value is required"}), 400

    # Filter OrderItems by session (contains), company, and family == "food"
    order_items = OrderItem.query.filter(
        OrderItem.session.contains(session_filter),
        OrderItem.company_name == user.company_name,
        OrderItem.family == "food"
    ).all()

    # Count item occurrences
    item_counts = Counter(item.item_name for item in order_items)

    # Build response
    result = [{"name": name, "count": count} for name, count in item_counts.most_common()]

    return jsonify(result), 200

from collections import Counter
from flask import request, jsonify


@guest.route("/search_most_item_drink", methods=["POST"])
@flask_praetorian.auth_required
def search_most_item_drink():
    # Get current user
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()

    # Get session/date input
    session_filter = request.json.get("date")

    # Validate user
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Validate input
    if not session_filter:
        return jsonify({"error": "Session value is required"}), 400

    # Filter OrderItems by session (contains), company, and family == "drink"
    order_items = OrderItem.query.filter(
        OrderItem.session.contains(session_filter),
        OrderItem.company_name == user.company_name,
        OrderItem.family == "drink"
    ).all()

    # Count item occurrences
    item_counts = Counter(item.item_name for item in order_items)

    # Build response
    result = [{"name": name, "count": count} for name, count in item_counts.most_common()]

    return jsonify(result), 200


from collections import Counter
from flask import request, jsonify


from collections import Counter
from flask import request, jsonify

from flask_praetorian import auth_required
@guest.route("/search_most_attendant", methods=["POST"])
@flask_praetorian.auth_required
def search_most_attendant():
    try:
        # Get current user
        user = User.query.filter_by(id=flask_praetorian.current_user().id).first()

        # Get date filter
        date_filter = request.json.get("date")

        # Validate user and input
        if not user:
            return jsonify({"error": "User not found"}), 404

        if not date_filter:
            return jsonify({"error": "Date is required"}), 400

        # ✅ Query HeldCart for orders on the specified date
        held_orders = HeldCart.query.filter(
            db.func.date(HeldCart.created_at) == date_filter,
            HeldCart.company_name == user.company_name
        ).all()

        # Count items per attendant
        from collections import Counter
        attendant_counts = Counter()
        
        for order in held_orders:
            try:
                waiter = order.waiter or 'Unknown'
                items = json.loads(order.items) if order.items else []
                
                # Count total items sold by this attendant
                total_qty = sum(int(item.get('qty', 0)) for item in items)
                if total_qty > 0:
                    attendant_counts[waiter] += total_qty
            except Exception as e:
                print(f"Error processing order {order.id}: {e}")
                continue

        # Format result - sort by count descending
        result = [
            {"waiter": name, "count": count} 
            for name, count in attendant_counts.most_common()
        ]

        return jsonify(result), 200

    except Exception as e:
        print(f"Error in search_most_attendant: {str(e)}")
        return jsonify({"error": str(e)}), 500


@guest.route("/add_chef",methods=['POST'])
@flask_praetorian.auth_required
def add_chef():
    session = Session.query.filter_by(status="current").first()
   
    room_number=request.json["room_number"]
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    food =request.json["food"]
    
    # date =request.json["date"]
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now()
    inc = FoodChef(name=name,food=food,
                   created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date,company_name=user.company_name,session=session.open_date)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_chef_list",methods=['GET'])
@flask_praetorian.auth_required
def get_chef_list():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = FoodChef.query.all()
    result = guest_schema.dump(inc)
    return jsonify(result)







@guest.route("/delete_chef/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_chef(id):
      sub_data = FoodChef.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp


@guest.route('/get_stock_items', methods=['GET'])
@flask_praetorian.auth_required
def get_stock_items():
    categories = Category.query.all()
    data = []
    for cat in categories:
        items = Iteman.query.filter_by(category=cat.name).all()
        item_list = [{"id": item.id, "description": item.name} for item in items]
        data.append({
            "category": cat.name,
            "items": item_list
        })
    return jsonify(data)


@guest.route('/add_customer', methods=['POST'])
@flask_praetorian.auth_required
def add_customer():
    try:
        user = current_user()
        firstname = request.json.get("firstname", "").strip()
        lastname = request.json.get("lastname", "").strip()
        phone = request.json.get("phone", "").strip()
        email = request.json.get("email", "").strip()
        dob = request.json.get("dob", "").strip()
        # Validate required fields
        # if not firstname or not lastname:
        #     resp = jsonify({"error": "Firstname and lastname are required"})
        #     resp.status_code = 400
        #     return resp
        
        # Create new customer WITHOUT customer_id
        customer = Customer(
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            company_name=user.company_name,
            email=email,
            dob=dob,
            created_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        hashed_password = guard.hash_password(phone)
        
        owner = User(
                    firstname=firstname,
                    lastname=lastname,
                    
                    phone=phone,
                    username=phone,
                    hashed_password=hashed_password,
                    roles="customer",
                    email=email,
                    created_date=datetime.now()
                )
        
        db.session.add(owner)      
        db.session.add(customer)
        db.session.commit()
        
        # NOW generate the customer_id after commit
        customer_id = generate_customer_id(customer.id)
        customer.customer_id = customer_id
        db.session.commit()
        
        resp = jsonify({
            "success": True,
            "message": "Customer added successfully",
            "customer_id": customer_id,
            "customer": {
                "id": customer.id,
                "customer_id": customer_id,
                "firstname": customer.firstname,
                "lastname": customer.lastname,
                "phone": customer.phone
            }
        })
        resp.status_code = 200
        return resp
        
    except Exception as e:
        db.session.rollback()
        resp = jsonify({"error": str(e)})
        resp.status_code = 500
        return resp



@guest.route('/update_customer', methods=['PUT'])
@flask_praetorian.auth_required
def update_customer():
    try:
        user = current_user()

        data = request.json

        customer_id = data.get("customer_id")

        firstname = data.get("firstname", "").strip()
        lastname = data.get("lastname", "").strip()
        phone = data.get("phone", "").strip()
        email = data.get("email", "").strip()
        dob = data.get("dob", "").strip()

        if not customer_id:
            return jsonify({
                "success": False,
                "error": "customer_id is required"
            }), 400

        # Find existing customer
        customer = Customer.query.filter_by(
            id=customer_id,
            company_name=user.company_name
        ).first()

        if not customer:
            return jsonify({
                "success": False,
                "error": "Customer not found"
            }), 404

        # Update Customer
        customer.firstname = firstname
        customer.lastname = lastname
        customer.phone = phone
        customer.email = email
        customer.dob = dob

        # Find the corresponding User
        owner = User.query.filter_by(
            phone=customer.phone
        ).first()

        # If phone was changed, you may need another
        # way to identify the User. We handle that below.
        if not owner:
            owner = User.query.filter_by(
                email=customer.email
            ).first()

        if owner:
            owner.firstname = firstname
            owner.lastname = lastname
            owner.phone = phone
            owner.username = phone
            owner.email = email

            # Only update password if phone changed
            if phone:
                owner.hashed_password = guard.hash_password(phone)

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Customer updated successfully",
            "customer": {
                "id": customer.id,
                "customer_id": customer.customer_id,
                "firstname": customer.firstname,
                "lastname": customer.lastname,
                "phone": customer.phone,
                "email": customer.email,
                "dob": customer.dob
            }
        }), 200

    except Exception as e:
        db.session.rollback()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


def generate_customer_id(customer_id, prefix="AFG"):
    """Generate customer ID from the id"""
    return f"{prefix}{customer_id:03d}"
@guest.route('/get_customers', methods=['GET'])
@flask_praetorian.auth_required
def get_customers():
    customer = Customer.query.all()
    results=guest_schema.dump(customer)
    return jsonify(results)

@guest.route('/delete_customer/<int:customer_id>', methods=['DELETE'])
@flask_praetorian.auth_required
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({'message': 'Customer deleted successfully'})


@app.route('/apply_coupon/<int:customer_id>', methods=['POST','PUT'])
@flask_praetorian.auth_required
def apply_coupon(customer_id):
    # Your logic to apply coupon (e.g., apply a discount)
    # For now, we'll simulate the coupon being applied
    customer = Customer.query.filter_by(id=customer_id).first()
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    
    else:
        customer.coupon_applied = "no"
        customer.coupon_value= request.json["discount"]
        
        db.session.commit() 
        
    return jsonify({"message": "Coupon applied successfully"}), 200
    # Simulate a coupon being applied to customer (you might want to update their discount info here)
    



@guest.route("/add_account_group",methods=['POST'])
@flask_praetorian.auth_required
def add_account_group():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    subcategory =request.json["subcategory"]
    # price= request.json["price"]
    # unit =request.json["unit"]
    # category= request.json["category"]
    # family= request.json["family"]
    # wholesale= request.json["wholesale"]
    
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now()
    inc = AccountGroup(name=name,subcategory=subcategory,
                   created_date=created_date)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_account_group_list",methods=['GET'])
@flask_praetorian.auth_required
def get_account_group_list():
    # us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = AccountGroup.query.all()
    result = guest_schema.dump(inc)
    return jsonify(result)


@guest.route("/get_account_group_list_sorted",methods=['GET'])
@flask_praetorian.auth_required
def get_account_group_list_sorted():
    # us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = AccountGroup.query.filter_by(subcategory="Uncategorized").all()
    result = guest_schema.dump(inc)
    return jsonify(result)





@guest.route("/update_account_group",methods=['PUT'])
@flask_praetorian.auth_required
def update_account_group():
    id = request.json["id"]
    sub_data = AccountGroup.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.subcategory = request.json["subcategory"]
   

    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@guest.route("/delete_account_group/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_account_group(id):
      sub_data = AccountGroup.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp
  
  
@guest.route("/get_account_group/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_account_group(id):
    # us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = AccountGroup.query.all()
    result = guest_schema.dump(inc)
    return jsonify(result)






@guest.route("/add_account",methods=['POST'])
@flask_praetorian.auth_required
def add_account():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    subcategory =request.json["subcategory"]
    amount= request.json["amount"]
    # unit =request.json["unit"]
    # category= request.json["category"]
    # family= request.json["family"]
    # wholesale= request.json["wholesale"]
    
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now()
    inc = Account(name=name,subcategory=subcategory,amount=amount,
                   created_date=created_date)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_account_list",methods=['GET'])
@flask_praetorian.auth_required
def get_account_list():
    # us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Account.query.all()
    result = guest_schema.dump(inc)
    return jsonify(result)


@guest.route("/get_account_list_sorted",methods=['GET'])
@flask_praetorian.auth_required
def get_account_list_sorted():
    # us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Account.query.filter_by(subcategory="Uncategorized").all()
    result = guest_schema.dump(inc)
    return jsonify(result)



@guest.route("/detailed_report", methods=["POST"])
@flask_praetorian.auth_required
def detailed_report():
    """
    Generate comprehensive detailed report between two dates
    """
    try:
        us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        data = request.json
        
        date_from = data.get("date_from")
        date_to = data.get("date_to")
        
        if not date_from or not date_to:
            return jsonify({"error": "Both date_from and date_to are required"}), 400
        
        # Parse dates
        from datetime import datetime, timedelta
        start_date = datetime.strptime(date_from, '%Y-%m-%d').date()
        end_date = datetime.strptime(date_to, '%Y-%m-%d').date()
        end_date = end_date + timedelta(days=1)  # Include end date
        
        # ===================== HELD ORDERS =====================
        held_orders = HeldCart.query.filter(
            HeldCart.company_name == us.company_name,
            db.func.date(HeldCart.created_at) >= start_date,
            db.func.date(HeldCart.created_at) <= end_date
        ).all()
        
        held_orders_data = []
        total_held_amount = 0
        
        for order in held_orders:
            try:
                items = json.loads(order.items) if order.items else []
                order_total = float(order.total) if order.total else 0
                order_balance = float(order.balance) if order.balance else 0
                total_held_amount += order_total
                
                # ✅ FIX: Get customer name safely
                customer_name = "Walk-in"
                if order.customer:
                    # Check if customer is a name or ID
                    try:
                        # Try to convert to int - if it works, it's an ID
                        customer_id = int(order.customer)
                        customer = Customer.query.filter_by(id=customer_id).first()
                        if customer:
                            customer_name = f"{customer.firstname} {customer.lastname}".strip() or "Walk-in"
                    except (ValueError, TypeError):
                        # If it can't convert to int, it's already a name
                        customer_name = order.customer
                
                held_orders_data.append({
                    "id": order.id,
                    "items": items,
                    "total": order_total,
                    "balance": order_balance,
                    "waiter": order.waiter or 'N/A',
                    "customer": order.customer,
                    "customer_name": customer_name,
                    "status": order.status,
                    "paid_status": order.paid_status,
                    "created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else None,
                    "note": order.note or '',
                    "contain_dtf": order.contain_dtf,
                    "contain_digital_printing": order.contain_digital_printing,
                    "contain_large_format": order.contain_large_format,
                    "contain_label": order.contain_label,
                    "contain_food": order.contain_food,
                    "contain_drink": order.contain_drink
                })
            except Exception as e:
                print(f"Error processing held order {order.id}: {e}")
                continue
        
        # ===================== POS PAYMENTS =====================
        # ✅ FIX: Use payment_date column properly
        pos_payments = PosPayment.query.filter(
            PosPayment.company_name == us.company_name,
            PosPayment.payment_date >= start_date.strftime('%Y-%m-%d'),
            PosPayment.payment_date <= end_date.strftime('%Y-%m-%d')
        ).all()
        
        pos_data = []
        total_pos_amount = 0
        
        for payment in pos_payments:
            try:
                amount = float(payment.amount) if payment.amount else 0
                total_pos_amount += amount
                pos_data.append({
                    "id": payment.id,
                    "name": payment.name or 'Unknown',
                    "amount": amount,
                    "attendant": payment.attendant or 'N/A',
                    "cashier": payment.cashier or 'N/A',
                    "method": payment.method or 'Cash',
                    "quantity": payment.quantity or '1',
                    "customer": payment.customer or 'Walk-in',
                    "phone": payment.phone or '',
                    "payment_date": payment.payment_date
                })
            except Exception as e:
                print(f"Error processing POS payment {payment.id}: {e}")
                continue
        
        # ===================== REFUNDS =====================
        refunds = Refund.query.filter(
            Refund.company_name == us.company_name,
            Refund.refund_time >= start_date.strftime('%Y-%m-%d'),
            Refund.refund_time <= end_date.strftime('%Y-%m-%d')
        ).all()
        
        refund_data = []
        total_refund_amount = 0
        
        for refund in refunds:
            try:
                amount = float(refund.refund_amount) if refund.refund_amount else 0
                total_refund_amount += amount
                refund_data.append({
                    "id": refund.id,
                    "name": refund.name or 'Unknown',
                    "refund_amount": amount,
                    "authorized_by": refund.authorized_by or 'N/A',
                    "reason": refund.reason or 'N/A',
                    "payment_id": refund.payment_id,
                    "refund_time": refund.refund_time.strftime('%Y-%m-%d %H:%M:%S') if refund.refund_time else None
                })
            except Exception as e:
                print(f"Error processing refund {refund.id}: {e}")
                continue
        
        # ===================== EXPENSES =====================
        expenses = Expenses.query.filter(
            Expenses.company_name == us.company_name,
            Expenses.date >= start_date.strftime('%Y-%m-%d'),
            Expenses.date <= end_date.strftime('%Y-%m-%d')
        ).all()
        
        expense_data = []
        total_expense_amount = 0
        
        for expense in expenses:
            try:
                amount = float(expense.amount) if expense.amount else 0
                total_expense_amount += amount
                expense_data.append({
                    "id": expense.id,
                    "name": expense.name or 'Unknown',
                    "amount": amount,
                    "note": expense.note or 'N/A',
                    "category": expense.subcategory or 'General',
                    "date": expense.date,
                    "user": expense.user or 'N/A'
                })
            except Exception as e:
                print(f"Error processing expense {expense.id}: {e}")
                continue
        
        # ===================== ATTENDANCE =====================
        attendance = Attendance.query.filter(
            Attendance.company_name == us.company_name,
            Attendance.created_date >= start_date.strftime('%Y-%m-%d'),
            Attendance.created_date <= end_date.strftime('%Y-%m-%d')
        ).all()
        
        attendance_data = []
        
        for att in attendance:
            try:
                attendance_data.append({
                    "id": att.id,
                    "name": att.name or 'Unknown',
                    "time_in": att.time_in or 'N/A',
                    "time_out": att.time_out or 'N/A',
                    "position": att.position or 'N/A',
                    "attendance": att.attendance or 'Present'
                })
            except Exception as e:
                print(f"Error processing attendance {att.id}: {e}")
                continue
        
        # ===================== MOST ORDERED ITEMS =====================
        item_count = {}
        for order in held_orders:
            try:
                items = json.loads(order.items) if order.items else []
                for item in items:
                    item_name = item.get('name', 'Unknown')
                    if item_name not in item_count:
                        item_count[item_name] = 0
                    item_count[item_name] += int(item.get('qty', 0))
            except Exception as e:
                print(f"Error counting items for order {order.id}: {e}")
                continue
        
        most_ordered = [{"name": k, "count": v} for k, v in item_count.items()]
        most_ordered.sort(key=lambda x: x['count'], reverse=True)
        
        # ===================== TOP ATTENDANTS =====================
        attendant_count = {}
        for order in held_orders:
            try:
                waiter = order.waiter or 'Unknown'
                if waiter not in attendant_count:
                    attendant_count[waiter] = 0
                items = json.loads(order.items) if order.items else []
                for item in items:
                    attendant_count[waiter] += int(item.get('qty', 0))
            except Exception as e:
                print(f"Error counting attendants for order {order.id}: {e}")
                continue
        
        top_attendants = [{"waiter": k, "count": v} for k, v in attendant_count.items()]
        top_attendants.sort(key=lambda x: x['count'], reverse=True)
        
        # ===================== SUMMARY =====================
        summary = {
            "total_held_orders": len(held_orders_data),
            "total_held_amount": round(total_held_amount, 2),
            "total_pos_amount": round(total_pos_amount, 2),
            "total_refund_amount": round(total_refund_amount, 2),
            "total_expense_amount": round(total_expense_amount, 2),
            "total_attendance": len(attendance_data),
            "total_orders": len(held_orders_data),
            "total_items_sold": sum([sum([item.get('qty', 0) for item in json.loads(order.items) if order.items]) for order in held_orders]) if held_orders else 0
        }
        
        return jsonify({
            "success": True,
            "summary": summary,
            "held_orders": held_orders_data,
            "pos_payments": pos_data,
            "refunds": refund_data,
            "expenses": expense_data,
            "attendance": attendance_data,
            "most_ordered": most_ordered[:10],
            "top_attendants": top_attendants[:10],
            "date_from": date_from,
            "date_to": date_to
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"Error in detailed_report: {str(e)}")
        return jsonify({"error": str(e)}), 500

@guest.route("/update_account",methods=['PUT'])
@flask_praetorian.auth_required
def update_account():
    id = request.json["id"]
    sub_data = Account.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.amount = request.json["name"]
    sub_data.subcategory = request.json["subcategory"]
   

    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =201
    return resp

@guest.route("/delete_account/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_account(id):
      sub_data = Account.query.filter_by(id=id).first()
      
      db.session.delete(sub_data)
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =201
      return resp
@guest.route("/balance_sheet", methods=["POST"])
@flask_praetorian.auth_required
def balance_sheet():
    try:
        from_date = request.json.get("from_date")
        to_date = request.json.get("to_date")

        if not from_date or not to_date:
            return jsonify({"error": "Please select both dates"}), 400

        # Get current user's company
        current_user = flask_praetorian.current_user()
        company_name = current_user.company_name

        start = datetime.strptime(from_date, "%Y-%m-%d")
        end = datetime.strptime(to_date, "%Y-%m-%d")
        end = end.replace(hour=23, minute=59, second=59)

        # -----------------------------------------------------
        #                      INCOME
        # -----------------------------------------------------
        # Convert session string to datetime for proper comparison
        income_records = HeldCart.query.filter(
            HeldCart.company_name == company_name,
            HeldCart.status.in_(["completed", "paid"]),  # Only completed sales
            func.date(HeldCart.session) >= start.date(),
            func.date(HeldCart.session) <= end.date()
        ).all()

        total_income = sum(float(i.total or 0) for i in income_records)

        # -----------------------------------------------------
        #                     EXPENSES
        # -----------------------------------------------------
        expense_records = Expenses.query.filter(
            Expenses.company_name == company_name,
            func.date(Expenses.session) >= start.date(),
            func.date(Expenses.session) <= end.date()
        ).all()

        grouped_expenses = {}
        category_totals = {}

        for e in expense_records:
            cat = e.name or "Other"
            sub = e.subcategory or "General"

            grouped_expenses.setdefault(cat, {}).setdefault(sub, 0)
            grouped_expenses[cat][sub] += float(e.amount or 0)

            category_totals[cat] = category_totals.get(cat, 0) + float(e.amount or 0)

        total_expenses = sum(float(e.amount or 0) for e in expense_records)

        # -----------------------------------------------------
        #                ACCOUNTS RECEIVABLE
        # -----------------------------------------------------
        # Credit sales that haven't been fully paid
        receivable_records = HeldCart.query.filter(
            HeldCart.company_name == company_name,
            HeldCart.paid_status.in_(["Pending", "Partial"]),
            HeldCart.status.in_(["completed", "paid"]),  # Only completed orders
            func.date(HeldCart.session) >= start.date(),
            func.date(HeldCart.session) <= end.date()
        ).all()

        accounts_receivable = sum(float(c.total or 0) for c in receivable_records)

        # -----------------------------------------------------
        #            STOCK AVAILABLE FOR SALE (Iteman)
        #            price × quantity
        # -----------------------------------------------------
        iteman_records = Iteman.query.filter(
            Iteman.company_name == company_name,
            Iteman.is_vip == "no",
            Iteman.voided != "yes"  # Exclude voided items
        ).all()

        stock_for_sale = sum(
            float(item.price or 0) * float(item.quantity or 0)
            for item in iteman_records
            if item.quantity and float(item.quantity) > 0
        )

        # -----------------------------------------------------
        #                    STOCK IN STORE
        #                    quantity × price (not just quantity)
        # -----------------------------------------------------
        stock_records = Stock.query.filter(
            Stock.company_name == company_name
        ).all()

        # This needs to join with Iteman to get prices
        # Or we need to store price in Stock table
        # For now, we'll calculate based on Iteman prices
        stock_in_store = 0
        for stock in stock_records:
            # Find matching item in Iteman to get price
            item = Iteman.query.filter(
                Iteman.company_name == company_name,
                Iteman.name == stock.name,
                Iteman.is_vip == "no",
                Iteman.voided != "yes"
            ).first()
            
            if item:
                stock_in_store += float(stock.quantity or 0) * float(item.price or 0)

        # -----------------------------------------------------
        #                     NET ASSETS
        # -----------------------------------------------------
        total_assets = total_income + accounts_receivable + stock_for_sale + stock_in_store
        net_assets = total_assets - total_expenses

        # -----------------------------------------------------
        #                    RETURN DATA
        # -----------------------------------------------------
        return jsonify({
            "from_date": from_date,
            "to_date": to_date,
            "income_total": round(total_income, 2),
            "accounts_receivable": round(accounts_receivable, 2),
            "stock_for_sale": round(stock_for_sale, 2),
            "stock_in_store": round(stock_in_store, 2),
            "total_assets": round(total_assets, 2),
            "total_expenses": round(total_expenses, 2),
            "net": round(net_assets, 2),
            "expense_groups": grouped_expenses,
            "expense_totals": category_totals
        })

    except Exception as e:
        print("Balance sheets error:", str(e))
        import traceback
        traceback.print_exc()
        return jsonify({"error": "Something went wrong"}), 500
@guest.route('/cocktail-setup/<int:item_id>', methods=['PUT'])
@flask_praetorian.auth_required
def save_cocktail_setup(item_id):
    item = Iteman.query.get_or_404(item_id)
    data = request.json

    # ✅ Only fail if category does NOT contain "cocktail"
    if not item.category or 'cocktail' not in item.category.lower():
        return jsonify({'error': 'Item is not a cocktail'}), 400

    # Save or overwrite the cocktail setup
    item.cocktail_setup = data.get('cocktail_setup', [])
    db.session.commit()

    # Serialize single item
    results = guest_single_schema.dump(item)
    return jsonify(results), 200


@guest.route('/cocktail-setup/<int:item_id>', methods=['GET'])
@flask_praetorian.auth_required
def get_cocktail_setup(item_id):
    item = Iteman.query.get_or_404(item_id)
    return jsonify(item.cocktail_setup or [])


from datetime import datetime, timedelta
import json
from sqlalchemy import desc

@guest.route('/sales_report', methods=['POST'])
@flask_praetorian.auth_required
def sales_report():
    try:
        user = current_user()
        data = request.json
        
        # Get date range from request
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        customer_filter = data.get('customer')  # Customer filter - string ID or name
        
        # Build query - include Success, Pending, and Partial paid_status
        query = HeldCart.query.filter_by(
            user_id=user.id,
        ).filter(
            HeldCart.paid_status.in_(['Success', 'Pending', 'Partial'])
        )
        
        # Apply date filter if provided
        if date_from and date_to:
            # If same date, query for that entire day
            if date_from == date_to:
                date_str = datetime.strptime(date_from, '%Y-%m-%d').strftime('%Y-%m-%d')
                # Query for the entire day (from 00:00:00 to 23:59:59)
                query = query.filter(
                    HeldCart.session >= date_str + ' 00:00:00',
                    HeldCart.session <= date_str + ' 23:59:59'
                )
            else:
                from_date_str = datetime.strptime(date_from, '%Y-%m-%d').strftime('%Y-%m-%d')
                to_date_str = datetime.strptime(date_to, '%Y-%m-%d').strftime('%Y-%m-%d')
                
                query = query.filter(
                    HeldCart.session >= from_date_str + ' 00:00:00',
                    HeldCart.session <= to_date_str + ' 23:59:59'
                )
        elif date_from:
            from_date_str = datetime.strptime(date_from, '%Y-%m-%d').strftime('%Y-%m-%d')
            query = query.filter(HeldCart.session >= from_date_str + ' 00:00:00')
        elif date_to:
            to_date_str = datetime.strptime(date_to, '%Y-%m-%d').strftime('%Y-%m-%d')
            query = query.filter(HeldCart.session <= to_date_str + ' 23:59:59')
        
        # Apply customer filter - FIXED: customer_id is a string
        if customer_filter:
            # Check if customer_filter is a valid string (not empty)
            if customer_filter :
                # Try to filter by customer_id (string) first
                query = query.filter(HeldCart.customer_id == customer_filter)
                # If no results, try filtering by customer name (partial match)
                # We'll handle this after fetching results if needed
            
        # Get all matching orders - ORDER BY created_at DESC (newest first)
        orders = query.order_by(desc(HeldCart.created_at)).all()
        
        # If customer filter didn't work with ID, try filtering by name
        if customer_filter and orders and len(orders) == 0:
            # Try filtering by customer name (case-insensitive partial match)
            query = query.filter(HeldCart.customer.ilike(f"%{customer_filter}%"))
            orders = query.order_by(desc(HeldCart.created_at)).all()
        
        # Calculate totals
        total_sales = sum(order.total for order in orders)
        total_orders = len(orders)
        total_balance = sum(float(order.balance) if order.balance else 0 for order in orders)
        total_collected = total_sales - total_balance
        
        # Get unique customers
        unique_customers = len(set(order.customer for order in orders if order.customer))
        
        # Get daily breakdown
        daily_sales = {}
        for order in orders:
            # Parse the session string to datetime for formatting
            if order.session:
                try:
                    # If session is stored as string from datetime.now()
                    session_date = datetime.strptime(order.session, '%Y-%m-%d %H:%M:%S.%f')
                    date_key = session_date.strftime('%Y-%m-%d')
                except ValueError:
                    # Try alternative format if needed
                    try:
                        session_date = datetime.strptime(order.session, '%Y-%m-%d %H:%M:%S')
                        date_key = session_date.strftime('%Y-%m-%d')
                    except ValueError:
                        date_key = order.session[:10] if len(order.session) >= 10 else 'unknown'
            elif order.created_at:
                # Fallback to created_at if session is not available
                try:
                    date_key = order.created_at.strftime('%Y-%m-%d') if hasattr(order.created_at, 'strftime') else str(order.created_at)[:10]
                except:
                    date_key = 'unknown'
            else:
                date_key = 'unknown'
                
            if date_key not in daily_sales:
                daily_sales[date_key] = {
                    'total': 0,
                    'count': 0,
                    'balance': 0,
                    'collected': 0,
                    'orders': []
                }
            order_balance = float(order.balance) if order.balance else 0
            daily_sales[date_key]['total'] += order.total
            daily_sales[date_key]['count'] += 1
            daily_sales[date_key]['balance'] += order_balance
            daily_sales[date_key]['collected'] += order.total - order_balance
            daily_sales[date_key]['orders'].append({
                'id': order.id,
                'total': order.total,
                'balance': order.balance,
                'customer': order.customer,
                'created_at': order.session if order.session else order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else None
            })
        
        # Sort daily breakdown by date descending (newest first)
        sorted_daily_sales = dict(sorted(daily_sales.items(), key=lambda x: x[0], reverse=True))
        
        # Prepare response with all order details
        response = {
            'success': True,
            'summary': {
                'total_sales': total_sales,
                'total_orders': total_orders,
                'total_balance': total_balance,
                'total_collected': total_collected,
                'average_order': total_sales / total_orders if total_orders > 0 else 0,
                'unique_customers': unique_customers,
                'date_from': date_from,
                'date_to': date_to
            },
            'daily_breakdown': sorted_daily_sales,
            'orders': [
                {
                    'id': order.id,
                    'total': order.total,
                    'balance': order.balance or "0",
                    'customer': order.customer or 'Walk-in',
                    'customer_id': order.customer_id,
                    'created_at': order.session if order.session else order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else None,
                    'paid_status': order.paid_status,
                    'status': order.status,
                    'table': order.table,
                    'waiter': order.waiter,
                    'working_on': order.working_on,
                    'working_on_id': order.working_on_id,
                    'working_on_label': order.working_on_label,
                    'working_on_id_label': order.working_on_id_label,
                    'working_on_large_format': order.working_on_large_format,
                    'working_on_id_large_format': order.working_on_id_large_format,
                    'working_on_dtf': order.working_on_dtf,
                    'working_on_id_dtf': order.working_on_id_dtf,
                    'working_on_digital_printing': order.working_on_digital_printing,
                    'working_on_id_digital_printing': order.working_on_id_digital_printing,
                    'items': json.loads(order.items) if order.items else []
                }
                for order in orders
            ]
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"Error in sales report: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
@guest.route("/search_income_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_income_dates_two():
    try:
        date = request.json.get("date")
        date_two = request.json.get("datetwo")

        if not date or not date_two:
            return jsonify({
                "status": "error",
                "message": "Both date and datetwo are required."
            }), 400

        # Parse dates
        from datetime import datetime
        start_date = datetime.strptime(date, '%Y-%m-%d').date()
        end_date = datetime.strptime(date_two, '%Y-%m-%d').date()
        end_date = end_date + timedelta(days=1)

        # ✅ Query HeldCart for orders in the date range
        held_orders = HeldCart.query.filter(
            db.func.date(HeldCart.session) >= start_date,
            db.func.date(HeldCart.session) <= end_date       ).all()

        result = []
        total_sales = 0
        total_collected = 0
        total_balance = 0

        for order in held_orders:
            try:
                items = json.loads(order.items) if order.items else []
                order_total = float(order.total) if order.total else 0
                order_balance = float(order.balance) if order.balance else 0
                order_collected = order_total - order_balance

                total_sales += order_total
                total_collected += order_collected
                total_balance += order_balance

                # Get customer name
                customer_name = "Walk-in"
                if order.customer:
                    try:
                        customer_id = int(order.customer)
                        customer = Customer.query.filter_by(id=customer_id).first()
                        if customer:
                            customer_name = f"{customer.firstname} {customer.lastname}".strip() or "Walk-in"
                    except (ValueError, TypeError):
                        customer_name = order.customer

                for item in items:
                    item_price = float(item.get('price', 0))
                    item_qty = int(item.get('qty', 0))
                    item_total = item_price * item_qty

                    if order_total > 0:
                        item_collected = (order_collected / order_total) * item_total
                    else:
                        item_collected = 0

                    result.append({
                        "id": order.id,
                        "name": item.get('name', 'Unknown'),
                        "amount": round(item_collected, 2),
                        "quantity": item_qty,
                        "price": item_price,
                        "total": round(item_total, 2),
                        "order_total": round(order_total, 2),
                        "balance": round(order_balance, 2),
                        "collected": round(order_collected, 2),
                        "payment_method":order.payment_method,
                        "attendant": order.waiter or 'N/A',
                        "customer": customer_name,
                        "waiter": order.waiter,
                        "date": order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else None,
                        "paid_status": order.paid_status,
                        "order_status": order.status
                    })

            except Exception as e:
                print(f"Error processing order {order.id}: {e}")
                continue

        summary = {
            "total_sales": round(total_sales, 2),
            "total_collected": round(total_collected, 2),
            "total_balance": round(total_balance, 2),
            "total_orders": len(held_orders),
            "total_items": len(result)
        }

        return jsonify({
            "data": result,
            "summary": summary
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error in search_income_dates_two: {str(e)}")
        return jsonify({"error": str(e)}), 500


@guest.route("/search_most_item_two", methods=["POST"])
@flask_praetorian.auth_required
def search_most_item_two():
    try:
        user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        date = request.json.get("date")
        datetwo = request.json.get("datetwo")

        if not user:
            return jsonify({"error": "User not found"}), 404

        if not date or not datetwo:
            return jsonify({"error": "Both 'date' and 'datetwo' are required"}), 400

        from datetime import datetime, timedelta
        start_date = datetime.strptime(date, '%Y-%m-%d').date()
        end_date = datetime.strptime(datetwo, '%Y-%m-%d').date()
        end_date = end_date + timedelta(days=1)

        # ✅ Query HeldCart for orders in the date range
        held_orders = HeldCart.query.filter(
            db.func.date(HeldCart.created_at) >= start_date,
            db.func.date(HeldCart.created_at) <= end_date,
            HeldCart.company_name == user.company_name
        ).all()

        # Count item occurrences
        from collections import Counter
        item_counts = Counter()

        for order in held_orders:
            try:
                items = json.loads(order.items) if order.items else []
                for item in items:
                    item_name = item.get('name', 'Unknown')
                    qty = int(item.get('qty', 0))
                    item_counts[item_name] += qty
            except Exception as e:
                print(f"Error processing order {order.id}: {e}")
                continue

        result = [
            {"name": name, "count": count} 
            for name, count in item_counts.most_common()
        ]

        return jsonify(result), 200

    except Exception as e:
        print(f"Error in search_most_item_two: {str(e)}")
        return jsonify({"error": str(e)}), 500


@guest.route("/search_most_attendant_two", methods=["POST"])
@flask_praetorian.auth_required
def search_most_attendant_two():
    try:
        user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        date = request.json.get("date")
        datetwo = request.json.get("datetwo")

        if not user:
            return jsonify({"error": "User not found"}), 404

        if not date or not datetwo:
            return jsonify({"error": "Both 'date' and 'datetwo' are required"}), 400

        from datetime import datetime, timedelta
        start_date = datetime.strptime(date, '%Y-%m-%d').date()
        end_date = datetime.strptime(datetwo, '%Y-%m-%d').date()
        end_date = end_date + timedelta(days=1)

        # ✅ Query HeldCart for orders in the date range
        held_orders = HeldCart.query.filter(
            db.func.date(HeldCart.created_at) >= start_date,
            db.func.date(HeldCart.created_at) <= end_date,
            HeldCart.company_name == user.company_name
        ).all()

        # Count items per attendant
        from collections import Counter
        attendant_counts = Counter()

        for order in held_orders:
            try:
                waiter = order.waiter or 'Unknown'
                items = json.loads(order.items) if order.items else []
                total_qty = sum(int(item.get('qty', 0)) for item in items)
                if total_qty > 0:
                    attendant_counts[waiter] += total_qty
            except Exception as e:
                print(f"Error processing order {order.id}: {e}")
                continue

        result = [
            {"waiter": name, "count": count} 
            for name, count in attendant_counts.most_common()
        ]

        return jsonify(result), 200

    except Exception as e:
        print(f"Error in search_most_attendant_two: {str(e)}")
        return jsonify({"error": str(e)}), 500




@guest.route("/accept_order/<int:order_id>", methods=["POST", "PUT"])
@flask_praetorian.auth_required
def accept_order(order_id):
    try:
        user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
        order = HeldCart.query.get_or_404(order_id)
        if user.roles=="label":
      
            order.working_on_label = flask_praetorian.current_user().firstname + " " + flask_praetorian.current_user().lastname
            order.working_on_id_label = str(flask_praetorian.current_user().id)


        elif user.roles=="dtf":
            order.working_on_dtf = flask_praetorian.current_user().firstname + " " + flask_praetorian.current_user().lastname
            order.working_on_id_dtf = str(flask_praetorian.current_user().id)

        elif user.roles=="digital_printing":
            order.working_on_digital_printing = flask_praetorian.current_user().firstname + " " + flask_praetorian.current_user().lastname
            order.working_on_id_digital_printing = str(flask_praetorian.current_user().id) 

        elif user.roles=="large_format":
            order.working_on_large_format = flask_praetorian.current_user().firstname + " " + flask_praetorian.current_user().lastname
            order.working_on_id_large_format = str(flask_praetorian.current_user().id)


        db.session.commit()
        return jsonify({"message": "Order accepted successfully"}), 200
    except Exception as e:
        print(f"Error in accept_order: {str(e)}")
        return jsonify({"error": str(e)}), 500
 

@guest.route("/cutting_order/<int:order_id>", methods=["POST", "PUT"])
@flask_praetorian.auth_required
def cutting_order(order_id):
    try:
        order = HeldCart.query.get_or_404(order_id)
        current_user = flask_praetorian.current_user()
        
        # Parse existing items
        try:
            items = json.loads(order.items) if order.items else []
        except json.JSONDecodeError:
            items = []
        
        # Get the item index from request (if you're updating a specific item)
        data = request.get_json()
        item_index = data.get('item_index') if data else None
        
        # Find and update the specific item
        item_found = False
        updated_item = None
        
        if item_index is not None:
            # Update by index
            if 0 <= item_index < len(items):
                items[item_index]['confirmed'] = "ready for pickup"
                # items[item_index]['checked_by'] = str(current_user.firstname + " " + current_user.lastname)
                items[item_index]['cutting_status'] = "ready for pickup"
                item_found = True
                updated_item = items[item_index]
        else:
            # Update all items in the order
            for item in items:
                item['confirmed'] = "ready for pickup"
                item['cutting_status'] = "ready for pickup"
                item_found = True
                updated_item = item
        
        if not item_found:
            return jsonify({"error": "Item not found in order"}), 404
        
        # Update order items and status
        order.items = json.dumps(items)
        order.status = "ready for pickup"
        db.session.commit()
        
        # --- GET CUSTOMER INFORMATION ---
        customer_email = None
        customer_name = "Valued Customer"
        phone_number = None
        
        # Get customer using customer_id from order
        if order.customer_id:
            customer = Customer.query.filter_by(id=order.customer_id).first()
            if customer:
                customer_email = getattr(customer, 'email', None)
                phone_number = getattr(customer, 'phone', None)
                customer_name = getattr(customer, 'firstname', '') + ' ' + getattr(customer, 'lastname', '')
                if not customer_name or customer_name.strip() == '':
                    customer_name = "Valued Customer"
        
        # Initialize flags
        email_sent = False
        sms_sent = False
        
        # ========== SEND EMAIL CONFIRMATION ==========
        if customer_email:
            try:
                now = datetime.now()
                # Build simple email HTML
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Order Ready for Pickup - Asempahfie Graphics</title>
                    <style>
                        body {{
                            font-family: 'Segoe UI', Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            background-color: #f8f9fa;
                            color: #333;
                        }}
                        .email-container {{
                            max-width: 500px;
                            margin: 20px auto;
                            background-color: #ffffff;
                            border-radius: 12px;
                            overflow: hidden;
                            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
                        }}
                        .header {{
                            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                            padding: 25px 20px;
                            text-align: center;
                            border-bottom: 4px solid #28a745;
                        }}
                        .header h1 {{
                            color: #ffffff;
                            font-size: 22px;
                            margin: 0;
                            font-weight: 700;
                            letter-spacing: 1px;
                        }}
                        .header .subtitle {{
                            color: #e0e0e0;
                            font-size: 13px;
                            margin: 5px 0 0;
                            opacity: 0.9;
                        }}
                        .content {{
                            padding: 25px 30px;
                        }}
                        .greeting {{
                            font-size: 17px;
                            color: #1a1a2e;
                            margin-bottom: 15px;
                            font-weight: 600;
                        }}
                        .greeting span {{
                            color: #28a745;
                        }}
                        .status-card {{
                            background: linear-gradient(135deg, #f0fff4 0%, #e8f5e9 100%);
                            border-left: 4px solid #28a745;
                            padding: 15px 20px;
                            border-radius: 8px;
                            margin: 20px 0;
                        }}
                        .status-card .stage {{
                            font-size: 14px;
                            color: #555;
                            margin: 3px 0;
                        }}
                        .status-card .stage strong {{
                            color: #1a1a2e;
                        }}
                        .status-badge {{
                            display: inline-block;
                            padding: 4px 14px;
                            border-radius: 20px;
                            font-size: 13px;
                            font-weight: 600;
                            text-transform: uppercase;
                            letter-spacing: 0.5px;
                            background: #28a745;
                            color: white;
                            margin: 5px 0;
                        }}
                        .order-ref {{
                            background: #f8f9fa;
                            border-radius: 8px;
                            padding: 15px 20px;
                            margin: 20px 0;
                            text-align: center;
                            border: 2px dashed #28a745;
                        }}
                        .order-ref .order-number {{
                            font-size: 28px;
                            font-weight: 700;
                            color: #1a1a2e;
                            letter-spacing: 2px;
                        }}
                        .order-ref .order-label {{
                            font-size: 13px;
                            color: #888;
                            text-transform: uppercase;
                            letter-spacing: 1px;
                        }}
                        .progress-steps {{
                            display: flex;
                            justify-content: space-between;
                            margin: 25px 0;
                            position: relative;
                        }}
                        .progress-steps::before {{
                            content: '';
                            position: absolute;
                            top: 15px;
                            left: 10%;
                            right: 10%;
                            height: 2px;
                            background: #dee2e6;
                            z-index: 0;
                        }}
                        .step {{
                            text-align: center;
                            flex: 1;
                            position: relative;
                            z-index: 1;
                        }}
                        .step .step-icon {{
                            width: 30px;
                            height: 30px;
                            border-radius: 50%;
                            background: #dee2e6;
                            display: inline-flex;
                            align-items: center;
                            justify-content: center;
                            color: white;
                            font-size: 14px;
                            font-weight: 700;
                            margin-bottom: 5px;
                        }}
                        .step.active .step-icon {{
                            background: #28a745;
                        }}
                        .step.completed .step-icon {{
                            background: #28a745;
                        }}
                        .step .step-label {{
                            font-size: 11px;
                            color: #888;
                            text-transform: uppercase;
                            letter-spacing: 0.5px;
                        }}
                        .step.active .step-label {{
                            color: #28a745;
                            font-weight: 600;
                        }}
                        .step.completed .step-label {{
                            color: #28a745;
                            font-weight: 600;
                        }}
                        .footer {{
                            background: #f8f9fa;
                            padding: 20px 30px;
                            text-align: center;
                            border-top: 1px solid #e9ecef;
                            font-size: 12px;
                            color: #888;
                        }}
                        .footer .shop-name {{
                            font-size: 15px;
                            font-weight: 700;
                            color: #1a1a2e;
                            margin-bottom: 3px;
                        }}
                        .footer .shop-info {{
                            color: #666;
                            margin: 2px 0;
                            font-size: 12px;
                        }}
                        @media (max-width: 600px) {{
                            .content {{
                                padding: 20px 15px;
                            }}
                            .order-ref .order-number {{
                                font-size: 22px;
                            }}
                            .progress-steps {{
                                flex-wrap: wrap;
                            }}
                            .step {{
                                flex: 0 0 33%;
                                margin-bottom: 10px;
                            }}
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="header">
                            <h1>🎨 Assempah fie Graphics</h1>
                            <div class="subtitle">📍 Kokomlemle, Accra • 📞 0243210009</div>
                        </div>
                        
                        <div class="content">
                            <div class="greeting">Dear <span>{customer_name}</span>,</div>
                            
                            <p style="color: #555; font-size: 14px; line-height: 1.6;">
                                Great news! Your order is now <strong>ready for pickup</strong>! 🎉
                            </p>
                            
                            <div class="status-card">
                                <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                                    <div>
                                        <div class="stage"><strong>📋 Status:</strong> <span class="status-badge">Ready for Pickup</span></div>
                                        <div class="stage" style="margin-top: 5px;"><strong>✅ Stage:</strong> Complete</div>
                                        <div class="stage" style="margin-top: 5px;"><strong>👤 Prepared By:</strong> {current_user.firstname} {current_user.lastname}</div>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="order-ref">
                                <div class="order-label">📦 Order Reference</div>
                                <div class="order-number">#{order_id}</div>
                            </div>
                            
                            <div class="progress-steps">
                                <div class="step completed">
                                    <div class="step-icon">✓</div>
                                    <div class="step-label">Order Placed</div>
                                </div>
                                <div class="step completed">
                                    <div class="step-icon">✓</div>
                                    <div class="step-label">Printed</div>
                                </div>
                                <div class="step completed">
                                    <div class="step-icon">✓</div>
                                    <div class="step-label">Cutting</div>
                                </div>
                                <div class="step active">
                                    <div class="step-icon">📦</div>
                                    <div class="step-label">Ready</div>
                                </div>
                            </div>
                            
                            <div style="background: #e8f5e9; padding: 15px; border-radius: 8px; margin: 20px 0; text-align: center;">
                                <p style="margin: 0; font-size: 16px; font-weight: 600; color: #2e7d32;">
                                    📍 Your order is ready for pickup at our location!
                                </p>
                                <p style="margin: 5px 0 0; font-size: 13px; color: #555;">
                                    Kokomlemle, Accra
                                </p>
                            </div>
                            
                            <p style="color: #666; font-size: 13px; line-height: 1.6; margin-top: 10px; text-align: center;">
                                Please come to our shop to collect your order.
                            </p>
                            
                            <p style="color: #1a1a2e; font-size: 13px; margin: 15px 0 5px; font-weight: 600; text-align: center;">
                                📢 Questions? Call us: 0243210009
                            </p>
                        </div>
                        
                        <div class="footer">
                            <div class="shop-name">✨ Asempahfie Graphics ✨</div>
                            <div class="shop-info">📍 Kokomlemle, Accra • 📞 0243210009</div>
                            <div class="shop-info">📧 info@asempahfiegraphics.com</div>
                            <p style="margin-top: 10px; font-size: 11px; color: #bbb;">
                                © {now.year} Asempahfie Graphics. All rights reserved.
                            </p>
                        </div>
                    </div>
                </body>
                </html>
                """
                
                # Send email
                from flask_mail import Message
                
                msg = Message(
                    subject=f"✅ Order #{order_id} - Ready for Pickup - Asempahfie Graphics",
                    html=html_content,
                    sender="afgghana@gmail.com",
                    recipients=[customer_email]
                )
                
                mail.send(msg)
                email_sent = True
                print(f"✅ Ready for pickup email sent to {customer_email} for order #{order_id}")
                
            except Exception as email_error:
                print(f"⚠️ Failed to send ready for pickup email to {customer_email}: {str(email_error)}")
                email_sent = False
        else:
            print(f"ℹ️ No email provided for order #{order_id}, skipping email notification")

        # ========== SEND SMS CONFIRMATION ==========
        if phone_number:
            try:
                # Clean phone number - remove spaces and ensure proper format
                clean_phone = ''.join(filter(str.isdigit, str(phone_number)))
                
                # Ensure it's a valid Ghana number (starts with 0 and is 10 digits)
                if len(clean_phone) == 10 and clean_phone.startswith('0'):
                    # Get current time for SMS
                    now = datetime.now()
                    
                    # Get attendant name
                    attendant = order.waiter if order.waiter else f"{current_user.firstname} {current_user.lastname}"
                    
                    # Build SMS message
                    sms_message = f"""
ASSEMPAH FIE GRAPHICS

Order #{order_id}
Dear {customer_name},
Your order is now ready for pickup!

Attendant: {attendant}
Date: {now.strftime('%d-%m-%Y %I:%M %p')}


Location: Kokomlemle, Accra
Hours: Mon-Sat 8am - 8pm

Contact Us:
Email: afgghana@gmail.com
Phone: 0243210009 / 0531100380
"""
                    
                    # Send SMS using the API
                    host = 'api.smsonlinegh.com'
                    requestURI = '/v5/message/sms/send'
                    apiKey = 'a7142fa4296ea493c9e2bd20352edf0d8c4191204fc126b7487408222a4fec27'
                    
                    headers = {
                        'Host': host,
                        'Content-Type': 'application/json',
                        'Accept': 'application/json',
                        'Authorization': f'key {apiKey}'
                    }
                    
                    msg_data = {
                        'text': sms_message.strip(),
                        'type': 0,  # 0 for standard SMS
                        'sender': 'ASEMPAH',  # Sender ID (max 11 characters)
                        'destinations': [clean_phone]
                    }
                    
                    httpConn = httpClient.HTTPConnection(host)
                    httpConn.request('POST', requestURI, json.dumps(msg_data), headers)
                    
                    response = httpConn.getresponse()
                    status = response.status
                    
                    if status == 200:
                        response_data = response.read()
                        print(f"✅ Ready for pickup SMS sent successfully to {clean_phone}: {response_data}")
                        sms_sent = True
                    else:
                        print(f"⚠️ SMS sending failed with status {status}: {response.read()}")
                        sms_sent = False
                    
                    httpConn.close()
                    
                else:
                    print(f"⚠️ Invalid phone number format: {clean_phone}")
                    sms_sent = False
                    
            except Exception as sms_error:
                print(f"⚠️ Failed to send ready for pickup SMS: {str(sms_error)}")
                sms_sent = False
        else:
            print(f"ℹ️ No phone number provided for order #{order_id}, skipping SMS notification")

        # ========== RETURN RESPONSE ==========
        return jsonify({
            "message": "Order is ready for pickup",
            "order_id": order_id,
            "status": "ready for pickup",
            "checked_by": current_user.firstname + " " + current_user.lastname,
            "cutting_status": "ready for pickup",
            "item_updated": updated_item,
            "email_sent": email_sent,
            "sms_sent": sms_sent,
            "customer_name": customer_name,
            "customer_email": customer_email,
            "customer_phone": phone_number
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error in cutting_order: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@guest.route(
    "/check_order_item/<order_id>/<item_id>",
    methods=["PUT"]
)
@flask_praetorian.auth_required
def check_order_item(order_id, item_id):

    try:

        # =====================================================
        # GET ORDER
        # =====================================================

        order = HeldCart.query.get(order_id)

        if not order:
            return jsonify({
                "success": False,
                "error": "Order not found.",
                "order_id": order_id
            }), 404

        current_user = flask_praetorian.current_user()

        # =====================================================
        # GET USER NAME
        # =====================================================

        firstname = getattr(
            current_user,
            "firstname",
            ""
        ) or ""

        lastname = getattr(
            current_user,
            "lastname",
            ""
        ) or ""

        checked_by = (
            f"{firstname} {lastname}"
        ).strip()

        if not checked_by:
            checked_by = "Unknown"

        # =====================================================
        # PARSE ITEMS
        # =====================================================

        if not order.items:

            return jsonify({
                "success": False,
                "error": "This order has no items.",
                "order_id": order_id
            }), 400

        try:

            if isinstance(order.items, str):
                items = json.loads(order.items)
            else:
                items = order.items

        except (json.JSONDecodeError, TypeError) as e:

            print(
                f"ITEM JSON ERROR - Order {order_id}: {e}"
            )

            return jsonify({
                "success": False,
                "error": "Invalid order items JSON.",
                "order_id": order_id
            }), 400

        # =====================================================
        # MAKE SURE ITEMS IS A LIST
        # =====================================================

        if not isinstance(items, list):

            return jsonify({
                "success": False,
                "error": "Order items are not stored as a list.",
                "order_id": order_id
            }), 400

        # =====================================================
        # NORMALIZE REQUESTED ID
        # =====================================================

        requested_item_id = str(item_id).strip()

        print(
            "\n================ CHECK ITEM ================"
        )

        print(
            f"Order ID: {order_id}"
        )

        print(
            f"Requested cart_item_id: "
            f"{requested_item_id}"
        )

        print(
            f"Number of items: {len(items)}"
        )

        # =====================================================
        # FIND ITEM
        # =====================================================

        found_item = None
        found_index = None

        available_ids = []

        for index, item in enumerate(items):

            if not isinstance(item, dict):
                continue

            cart_item_id = item.get(
                "cart_item_id"
            )

            if cart_item_id is not None:

                cart_item_id = str(
                    cart_item_id
                ).strip()

                available_ids.append(
                    cart_item_id
                )

            print(
                f"Item {index}: "
                f"cart_item_id={cart_item_id}"
            )

            # ---------------------------------------------
            # Compare UUID as strings
            # ---------------------------------------------

            if (
                cart_item_id
                and cart_item_id == requested_item_id
            ):

                found_item = item
                found_index = index

                break

        # =====================================================
        # ITEM NOT FOUND
        # =====================================================

        if found_item is None:

            print(
                "ITEM NOT FOUND"
            )

            print(
                "Requested:",
                requested_item_id
            )

            print(
                "Available:",
                available_ids
            )

            print(
                "===========================================\n"
            )

            return jsonify({

                "success": False,

                "error":
                    "Cart item not found.",

                "order_id":
                    order_id,

                "requested_cart_item_id":
                    requested_item_id,

                "available_cart_item_ids":
                    available_ids

            }), 404

        # =====================================================
        # UPDATE ITEM
        # =====================================================

        found_item["is_checked"] = "yes"

        found_item["checked_by"] = checked_by

        # Optional
        found_item["checked_at"] = datetime.utcnow().isoformat()

        # =====================================================
        # SAVE
        # =====================================================

        order.items = json.dumps(
            items
        )

        db.session.commit()

        print(
            f"ITEM CHECKED SUCCESSFULLY: "
            f"{requested_item_id}"
        )

        print(
            "===========================================\n"
        )

        # =====================================================
        # RESPONSE
        # =====================================================

        return jsonify({

            "success": True,

            "message":
                "Item checked successfully.",

            "order_id":
                order_id,

            "cart_item_id":
                requested_item_id,

            "item_index":
                found_index,

            "item":
                found_item,

            "is_checked":
                "yes",

            "checked_by":
                checked_by

        }), 200

    except Exception as e:

        db.session.rollback()

        print(
            "\nCHECK ITEM ERROR:"
        )

        print(
            str(e)
        )

        import traceback
        traceback.print_exc()

        return jsonify({

            "success": False,

            "error":
                str(e)

        }), 500


from flask import request, jsonify
from datetime import datetime
import json
import uuid
import http.client as httpClient
from flask_mail import Message

@guest.route('/hold_and_pay', methods=['POST'])
@flask_praetorian.auth_required
def hold_and_pay():
  

    try:
        # ==========================================================
        # CURRENT USER
        # ==========================================================
        user = flask_praetorian.current_user()
        data = request.get_json(silent=True)

        # ==========================================================
        # VALIDATION
        # ==========================================================
        if not data:
            return jsonify({
                "success": False,
                "error": "Request body is required."
            }), 400

        cart_items = data.get("cartItems")

        if not isinstance(cart_items, list):
            return jsonify({
                "success": False,
                "error": "'cartItems' must be a list."
            }), 400

        # ==========================================================
        # BASIC DATA
        # ==========================================================
        hold_id = data.get("id")

        # ==========================================================
        # AMOUNT PAID
        # ==========================================================
        try:
            amount_paid = float(data.get("amount_paid", 0) or 0)
        except (ValueError, TypeError):
            return jsonify({
                "success": False,
                "error": "Invalid amount_paid."
            }), 400

        if amount_paid < 0:
            amount_paid = 0

        # ==========================================================
        # CHECK FOR BALANCE PAYMENT FLAG
        # ==========================================================
        is_balance_payment = data.get("is_balance_payment", False)
        existing_balance_from_frontend = float(data.get("existing_balance", 0) or 0)

        # ==========================================================
        # FRONTEND TOTAL
        # ==========================================================
        try:
            supplied_total = float(data.get("total", 0) or 0)
        except (ValueError, TypeError):
            return jsonify({
                "success": False,
                "error": "Invalid total."
            }), 400

        if supplied_total < 0:
            supplied_total = 0

        # ==========================================================
        # DISCOUNT
        # ==========================================================
        try:
            discount = float(data.get("discount", 0) or 0)
        except (ValueError, TypeError):
            discount = 0

        if discount < 0:
            discount = 0
        if discount > 100:
            discount = 100

        # ==========================================================
        # DISCOUNT AMOUNT
        # ==========================================================
        try:
            supplied_discount_amount = float(data.get("discount_amount", 0) or 0)
        except (ValueError, TypeError):
            supplied_discount_amount = 0

        if supplied_discount_amount < 0:
            supplied_discount_amount = 0

        # ==========================================================
        # OTHER DATA
        # ==========================================================
        payment_method = data.get("method", "Cash") or "Cash"
        note = data.get("note", "") or ""
        table = data.get("table", "") or ""
        customer_id = data.get("customer")
        phone_number = data.get("phone_number", "") or ""

        # ==========================================================
        # CUSTOMER
        # ==========================================================
        customer = None
        customer_name = "Valued Customer"
        customer_email = data.get("customer_email", "") or ""

        if customer_id:
            try:
                customer = Customer.query.filter_by(id=int(customer_id)).first()
            except (ValueError, TypeError):
                customer = None

            if customer:
                customer_name = f"{customer.firstname} {customer.lastname}".strip()
                if hasattr(customer, "phone") and customer.phone:
                    phone_number = customer.phone
                if hasattr(customer, "email") and customer.email:
                    customer_email = customer.email

        # ==========================================================
        # FALLBACK CUSTOMER NAME
        # ==========================================================
        if customer_name == "Valued Customer" and data.get("customer_name"):
            customer_name = data.get("customer_name")

        # ==========================================================
        # UNIQUE CART ITEM ID
        # ==========================================================
        def generate_cart_item_id():
            return str(uuid.uuid4())

        # ==========================================================
        # PREPARE ONE CART ITEM
        # ==========================================================
        def prepare_cart_item(item):
            if not isinstance(item, dict):
                raise ValueError("Each cart item must be an object.")

            # Product ID
            product_id = item.get("id")
            if product_id is None or product_id == "":
                product_id = item.get("productId")
            if product_id is None or product_id == "":
                product_id = ""

            # Cart Item ID
            cart_item_id = item.get("cart_item_id")
            if not cart_item_id:
                cart_item_id = generate_cart_item_id()
            else:
                cart_item_id = str(cart_item_id)

            # Quantity
            try:
                qty = int(item.get("qty", 1) or 1)
            except (ValueError, TypeError):
                qty = 1
            if qty <= 0:
                qty = 1

            # Price
            try:
                price = float(item.get("price", 0) or 0)
            except (ValueError, TypeError):
                price = 0
            if price < 0:
                price = 0

            # Name
            name = item.get("name") or item.get("item_name") or ""

            # Measurements
            measurement = item.get("measurement")
            measurement_width = item.get("measurementWidth")
            measurement_height = item.get("measurementHeight")
            measurement_unit = item.get("measurementUnit")
            measurement_area = item.get("measurementArea")
            is_measurement_product = bool(item.get("is_measurement_product", False))
            show_measurement = bool(item.get("showMeasurement", is_measurement_product))

            if isinstance(measurement, dict):
                if measurement_width is None:
                    measurement_width = measurement.get("width")
                if measurement_height is None:
                    measurement_height = measurement.get("height")
                if not measurement_unit:
                    measurement_unit = measurement.get("unit")
                if measurement_area is None:
                    measurement_area = measurement.get("area")

            # Convert measurements
            if measurement_width is not None:
                try:
                    measurement_width = float(measurement_width)
                except (ValueError, TypeError):
                    measurement_width = None

            if measurement_height is not None:
                try:
                    measurement_height = float(measurement_height)
                except (ValueError, TypeError):
                    measurement_height = None

            if measurement_area is not None:
                try:
                    measurement_area = float(measurement_area)
                except (ValueError, TypeError):
                    measurement_area = None

            if measurement_unit:
                measurement_unit = str(measurement_unit)

            # Calculate area
            if measurement_area is None and measurement_width is not None and measurement_height is not None:
                measurement_area = measurement_width * measurement_height

            # Final measurement
            final_measurement = None
            if measurement_width is not None and measurement_height is not None and measurement_unit:
                final_measurement = {
                    "width": measurement_width,
                    "height": measurement_height,
                    "unit": measurement_unit,
                    "area": measurement_area
                }

            # Item total
            item_total = round(price * qty, 2)

            # Checked by
            is_checked = item.get("is_checked", "no")
            checked_by = item.get("checked_by", "") or ""

            if is_checked == "yes" and not checked_by:
                checked_by = f"{user.firstname} {user.lastname}".strip()

            # Final item
            prepared_item = {
                "cart_item_id": cart_item_id,
                "id": product_id,
                "name": name,
                "qty": qty,
                "price": round(price, 2),
                "total": item_total,
                "description": item.get("description", "") or "",
                "family": str(item.get("family", "")).strip(),
                "category": str(item.get("category", "")).strip(),
                "confirmed": bool(item.get("confirmed", False)),
                "is_checked": is_checked,
                "checked_by": checked_by,
                "is_checked_label": str(item.get("is_checked_label", "no")).strip(),
                "is_checked_dtf": str(item.get("is_checked_dtf", "no")).strip(),
                "is_checked_large_format": str(item.get("is_checked_large_format", "no")).strip(),
                "is_checked_digital_printing": str(item.get("is_checked_digital_printing", "no")).strip(),
                "is_vip": item.get("is_vip", "no"),
                "is_measurement_product": is_measurement_product,
                "measurement": final_measurement,
                "measurementWidth": measurement_width,
                "measurementHeight": measurement_height,
                "measurementUnit": measurement_unit,
                "measurementArea": measurement_area,
                "showMeasurement": show_measurement
            }

            return prepared_item

        # ==========================================================
        # PREPARE ALL ITEMS
        # ==========================================================
        incoming_items = []

        try:
            for item in cart_items:
                prepared_item = prepare_cart_item(item)
                incoming_items.append(prepared_item)
        except Exception as e:
            return jsonify({
                "success": False,
                "error": f"Invalid cart item: {str(e)}"
            }), 400

        # ==========================================================
        # CALCULATE ORIGINAL SUBTOTAL
        # ==========================================================
        calculated_subtotal = 0
        for item in incoming_items:
            item_price = float(item.get("price", 0) or 0)
            item_qty = int(item.get("qty", 1) or 1)
            calculated_subtotal += (item_price * item_qty)

        calculated_subtotal = round(calculated_subtotal, 2)

        # ==========================================================
        # DISCOUNT CALCULATION
        # ==========================================================
        calculated_discount_amount = round((calculated_subtotal * discount) / 100, 2)
        calculated_discounted_total = round(calculated_subtotal - calculated_discount_amount, 2)

        # ==========================================================
        # DETERMINE FINAL TOTAL
        # ==========================================================
        if discount > 0:
            total = calculated_discounted_total
            discount_amount = calculated_discount_amount
        elif supplied_total > 0:
            total = round(supplied_total, 2)
            discount_amount = round(max(calculated_subtotal - total, 0), 2)
            if calculated_subtotal > 0:
                discount = round((discount_amount / calculated_subtotal) * 100, 2)
        else:
            total = calculated_subtotal
            discount_amount = 0
            discount = 0

        # Empty cart
        if not incoming_items:
            calculated_subtotal = 0
            discount = 0
            discount_amount = 0
            total = 0

        # ==========================================================
        # IMPORTANT PAYMENT SAFETY
        # ==========================================================
        if amount_paid > total:
            amount_paid = round(total, 2)

        # ==========================================================
        # FIND EXISTING HOLD
        # ==========================================================
        existing_hold = None

        if hold_id:
            try:
                hold_id = int(hold_id)
            except (ValueError, TypeError):
                return jsonify({
                    "success": False,
                    "error": "Invalid hold ID."
                }), 400

            existing_hold = HeldCart.query.filter_by(
                id=hold_id,
                user_id=user.id
            ).first()

            if not existing_hold:
                return jsonify({
                    "success": False,
                    "error": "Held order not found."
                }), 404

        # ==========================================================
        # EXISTING HELD ORDER
        # ==========================================================
        if existing_hold:
            # ======================================================
            # GET PREVIOUS VALUES
            # ======================================================
            try:
                previous_balance = float(existing_hold.balance or 0)
            except (ValueError, TypeError):
                previous_balance = 0

            try:
                previous_total = float(existing_hold.total or 0)
            except (ValueError, TypeError):
                previous_total = 0

            # ======================================================
            # EXISTING ITEMS
            # ======================================================
            try:
                existing_items = json.loads(existing_hold.items) if existing_hold.items else []
                if not isinstance(existing_items, list):
                    existing_items = []
            except (json.JSONDecodeError, TypeError):
                existing_items = []

            # ======================================================
            # INDEX EXISTING CART LINES
            # ======================================================
            existing_by_cart_id = {}

            for existing_item in existing_items:
                if not isinstance(existing_item, dict):
                    continue

                existing_cart_id = existing_item.get("cart_item_id")
                if not existing_cart_id:
                    existing_cart_id = generate_cart_item_id()
                    existing_item["cart_item_id"] = existing_cart_id

                existing_by_cart_id[str(existing_cart_id)] = existing_item

            # ======================================================
            # MERGE ITEMS
            # ======================================================
            updated_items = []

            for new_item in incoming_items:
                cart_id = str(new_item["cart_item_id"])
                old_item = existing_by_cart_id.get(cart_id)

                if old_item:
                    # Preserve cart_item_id
                    old_item["cart_item_id"] = cart_id

                    # Basic information
                    old_item["id"] = new_item.get("id", old_item.get("id", ""))
                    old_item["name"] = new_item.get("name", old_item.get("name", ""))
                    old_item["price"] = float(new_item.get("price", old_item.get("price", 0)) or 0)

                    try:
                        old_item["qty"] = int(new_item.get("qty", old_item.get("qty", 1)) or 1)
                    except (ValueError, TypeError):
                        old_item["qty"] = 1

                    if old_item["qty"] <= 0:
                        old_item["qty"] = 1

                    # ALWAYS RECALCULATE LINE TOTAL
                    old_item["total"] = round(
                        float(old_item.get("price", 0)) * int(old_item.get("qty", 1)),
                        2
                    )

                    # Basic fields
                    old_item["description"] = new_item.get("description", old_item.get("description", ""))
                    old_item["family"] = new_item.get("family", old_item.get("family", ""))
                    old_item["category"] = new_item.get("category", old_item.get("category", ""))
                    old_item["confirmed"] = new_item.get("confirmed", old_item.get("confirmed", False))
                    old_item["is_vip"] = new_item.get("is_vip", old_item.get("is_vip", "no"))

                    # Checking
                    old_item["is_checked"] = new_item.get("is_checked", old_item.get("is_checked", "no"))
                    if new_item.get("checked_by"):
                        old_item["checked_by"] = new_item["checked_by"]

                    old_item["is_checked_label"] = new_item.get("is_checked_label", old_item.get("is_checked_label", "no"))
                    old_item["is_checked_dtf"] = new_item.get("is_checked_dtf", old_item.get("is_checked_dtf", "no"))
                    old_item["is_checked_large_format"] = new_item.get("is_checked_large_format", old_item.get("is_checked_large_format", "no"))
                    old_item["is_checked_digital_printing"] = new_item.get("is_checked_digital_printing", old_item.get("is_checked_digital_printing", "no"))

                    # Measurements
                    old_item["is_measurement_product"] = new_item.get("is_measurement_product", old_item.get("is_measurement_product", False))
                    old_item["measurement"] = new_item.get("measurement", old_item.get("measurement"))
                    old_item["measurementWidth"] = new_item.get("measurementWidth", old_item.get("measurementWidth"))
                    old_item["measurementHeight"] = new_item.get("measurementHeight", old_item.get("measurementHeight"))
                    old_item["measurementUnit"] = new_item.get("measurementUnit", old_item.get("measurementUnit"))
                    old_item["measurementArea"] = new_item.get("measurementArea", old_item.get("measurementArea"))
                    old_item["showMeasurement"] = new_item.get("showMeasurement", old_item.get("showMeasurement", False))

                    updated_items.append(old_item)
                else:
                    # New cart line
                    updated_items.append(new_item)

            # ======================================================
            # REMOVE REMOVED CART LINES
            # ======================================================
            incoming_cart_ids = {str(item["cart_item_id"]) for item in incoming_items}

            final_items = []
            for item in updated_items:
                item_cart_id = str(item.get("cart_item_id", ""))
                if item_cart_id in incoming_cart_ids:
                    final_items.append(item)

            # ======================================================
            # CALCULATE MERGED SUBTOTAL
            # ======================================================
            merged_subtotal = 0
            for item in final_items:
                try:
                    item_price = float(item.get("price", 0) or 0)
                except (ValueError, TypeError):
                    item_price = 0

                try:
                    item_qty = int(item.get("qty", 1) or 1)
                except (ValueError, TypeError):
                    item_qty = 1

                merged_subtotal += (item_price * item_qty)

            merged_subtotal = round(merged_subtotal, 2)

            # ======================================================
            # ======================================================
            # ======================================================
            # CRITICAL FIX: BALANCE PAYMENT LOGIC
            # ======================================================
            # ======================================================
            # ======================================================

            if is_balance_payment:
                # ==================================================
                # BALANCE PAYMENT - ONLY PAYING OUTSTANDING BALANCE
                # ==================================================
                #
                # When is_balance_payment is True:
                #   - The cart items are just for display/reference
                #   - We ONLY deduct the amount_paid from the existing balance
                #   - The total remains unchanged
                #   - No discounts apply to balance payments
                #   - The order total should NOT change
                #
                # ==================================================

                # NEW TOTAL stays the same as previous total
                new_total = previous_total

                # NEW BALANCE = previous balance - amount paid
                new_balance = previous_balance - amount_paid

                # Ensure balance doesn't go negative
                if new_balance < 0:
                    new_balance = 0

                new_balance = round(new_balance, 2)

                # No discount for balance payments
                discount = 0
                discount_amount = 0

                # Log for debugging
                print(f"💰 BALANCE PAYMENT:")
                print(f"   Previous Balance: {previous_balance}")
                print(f"   Amount Paid: {amount_paid}")
                print(f"   New Balance: {new_balance}")
                print(f"   Previous Total: {previous_total}")
                print(f"   New Total: {new_total}")

            else:
                # ==================================================
                # NORMAL PAYMENT - PAYING FOR ITEMS IN CART
                # ==================================================
                #
                # When is_balance_payment is False:
                #   - This is a normal order or adding items
                #   - Calculate new total from merged items
                #   - Apply discount if any
                #   - New balance = previous balance + change in total - payment
                #
                # ==================================================

                # Apply discount to merged subtotal
                if discount > 0:
                    new_total = round(merged_subtotal - (merged_subtotal * discount / 100), 2)
                    discount_amount = round(merged_subtotal - new_total, 2)
                elif supplied_total > 0:
                    new_total = round(supplied_total, 2)
                    discount_amount = round(max(merged_subtotal - new_total, 0), 2)
                    if merged_subtotal > 0:
                        discount = round((discount_amount / merged_subtotal) * 100, 2)
                else:
                    new_total = merged_subtotal
                    discount = 0
                    discount_amount = 0

                # Calculate new balance
                total_difference = new_total - previous_total
                new_balance = previous_balance + total_difference - amount_paid

                # Ensure balance doesn't go negative
                if new_balance < 0:
                    new_balance = 0

                new_balance = round(new_balance, 2)

                # Log for debugging
                print(f"💰 NORMAL PAYMENT:")
                print(f"   Previous Balance: {previous_balance}")
                print(f"   Previous Total: {previous_total}")
                print(f"   New Total: {new_total}")
                print(f"   Total Difference: {total_difference}")
                print(f"   Amount Paid: {amount_paid}")
                print(f"   New Balance: {new_balance}")

            # ======================================================
            # PAYMENT STATUS
            # ======================================================
            if new_balance <= 0:
                new_status = "Confirmed"
                new_paid_status = "Success"
            elif amount_paid > 0:
                new_status = "Pending"
                new_paid_status = "Partial"
            else:
                new_status = "Pending"
                new_paid_status = "Pending"

            # ======================================================
            # DEPARTMENT FLAGS
            # ======================================================
            contain_drink = any(item.get("family") == "drink" for item in final_items)
            contain_food = any(item.get("family") == "food" for item in final_items)
            contain_dtf = any(item.get("family") == "dtf" for item in final_items)
            contain_digital_printing = any(item.get("family") == "digital_printing" for item in final_items)
            contain_large_format = any(item.get("family") == "large_format" for item in final_items)
            contain_label = any(item.get("family") == "label" for item in final_items)

            # ======================================================
            # UPDATE HELD ORDER
            # ======================================================
            existing_hold.items = json.dumps(final_items)
            existing_hold.total = new_total
            existing_hold.balance = f"{new_balance:.2f}"
            existing_hold.status = new_status
            existing_hold.paid_status = new_paid_status
            existing_hold.payment_method = payment_method
            existing_hold.table = table

            existing_hold.contain_drink = "yes" if contain_drink else "no"
            existing_hold.contain_food = "yes" if contain_food else "no"
            existing_hold.contain_dtf = "yes" if contain_dtf else "no"
            existing_hold.contain_digital_printing = "yes" if contain_digital_printing else "no"
            existing_hold.contain_large_format = "yes" if contain_large_format else "no"
            existing_hold.contain_label = "yes" if contain_label else "no"

            # ======================================================
            # CUSTOMER
            # ======================================================
            if customer:
                existing_hold.customer = f"{customer.firstname} {customer.lastname}".strip()
                existing_hold.customer_id = customer.id

            # ======================================================
            # PAYMENT NOTE
            # ======================================================
            payment_note = (
                f"💰 Payment: GHS {amount_paid:.2f} | "
                f"Discount: {discount:.2f}% | "
                f"Total: GHS {new_total:.2f} | "
                f"Balance: GHS {new_balance:.2f}"
            )

            if is_balance_payment:
                payment_note = f"💳 BALANCE PAYMENT: GHS {amount_paid:.2f} | Remaining Balance: GHS {new_balance:.2f}"

            if amount_paid > 0:
                if existing_hold.note:
                    existing_hold.note = f"{existing_hold.note} | {payment_note}"
                else:
                    existing_hold.note = payment_note
            elif note:
                existing_hold.note = note

            order = existing_hold
            order_id = existing_hold.id
            total = new_total

        # ==========================================================
        # NEW ORDER
        # ==========================================================
        else:
            # ======================================================
            # NEW ORDER TOTAL
            # ======================================================
            new_total = round(total, 2)

            # ======================================================
            # NEW ORDER BALANCE
            # ======================================================
            new_balance = new_total - amount_paid
            if new_balance < 0:
                new_balance = 0
            new_balance = round(new_balance, 2)

            # ======================================================
            # PAYMENT STATUS
            # ======================================================
            if new_balance <= 0:
                order_status = "Confirmed"
                paid_status = "Success"
            elif amount_paid > 0:
                order_status = "Pending"
                paid_status = "Partial"
            else:
                order_status = "Pending"
                paid_status = "Pending"

            # ======================================================
            # DEPARTMENT FLAGS
            # ======================================================
            contain_drink = any(item.get("family") == "drink" for item in incoming_items)
            contain_food = any(item.get("family") == "food" for item in incoming_items)
            contain_dtf = any(item.get("family") == "dtf" for item in incoming_items)
            contain_digital_printing = any(item.get("family") == "digital_printing" for item in incoming_items)
            contain_large_format = any(item.get("family") == "large_format" for item in incoming_items)
            contain_label = any(item.get("family") == "label" for item in incoming_items)

            # ======================================================
            # PAYMENT NOTE
            # ======================================================
            final_note = note

            payment_note = (
                f"💰 Payment: GHS {amount_paid:.2f} | "
                f"Discount: {discount:.2f}% | "
                f"Discount Amount: GHS {discount_amount:.2f} | "
                f"Total: GHS {new_total:.2f} | "
                f"Balance: GHS {new_balance:.2f}"
            )

            if amount_paid > 0:
                final_note = f"{note} | {payment_note}" if note else payment_note
            elif discount > 0:
                final_note = f"{note} | {payment_note}" if note else payment_note

            # ======================================================
            # CREATE HELD CART
            # ======================================================
            order = HeldCart(
                user_id=user.id,
                items=json.dumps(incoming_items),
                total=new_total,
                balance=f"{new_balance:.2f}",
                customer=f"{customer.firstname} {customer.lastname}" if customer else data.get("customer", ""),
                customer_id=customer.id if customer else None,
                company_name=user.company_name,
                status=order_status,
                paid_status=paid_status,
                onetime="no",
                waiter=f"{user.firstname} {user.lastname}".strip(),
                contain_drink="yes" if contain_drink else "no",
                contain_food="yes" if contain_food else "no",
                contain_dtf="yes" if contain_dtf else "no",
                contain_digital_printing="yes" if contain_digital_printing else "no",
                contain_large_format="yes" if contain_large_format else "no",
                contain_label="yes" if contain_label else "no",
                food_confirm="no",
                drink_confirm="no",
                label_confirm="no",
                dtf_confirm="no",
                large_format_confirm="no",
                digital_printing_confirm="no",
                session=datetime.now(),
                table=table,
                note=note,
                payment_method=payment_method
            )

            db.session.add(order)
            db.session.flush()

            order_id = order.id
            total = new_total

        # ==========================================================
        # COMMIT ORDER
        # ==========================================================
        db.session.commit()

        # ==========================================================
        # NOTIFICATION VALUES
        # ==========================================================
        email_sent = False
        sms_sent = False

        try:
            notification_items = json.loads(order.items) if order.items else []
        except (json.JSONDecodeError, TypeError):
            notification_items = []

        try:
            order_total = float(order.total or 0)
        except (ValueError, TypeError):
            order_total = float(total)

        try:
            order_balance = float(order.balance or 0)
        except (ValueError, TypeError):
            order_balance = float(new_balance)

        # ==========================================================
        # EMAIL
        # ==========================================================
        if customer_email and "@" in str(customer_email):
            try:
                now = datetime.now()

                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Order Confirmation - Asempahfie Graphics</title>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            margin: 0;
                            padding: 0;
                            background-color: #f8f9fa;
                        }}
                        .email-container {{
                            max-width: 600px;
                            margin: 20px auto;
                            background: #ffffff;
                            border-radius: 12px;
                            overflow: hidden;
                            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
                        }}
                        .header {{
                            background: #1a1a2e;
                            padding: 30px 20px;
                            text-align: center;
                        }}
                        .header h1 {{
                            color: white;
                            margin: 0;
                            font-size: 26px;
                        }}
                        .content {{
                            padding: 30px;
                        }}
                        .items-table {{
                            width: 100%;
                            border-collapse: collapse;
                        }}
                        .items-table th {{
                            background: #1a1a2e;
                            color: white;
                            padding: 12px;
                            text-align: left;
                            font-size: 13px;
                        }}
                        .items-table td {{
                            padding: 12px;
                            border-bottom: 1px solid #e9ecef;
                            font-size: 13px;
                        }}
                        .measurement {{
                            font-size: 12px;
                            color: #666;
                            margin-top: 5px;
                            line-height: 1.5;
                        }}
                        .total-section {{
                            background: #1a1a2e;
                            color: white;
                            padding: 20px;
                            margin-top: 20px;
                            border-radius: 8px;
                            line-height: 1.8;
                        }}
                        .footer {{
                            text-align: center;
                            padding: 20px;
                            color: #777;
                            font-size: 12px;
                        }}
                        .balance-payment-badge {{
                            background: #ffc107;
                            color: #000;
                            padding: 10px;
                            text-align: center;
                            font-weight: bold;
                            border-radius: 8px;
                            margin: 15px 0;
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <div class="header">
                            <h1>Asempahfie Graphics</h1>
                            <div style="color:#ddd;font-size:14px;margin-top:8px;">
                                Kokomlemle, Accra • 0243210009
                            </div>
                        </div>
                        <div class="content">
                            <h3>Dear {customer_name},</h3>
                            <p>Thank you for choosing <strong>Asempahfie Graphics</strong>.</p>
                            """

                if is_balance_payment:
                    html_content += f"""
                            <div class="balance-payment-badge">
                                💳 BALANCE PAYMENT RECEIVED
                                <br>
                                Amount Paid: GHS {amount_paid:.2f}
                                <br>
                                Remaining Balance: GHS {order_balance:.2f}
                            </div>
                            """

                html_content += f"""
                            <p><strong>Order #{order_id}</strong></p>
                            <table class="items-table">
                                <thead>
                                    <tr>
                                        <th>Item</th>
                                        <th>Qty</th>
                                        <th>Price</th>
                                        <th>Total</th>
                                    </tr>
                                </thead>
                                <tbody>
                """

                for item in notification_items:
                    try:
                        item_qty = float(item.get("qty", 0) or 0)
                    except (ValueError, TypeError):
                        item_qty = 0

                    try:
                        item_price = float(item.get("price", 0) or 0)
                    except (ValueError, TypeError):
                        item_price = 0

                    item_total = round(item_price * item_qty, 2)

                    measurement_html = ""
                    measurement = item.get("measurement")
                    if not isinstance(measurement, dict):
                        measurement = {}

                    width = measurement.get("width")
                    if width is None:
                        width = item.get("measurementWidth")

                    height = measurement.get("height")
                    if height is None:
                        height = item.get("measurementHeight")

                    unit = measurement.get("unit")
                    if not unit:
                        unit = item.get("measurementUnit")

                    area = measurement.get("area")
                    if area is None:
                        area = item.get("measurementArea")

                    if width is not None and height is not None and unit:
                        try:
                            width_text = f"{float(width):g}"
                        except (ValueError, TypeError):
                            width_text = str(width)

                        try:
                            height_text = f"{float(height):g}"
                        except (ValueError, TypeError):
                            height_text = str(height)

                        measurement_html = f"""
                            <div class="measurement">
                                📏 {width_text} × {height_text} {unit}
                        """

                        if area is not None:
                            try:
                                area_text = f"{float(area):g}"
                            except (ValueError, TypeError):
                                area_text = str(area)

                            measurement_html += f"""
                                <br>Area: {area_text} sq {unit}
                            """

                        measurement_html += "</div>"

                    html_content += f"""
                        <tr>
                            <td>
                                <strong>{item.get("name", "")}</strong>
                                {measurement_html}
                            </td>
                            <td>{item_qty:g}</td>
                            <td>GHS {item_price:.2f}</td>
                            <td>GHS {item_total:.2f}</td>
                        </tr>
                    """

                html_content += f"""
                                </tbody>
                            </table>
                            <div class="total-section">
                                <strong>Subtotal:</strong> GHS {calculated_subtotal:.2f}
                                <br>
                                Discount: {discount:.2f}%
                                <br>
                                Discount Amount: GHS {discount_amount:.2f}
                                <br>
                                <strong>Order Total:</strong> GHS {order_total:.2f}
                                <br>
                                Amount Paid: GHS {amount_paid:.2f}
                                <br>
                                Balance: GHS {order_balance:.2f}
                                <br>
                                Payment Method: {payment_method}
                                <br>
                                Order Status: {order.status}
                                <br>
                                Date: {now.strftime("%d-%m-%Y %I:%M %p")}
                            </div>
                        </div>
                        <div class="footer">
                            Thank you for choosing Asempahfie Graphics.
                            <br><br>
                            Email: afgghana@gmail.com
                            <br>
                            Phone: 0243210009 / 0531100380
                        </div>
                    </div>
                </body>
                </html>
                """

                msg = Message(
                    subject=f"Order Confirmation - Asempahfie Graphics (Order #{order_id})",
                    recipients=[str(customer_email)],
                    html=html_content,
                    sender="afghana@gmail.com"
                )

                mail.send(msg)
                email_sent = True
                print(f"✅ Email sent successfully to {customer_email}")

            except Exception as e:
                email_sent = False
                print(f"⚠️ Failed to send email: {str(e)}")

        # ==========================================================
        # SMS
        # ==========================================================
        if phone_number:
            try:
                clean_phone = "".join(filter(str.isdigit, str(phone_number)))

                if len(clean_phone) == 10 and clean_phone.startswith("0"):
                    now = datetime.now()
                    attendant = order.waiter if order.waiter else f"{user.firstname} {user.lastname}".strip()

                    item_lines = []

                    for index, item in enumerate(notification_items, start=1):
                        try:
                            item_qty = float(item.get("qty", 0) or 0)
                        except (ValueError, TypeError):
                            item_qty = 0

                        try:
                            item_price = float(item.get("price", 0) or 0)
                        except (ValueError, TypeError):
                            item_price = 0

                        item_total = round(item_price * item_qty, 2)

                        item_text = f"{index}. {item.get('name', '')}"

                        measurement = item.get("measurement")
                        if not isinstance(measurement, dict):
                            measurement = {}

                        width = measurement.get("width")
                        if width is None:
                            width = item.get("measurementWidth")

                        height = measurement.get("height")
                        if height is None:
                            height = item.get("measurementHeight")

                        unit = measurement.get("unit")
                        if not unit:
                            unit = item.get("measurementUnit")

                        area = measurement.get("area")
                        if area is None:
                            area = item.get("measurementArea")

                        if width is not None and height is not None and unit:
                            try:
                                width_text = f"{float(width):g}"
                            except (ValueError, TypeError):
                                width_text = str(width)

                            try:
                                height_text = f"{float(height):g}"
                            except (ValueError, TypeError):
                                height_text = str(height)

                            item_text += f"\n   {width_text} x {height_text} {unit}"

                            if area is not None:
                                try:
                                    area_text = f"{float(area):g}"
                                except (ValueError, TypeError):
                                    area_text = str(area)

                                item_text += f"\n   Area: {area_text} sq {unit}"

                        item_text += f"\n   x{item_qty:g} = GHS {item_total:.2f}"
                        item_lines.append(item_text)

                    if len(notification_items) > 5:
                        item_lines.append(f"... and {len(notification_items) - 5} more items")

                    items_text = "\n".join(item_lines)

                    if order_balance <= 0:
                        status_text = "PAID IN FULL"
                        status_icon = "✅"
                    else:
                        status_text = f"BALANCE: GHS {order_balance:.2f}"
                        status_icon = "⏳"

                    # SMS Message
                    sms_message = f"""
ASSEMPAH FIE GRAPHICS
Order #{order_id}
Customer: {customer_name}
Status: {status_icon} {status_text}
Attendant: {attendant}
Location: Kokomlemle, Accra

ITEMS:
{items_text}

Subtotal: GHS {calculated_subtotal:.2f}
Discount: {discount:.2f}%
Discount Amount: GHS {discount_amount:.2f}
Total: GHS {order_total:.2f}
Paid: GHS {amount_paid:.2f}
Balance: GHS {order_balance:.2f}
Method: {payment_method}
Date: {now.strftime('%d-%m-%Y %I:%M %p')}

Thank you for choosing Asempahfie Graphics!

Contact Us:
Email: afgghana@gmail.com
Phone: 0243210009 / 0531100380
"""

                    # Send SMS via SMS Online GH
                    host = "api.smsonlinegh.com"
                    requestURI = "/v5/message/sms/send"
                    apiKey = "a7142fa4296ea493c9e2bd20352edf0d8c4191204fc126b7487408222a4fec27"

                    headers = {
                        "Host": host,
                        "Content-Type": "application/json",
                        "Accept": "application/json",
                        "Authorization": f"key {apiKey}"
                    }

                    msg_data = {
                        "text": sms_message.strip(),
                        "type": 0,
                        "sender": "Assempa Fie",
                        "destinations": [clean_phone]
                    }

                    httpConn = httpClient.HTTPConnection(host, timeout=15)

                    try:
                        httpConn.request(
                            "POST",
                            requestURI,
                            json.dumps(msg_data),
                            headers
                        )

                        response = httpConn.getresponse()
                        response_body = response.read()
                        status = response.status

                    finally:
                        httpConn.close()

                    if status == 200:
                        print(f"✅ SMS sent successfully: {response_body}")
                        sms_sent = True
                    else:
                        print(f"⚠️ SMS sending failed with status {status}: {response_body}")
                        sms_sent = False

                else:
                    print(f"⚠️ Invalid phone number format: {clean_phone}")

            except Exception as e:
                sms_sent = False
                print(f"⚠️ Failed to send SMS: {str(e)}")

        # ==========================================================
        # FINAL RESPONSE
        # ==========================================================
        return jsonify({
            "success": True,
            "message": "Order processed successfully",
            "id": order_id,
            "order_id": order_id,
            "subtotal": f"{float(calculated_subtotal):.2f}",
            "discount": f"{float(discount):.2f}",
            "discount_amount": f"{float(discount_amount):.2f}",
            "total": f"{float(total):.2f}",
            "balance": f"{float(new_balance):.2f}",
            "amount_paid": f"{float(amount_paid):.2f}",
            "status": order.status,
            "paid_status": order.paid_status,
            "is_held": float(new_balance) > 0,
            "is_paid": float(new_balance) <= 0,
            "is_full_payment": float(new_balance) <= 0,
            "email_sent": email_sent,
            "sms_sent": sms_sent,
            "items": json.loads(order.items) if order.items else []
        }), 200

    # ==============================================================
    # ERROR HANDLING
    # ==============================================================
    except Exception as e:
        db.session.rollback()
        import traceback
        traceback.print_exc()

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
@guest.route('/get_helding_orders_customers', methods=['GET'])
@flask_praetorian.auth_required
def get_helding_orders_customers():
    user = flask_praetorian.current_user()
    us = User.query.filter_by(id=user.id).first()

    if not us:
        return jsonify({"error": "User not found"}), 404

    # Query for held orders belonging to this user
    held_orders = HeldCart.query.filter_by(
    customer_id=user.id
).order_by(HeldCart.created_at.desc()).all()

    orders_list = []

    for order in held_orders:
        try:
            items = json.loads(order.items)  # Convert JSON string to list
            
            # Determine order status based on items
            order_status = order.status or "Pending"
            
            # Check if all items are confirmed
            all_confirmed = all(item.get('confirmed', False) for item in items)
            any_confirmed = any(item.get('confirmed', False) for item in items)
            
            if all_confirmed and len(items) > 0:
                order_status = "Completed"
            elif any_confirmed:
                order_status = "Partially Completed"
            elif order.status == "Confirmed":
                order_status = "Confirmed"
            else:
                order_status = "Processing"

            orders_list.append({
                "id": order.id,
                "items": items,
                "total": float(order.total) if order.total else 0,
                "balance": float(order.balance) if order.balance else 0,
                "note": order.note or "",
                "waiter": order.waiter or "",
                "customer": order.customer or "",
                "company_name": order.company_name or "",
                "status": order_status,
                "paid_status": order.paid_status or "Pending",
                "payment_method": order.payment_method or "",
                "contain_drink": order.contain_drink,
                "contain_food": order.contain_food,
                "contain_dtf": order.contain_dtf,
                "contain_digital_printing": order.contain_digital_printing,
                "contain_large_format": order.contain_large_format,
                "contain_label": order.contain_label,
                "food_confirm": order.food_confirm,
                "drink_confirm": order.drink_confirm,
                "label_confirm": order.label_confirm,
                "dtf_confirm": order.dtf_confirm,
                "large_format_confirm": order.large_format_confirm,
                "digital_printing_confirm": order.digital_printing_confirm,
                "created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else "",
                "updated_at": order.updated_at.strftime('%Y-%m-%d %H:%M:%S') if hasattr(order, 'updated_at') and order.updated_at else ""
            })

        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON for order {order.id}: {e}")

    return jsonify(orders_list), 200



@guest.route('/get_customer_payments', methods=['GET'])
@flask_praetorian.auth_required
def get_customer_payments():
    try:
        user = flask_praetorian.current_user()
        
        # Query for all orders belonging to this customer
        # Using customer_id field (which stores the user's ID)
        held_orders = HeldCart.query.filter_by(
            customer_id=user.id
        ).order_by(HeldCart.created_at.desc()).all()
        
        payments_list = []
        
        for order in held_orders:
            try:
                items = json.loads(order.items) if order.items else []
                
                # Determine payment status
                payment_status = "Completed"
                if order.paid_status == "Pending":
                    payment_status = "Pending"
                elif order.paid_status == "Success":
                    payment_status = "Completed"
                elif order.paid_status == "Failed":
                    payment_status = "Failed"
                
                # Get balance as float
                balance = float(order.balance) if order.balance else 0
                total = float(order.total) if order.total else 0
                
                # Calculate amount paid
                amount_paid = total - balance if balance > 0 else total
                
                payments_list.append({
                    "id": order.id,
                    "order_id": order.id,
                    "items": items,
                    "total": total,
                    "amount_paid": amount_paid,
                    "balance": balance,
                    "status": order.status or "Processing",
                    "payment_status": payment_status,
                    "payment_method": order.payment_method or "Not specified",
                    "created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else "",
                    "customer": order.customer or "Walk-in",
                    "waiter": order.waiter or "",
                    "note": order.note or "",
                    "contain_food": order.contain_food,
                    "contain_drink": order.contain_drink,
                    "contain_dtf": order.contain_dtf,
                    "contain_digital_printing": order.contain_digital_printing,
                    "contain_large_format": order.contain_large_format,
                    "contain_label": order.contain_label,
                    "item_count": len(items)
                })
                
            except (json.JSONDecodeError, TypeError) as e:
                print(f"Error decoding JSON for order {order.id}: {e}")
                continue
        
        return jsonify({
            "success": True,
            "payments": payments_list,
            "total_count": len(payments_list)
        }), 200
        
    except Exception as e:
        print(f"Error in get_customer_payments: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500



from datetime import datetime, timezone, timedelta
import json
import http.client as httpClient
import flask_praetorian
from flask import request, jsonify
from flask_mail import Message


# ============================================
# SMS SENDING FUNCTION (USING YOUR API)
# ============================================
def send_sms_bulk(phone, message):
    """
    Send SMS using your SMS Online GH API
    Handles both 0XXXXXXXXX and 233XXXXXXXXX formats
    Returns: (success: bool, message: str)
    """
    try:
        # Clean phone number - remove all non-digit characters
        clean_phone = ''.join(filter(str.isdigit, str(phone)))
        
        # Normalize Ghana phone number
        normalized_phone = None
        
        # Format 1: 0XXXXXXXXX (10 digits starting with 0)
        if len(clean_phone) == 10 and clean_phone.startswith('0'):
            normalized_phone = clean_phone
        
        # Format 2: 233XXXXXXXXX (12 digits starting with 233)
        elif len(clean_phone) == 12 and clean_phone.startswith('233'):
            # Convert to 0XXXXXXXXX format
            normalized_phone = '0' + clean_phone[3:]
        
        # Format 3: 233XXXXXXXX (11 digits - missing one digit)
        elif len(clean_phone) == 11 and clean_phone.startswith('233'):
            # Try to fix: take last 8 digits after 233
            normalized_phone = '0' + clean_phone[3:]
        
        # Format 4: 23XXXXXXXX (9 digits - missing one 3)
        elif len(clean_phone) == 9 and clean_phone.startswith('23'):
            normalized_phone = '0' + clean_phone[2:]
        
        # Format 5: Starts with 0 but has extra digits
        elif len(clean_phone) > 10 and clean_phone.startswith('0'):
            normalized_phone = clean_phone[:10]  # Take first 10 digits
        
        # Format 6: No prefix but starts with common network codes
        elif len(clean_phone) == 9:
            # Ghana network prefixes: 20, 24, 26, 27, 50, 54, 55, 59
            if clean_phone[:2] in ['20', '24', '26', '27', '50', '54', '55', '59']:
                normalized_phone = '0' + clean_phone
        
        # If not valid, return False with error message
        if not normalized_phone:
            error_msg = f"Invalid phone number format: {phone} (cleaned: {clean_phone})"
            print(f"⚠️ {error_msg}")
            return False, error_msg
        
        # Validate final format
        if len(normalized_phone) != 10 or not normalized_phone.startswith('0'):
            error_msg = f"Invalid normalized phone number: {normalized_phone}"
            print(f"⚠️ {error_msg}")
            return False, error_msg
        
        # Your SMS API Configuration
        host = 'api.smsonlinegh.com'
        requestURI = '/v5/message/sms/send'
        apiKey = 'a7142fa4296ea493c9e2bd20352edf0d8c4191204fc126b7487408222a4fec27'
        
        headers = {
            'Host': host,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'key {apiKey}'
        }
        
        # Prepare message data
        msg_data = {
            'text': message,
            'type': 0,  # 0 for standard SMS
            'sender': 'Assempa Fie',  # Sender ID (max 11 characters)
            'destinations': [normalized_phone]
        }
        
        # Send via HTTP
        httpConn = httpClient.HTTPConnection(host)
        httpConn.request('POST', requestURI, json.dumps(msg_data), headers)
        
        response = httpConn.getresponse()
        status = response.status
        response_data = response.read().decode('utf-8')
        httpConn.close()
        
        if status == 200:
            print(f"✅ SMS sent successfully to {normalized_phone} (original: {phone})")
            return True, "Sent successfully"
        else:
            error_msg = f"API Error {status}: {response_data}"
            print(f"⚠️ SMS sending failed: {error_msg}")
            return False, error_msg
            
    except Exception as e:
        error_msg = f"Exception: {str(e)}"
        print(f"⚠️ Failed to send SMS to {phone}: {error_msg}")
        return False, error_msg

# ============================================
# EMAIL SENDING FUNCTION (USING YOUR CONFIG)
# ============================================

def send_email_bulk(to_email, subject, message, company_name="Asempahfie Graphics"):
    """
    Send Email using your Flask-Mail configuration
    """
    try:
        # Validate email
        if not to_email or '@' not in str(to_email):
            print(f"⚠️ Invalid email: {to_email}")
            return False
        
        # Create HTML email template
        now = datetime.now()
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{subject}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f8f9fa; }}
                .email-container {{ max-width: 600px; margin: 20px auto; background: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
                .header {{ background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%); padding: 30px 20px; text-align: center; border-bottom: 4px solid #e94560; }}
                .header h1 {{ color: #ffffff; font-size: 24px; margin: 0; }}
                .content {{ padding: 30px; }}
                .greeting {{ font-size: 18px; color: #1a1a2e; margin-bottom: 15px; font-weight: 600; }}
                .message-body {{ color: #555; font-size: 15px; line-height: 1.8; margin: 20px 0; white-space: pre-wrap; }}
                .footer {{ background: #f8f9fa; padding: 25px 30px; text-align: center; border-top: 1px solid #e9ecef; color: #888; }}
                .footer .brand {{ font-size: 16px; font-weight: 700; color: #1a1a2e; }}
                .divider {{ border: none; border-top: 2px solid #e94560; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="email-container">
                <div class="header">
                    <h1>{company_name}</h1>
                    <div style="color: #e0e0e0; font-size: 14px;">📍 Kokomlemle, Accra • 📞 0243210009</div>
                </div>
                <div class="content">
                    <div class="greeting">Dear Valued Customer,</div>
                    <div class="message-body">{message}</div>
                    <hr class="divider">
                    <p style="color: #555; font-size: 14px; line-height: 1.6;">
                        💖 We truly appreciate your continued support and loyalty to {company_name}.
                        If you have any questions, please don't hesitate to contact us.
                    </p>
                </div>
                <div class="footer">
                    <div class="brand">✨ {company_name} ✨</div>
                    <div style="color: #666; margin: 3px 0;">📍 Kokomlemle, Accra</div>
                    <div style="color: #666; margin: 3px 0;">📞 0243210009</div>
                    <div style="color: #666; margin: 3px 0;">📧 afgghana@gmail.com</div>
                    <p style="margin-top: 15px; font-size: 12px; color: #aaa;">
                        © {now.year} {company_name}. All rights reserved.
                    </p>
                    <p style="font-size: 11px; color: #bbb; margin-top: 10px;">
                        This is an automated message. Please do not reply to this email.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Create and send email using Flask-Mail
        msg = Message(
            subject=subject,
            recipients=[str(to_email)],
            html=html_content,
            sender="afgghana@gmail.com"
        )
        mail.send(msg)
        print(f"✅ Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"⚠️ Failed to send email to {to_email}: {str(e)}")
        return False

# ============================================
# BULK MESSAGE ROUTES
# ============================================

@guest.route("/bulk_message/send", methods=["POST"])
@flask_praetorian.auth_required
def send_bulk_message():
    """
    Send bulk messages to users based on role
    """
    try:
        data = request.json
        current_user = flask_praetorian.current_user()
        company_name = current_user.company_name
        
        # Get form data
        subject = data.get('subject', 'Bulk Message')
        message = data.get('message', '')
        message_type = data.get('message_type', 'sms')  # sms, email, both
        recipient_type = data.get('recipient_type', 'customers')  # customers, employees, all
        schedule_delay = int(data.get('schedule', 0))  # minutes
        
        if not message:
            return jsonify({"error": "Message content is required"}), 400
        
        # Get recipients based on role
        recipients = []
        
        # Query users
        users = User.query.filter(
            User.is_active == True
        ).all()
        
        if recipient_type == 'customers':
            # Get customers (users with role='customer')
            filtered_users = [u for u in users if 'customer' in (u.roles or '').lower()]
        elif recipient_type == 'employees':
            # Get employees (users with role != 'customer')
            filtered_users = [u for u in users if 'customer' not in (u.roles or '').lower()]
        else:
            # Get all users
            filtered_users = users
        
        # Filter based on message type and ensure contact info exists
        for user in filtered_users:
            # Skip if no phone for SMS
            if message_type in ['sms', 'both'] and (not user.phone or user.phone == ''):
                continue
            # Skip if no email for email
            if message_type in ['email', 'both'] and (not user.email or user.email == ''):
                continue
                
            recipients.append({
                'id': user.id,
                'name': f"{user.firstname or ''} {user.lastname or ''}".strip() or user.username or 'Valued Customer',
                'phone': user.phone or '',
                'email': user.email or '',
                'role': 'customer' if 'customer' in (user.roles or '').lower() else 'employee'
            })
        
        # Remove duplicates based on phone/email
        unique_recipients = []
        seen_phones = set()
        seen_emails = set()
        
        for recipient in recipients:
            if recipient['phone'] and recipient['phone'] not in seen_phones:
                seen_phones.add(recipient['phone'])
                unique_recipients.append(recipient)
            elif recipient['email'] and recipient['email'] not in seen_emails:
                seen_emails.add(recipient['email'])
                unique_recipients.append(recipient)
        
        if not unique_recipients:
            return jsonify({"error": "No valid recipients found"}), 404
        
        # Create bulk message record
        bulk_message = BulkMessage(
            company_name=company_name,
            subject=subject,
            message=message,
            message_type=message_type,
            recipient_type=recipient_type,
            recipient_count=len(unique_recipients),
            status='pending',
            created_by=f"{current_user.firstname or ''} {current_user.lastname or ''}".strip() or current_user.username,
            created_at=datetime.now(timezone.utc)
        )
        
        if schedule_delay > 0:
            bulk_message.scheduled_for = datetime.now(timezone.utc) + timedelta(minutes=schedule_delay)
        
        db.session.add(bulk_message)
        db.session.flush()
        
        # Create recipient records
        for recipient in unique_recipients:
            msg_recipient = MessageRecipient(
                bulk_message_id=bulk_message.id,
                recipient_name=recipient['name'],
                recipient_phone=recipient['phone'],
                recipient_email=recipient['email'],
                recipient_role=recipient['role'],
                message_type=message_type,
                status='pending'
            )
            db.session.add(msg_recipient)
        
        db.session.commit()
        
        # Send messages immediately if not scheduled
        if schedule_delay == 0:
            # Start sending in background
            send_messages_background(bulk_message.id)
        
        return jsonify({
            "success": True,
            "message": f"✅ Bulk message created successfully! {len(unique_recipients)} recipients found.",
            "data": {
                "bulk_id": bulk_message.id,
                "recipient_count": len(unique_recipients),
                "status": bulk_message.status,
                "message_type": message_type,
                "recipient_type": recipient_type
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Bulk message error: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

def send_messages_background(bulk_id):
    """
    Background function to send messages
    """
    try:
        # Update status to sending
        bulk_message = BulkMessage.query.get(bulk_id)
        if not bulk_message:
            return
        
        recipients = MessageRecipient.query.filter_by(
            bulk_message_id=bulk_id,
            status='pending'
        ).all()
        
        bulk_message.status = 'sending'
        db.session.commit()
        
        sent_count = 0
        failed_count = 0
        
        for recipient in recipients:
            try:
                success = False
                message_text = bulk_message.message
                
                # Send SMS
                if bulk_message.message_type in ['sms', 'both'] and recipient.recipient_phone:
                    sms_sent = send_sms_bulk(
                        phone=recipient.recipient_phone,
                        message=message_text
                    )
                    if sms_sent:
                        success = True
                
                # Send Email
                if bulk_message.message_type in ['email', 'both'] and recipient.recipient_email:
                    email_sent = send_email_bulk(
                        to_email=recipient.recipient_email,
                        subject=bulk_message.subject or 'Bulk Message',
                        message=message_text,
                        company_name=bulk_message.company_name or "Asempahfie Graphics"
                    )
                    if email_sent:
                        success = True
                
                if success:
                    recipient.sent = True
                    recipient.status = 'sent'
                    recipient.sent_at = datetime.now(timezone.utc)
                    sent_count += 1
                else:
                    recipient.status = 'failed'
                    recipient.error_message = 'Failed to send message'
                    failed_count += 1
                
                db.session.commit()
                
            except Exception as e:
                recipient.status = 'failed'
                recipient.error_message = str(e)
                failed_count += 1
                db.session.commit()
                print(f"⚠️ Error sending to {recipient.recipient_name}: {str(e)}")
        
        # Update bulk message
        bulk_message.sent_count = sent_count
        bulk_message.failed_count = failed_count
        bulk_message.status = 'completed' if sent_count > 0 else 'failed'
        bulk_message.sent_at = datetime.now(timezone.utc)
        db.session.commit()
        
        print(f"✅ Bulk message {bulk_id} completed: {sent_count} sent, {failed_count} failed")
        
    except Exception as e:
        print(f"❌ Error in bulk send: {str(e)}")
        bulk_message = BulkMessage.query.get(bulk_id)
        if bulk_message:
            bulk_message.status = 'failed'
            db.session.commit()

@guest.route("/bulk_message/history", methods=["GET"])
@flask_praetorian.auth_required
def get_bulk_message_history():
    """
    Get bulk message history for the current company
    """
    try:
        current_user = flask_praetorian.current_user()
        company_name = current_user.company_name
        
        # Get all bulk messages for this company, ordered by newest first
        messages = BulkMessage.query.filter_by(
            company_name=company_name
        ).order_by(BulkMessage.created_at.desc()).limit(100).all()
        
        result = []
        for msg in messages:
            result.append({
                "id": msg.id,
                "subject": msg.subject,
                "message": msg.message[:200] + '...' if len(msg.message) > 200 else msg.message,
                "message_type": msg.message_type,
                "recipient_type": msg.recipient_type,
                "recipient_count": msg.recipient_count,
                "sent_count": msg.sent_count or 0,
                "failed_count": msg.failed_count or 0,
                "status": msg.status,
                "created_at": msg.created_at.isoformat() if msg.created_at else None,
                "sent_at": msg.sent_at.isoformat() if msg.sent_at else None,
                "created_by": msg.created_by
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"❌ History error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@guest.route("/bulk_message/status/<int:message_id>", methods=["GET"])
@flask_praetorian.auth_required
def get_bulk_message_status(message_id):
    """
    Get detailed status of a specific bulk message
    """
    try:
        current_user = flask_praetorian.current_user()
        company_name = current_user.company_name
        
        bulk_message = BulkMessage.query.filter_by(
            id=message_id
        ).first()
        
        if not bulk_message:
            return jsonify({"error": "Message not found"}), 404
        
        recipients = MessageRecipient.query.filter_by(
            bulk_message_id=message_id
        ).limit(200).all()
        
        recipient_list = []
        for r in recipients:
            recipient_list.append({
                "name": r.recipient_name,
                "phone": r.recipient_phone,
                "email": r.recipient_email,
                "role": r.recipient_role,
                "status": r.status,
                "sent_at": r.sent_at.isoformat() if r.sent_at else None,
                "error": r.error_message
            })
        
        return jsonify({
            "id": bulk_message.id,
            "subject": bulk_message.subject,
            "message": bulk_message.message,
            "message_type": bulk_message.message_type,
            "recipient_type": bulk_message.recipient_type,
            "recipient_count": bulk_message.recipient_count,
            "sent_count": bulk_message.sent_count or 0,
            "failed_count": bulk_message.failed_count or 0,
            "status": bulk_message.status,
            "created_at": bulk_message.created_at.isoformat() if bulk_message.created_at else None,
            "sent_at": bulk_message.sent_at.isoformat() if bulk_message.sent_at else None,
            "created_by": bulk_message.created_by,
            "recipients": recipient_list
        }), 200
        
    except Exception as e:
        print(f"❌ Status error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@guest.route("/bulk_message/preview", methods=["POST"])
@flask_praetorian.auth_required
def preview_bulk_message():
    """
    Preview recipients for a bulk message
    """
    try:
        data = request.json
        current_user = flask_praetorian.current_user()
        company_name = current_user.company_name
        
        recipient_type = data.get('recipient_type', 'customers')
        message_type = data.get('message_type', 'sms')
        
        # Query users
        users = User.query.filter(
            User.company_name == company_name,
            User.is_active == True
        ).all()
        
        if recipient_type == 'customers':
            filtered_users = [u for u in users if 'customer' in (u.roles or '').lower()]
        elif recipient_type == 'employees':
            filtered_users = [u for u in users if 'customer' not in (u.roles or '').lower()]
        else:
            filtered_users = users
        
        # Filter based on message type
        if message_type in ['sms', 'both']:
            filtered_users = [u for u in filtered_users if u.phone and u.phone != '']
        if message_type in ['email', 'both']:
            filtered_users = [u for u in filtered_users if u.email and u.email != '']
        
        # Limit to 5 previews
        preview_users = filtered_users[:5]
        
        preview_data = []
        for user in preview_users:
            preview_data.append({
                "name": f"{user.firstname or ''} {user.lastname or ''}".strip() or user.username or 'Valued Customer',
                "phone": user.phone or '',
                "email": user.email or '',
                "role": 'customer' if 'customer' in (user.roles or '').lower() else 'employee'
            })
        
        return jsonify({
            "total_recipients": len(filtered_users),
            "preview_count": len(preview_users),
            "preview": preview_data
        }), 200
        
    except Exception as e:
        print(f"❌ Preview error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@guest.route("/bulk_message/delete/<int:message_id>", methods=["DELETE"])
@flask_praetorian.auth_required
def delete_bulk_message(message_id):
    """
    Delete a bulk message and its recipients
    """
    try:
        current_user = flask_praetorian.current_user()
        company_name = current_user.company_name
        
        bulk_message = BulkMessage.query.filter_by(
            id=message_id
        ).first()
        
        if not bulk_message:
            return jsonify({"error": "Message not found"}), 404
        
        # Delete all recipients first
        MessageRecipient.query.filter_by(bulk_message_id=message_id).delete()
        
        # Delete the bulk message
        db.session.delete(bulk_message)
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "Bulk message deleted successfully"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Delete error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@guest.route("/bulk_message/resend/<int:message_id>", methods=["POST"])
@flask_praetorian.auth_required
def resend_bulk_message(message_id):
    """
    Resend a failed bulk message
    """
    try:
        current_user = flask_praetorian.current_user()
        company_name = current_user.company_name
        
        bulk_message = BulkMessage.query.filter_by(
            id=message_id
        ).first()
        
        if not bulk_message:
            return jsonify({"error": "Message not found"}), 404
        
        # Get all failed recipients
        failed_recipients = MessageRecipient.query.filter_by(
            bulk_message_id=message_id,
            status='failed'
        ).all()
        
        if not failed_recipients:
            return jsonify({"error": "No failed recipients to resend"}), 404
        
        # Reset status for failed recipients
        for recipient in failed_recipients:
            recipient.status = 'pending'
            recipient.sent = False
            recipient.error_message = None
        
        # Update bulk message status
        bulk_message.status = 'pending'
        db.session.commit()
        
        # Send messages
        send_messages_background(bulk_message.id)
        
        return jsonify({
            "success": True,
            "message": f"Resending to {len(failed_recipients)} failed recipients",
            "data": {
                "bulk_id": bulk_message.id,
                "recipient_count": len(failed_recipients)
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Resend error: {str(e)}")
        return jsonify({"error": str(e)}), 500