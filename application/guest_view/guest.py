from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app

import json
# from application.forms import LoginForm
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
        return jsonify({"error": "Both date and datetwo are requireds"}), 400

    try:
        # Convert to datetime range covering full days
        start_date = datetime.combine(datetime.strptime(date, "%Y-%m-%d"), time.min)
        end_date = datetime.combine(datetime.strptime(datetwo, "%Y-%m-%d"), time.max)

        # Query HeldCart with filtering
        held_orders = HeldCart.query.filter(
            HeldCart.session >= start_date,
            HeldCart.session <= end_date,
            HeldCart.company_name == user.company_name,HeldCart.paid_status=="pending"
        ).order_by(desc(HeldCart.session)).all()

        # Deserialize 'items' field before returning JSON response
        result = []
        for order in held_orders:
            try:
                order_items = json.loads(order.items)
            except json.JSONDecodeError:
                order_items = []

            result.append({
                "id": order.id,
                "company_name": order.company_name,
                "created_at": order.created_at,
                "status": order.status,
                "total": order.total,
                "waiter": order.waiter,
                "items": order_items,
                "customer": order.customer,
             "phone": order.phone  
            })

        return jsonify(result), 200

    except Exception as e:
        print(f"Error occurred: {e}")
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
        return jsonify({"error": "An error occurred while fetching data"}), 500


@guest.route("/search_waiter_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_waiter_dates():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    waiter =request.json["waiter"]
    
    # print(date)
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



@guest.route("/get_income_list",methods=['GET'])
@flask_praetorian.auth_required
def get_income_list():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Income.query.all()
    result = guest_schema.dump(inc)
    return jsonify(result)



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
    inc = Iteman(name=name,description=description,price=price,quantity="0",is_vip=wholesale,
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
        query = HeldCart.query.filter_by(company_name=us.company_name)
        
        # Date range filter
        if date_from and date_to:
            from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
            to_date = datetime.strptime(date_to, '%Y-%m-%d').date()
            to_date = to_date + timedelta(days=1)  # Include end date
            query = query.filter(HeldCart.created_at >= from_date, HeldCart.created_at <= to_date)
        elif date_from:
            from_date = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(HeldCart.created_at >= from_date)
        elif date_to:
            to_date = datetime.strptime(date_to, '%Y-%m-%d').date()
            to_date = to_date + timedelta(days=1)
            query = query.filter(HeldCart.created_at <= to_date)
        
        # Waiter filter
        if waiter:
            query = query.filter(HeldCart.waiter == waiter)
        
        # Cashier filter (stored in waiter field or separate field)
        if cashier:
            query = query.filter(HeldCart.waiter == cashier)
        
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
    print("Received data:", data)  # Debugging log
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

# @guest.route('/create_orders', methods=['POST'])
# @flask_praetorian.auth_required
# def create_orders():
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
        
#         # Ensure amount_paid doesn't exceed total
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
#                 table=data.get('table', '')
#             )
#             db.session.add(order_item)

#             # Calculate prorated amount for each item based on payment ratio
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

#             # Update held cart if exists
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
#         print(f"Error in create_orders: {str(e)}")
#         return jsonify({"error": str(e)}), 500


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
        # If amount_paid is provided, subtract it from total
        if amount_paid > 0:
            new_balance = total - amount_paid
        else:
            # If no payment, balance is the total (full amount owed)
            new_balance = total

        # If there was an existing balance, add it to the new balance
        if existing_balance > 0:
            new_balance = new_balance + existing_balance

        # Ensure balance is not negative
        if new_balance < 0:
            new_balance = 0

        if existing_hold:
            try:
                existing_items = json.loads(existing_hold.items)
            except json.JSONDecodeError:
                existing_items = []

            existing_items_dict = {int(item['id']): item for item in existing_items}
            updated_items = []

            # Keep confirmed items and add/update unconfirmed items
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
            existing_hold.balance = str(new_balance)  # ✅ Update balance
            existing_hold.contain_drink = "yes" if contain_drink else "no"
            existing_hold.contain_food = "yes" if contain_food else "no"
            existing_hold.contain_dtf = "yes" if contain_dtf else "no"
            existing_hold.contain_digital_printing = "yes" if contain_digital_printing else "no"
            existing_hold.contain_large_format = "yes" if contain_large_format else "no"
            existing_hold.contain_label = "yes" if contain_label else "no"

            # Update status based on balance
            if new_balance <= 0:
                existing_hold.status = "Confirmed"
                existing_hold.paid_status = "Success"
            else:
                existing_hold.status = "Pending"
                existing_hold.paid_status = "Pending"

            # Update customer if provided
            if data.get('customer'):
                existing_hold.customer = data.get('customer')
            
            # Update note if provided
            if data.get('note'):
                existing_hold.note = data.get('note')
            
            # Update table if provided
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
                balance="0",  # ✅ Set initial balance
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
                session=session.open_date if session else None,
                table=data.get('table', ''),
                note=note
            )
            db.session.add(existing_hold)
            db.session.flush()
            order_id = existing_hold.id

        db.session.commit()
        
        return jsonify({
            "message": "Order held successfully",
            "id": order_id,
            "order_id": order_id,
            "balance": str(new_balance),  # ✅ Return balance in response
            "total": str(total),
            "amount_paid": str(amount_paid)
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error in hold_order: {str(e)}")
        return jsonify({"error": "An error occurred while holding the order", "details": str(e)}), 500


# ========# ===================== CREATE ORDERS WITH BALANCE =====================
# ===================== CREATE ORDERS WITH CORRECT BALANCE =====================
# ===================== CREATE ORDERS WITH CORRECT BALANCE AND STATUS =====================
# ===================== CREATE ORDERS WITH BALANCE PAYMENT SUPPORT =====================

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
                # Get the total from the held cart
                held_cart_total = float(held_cart.total) if held_cart.total else 0
                
                # Get existing balance from held cart
                try:
                    existing_balance = float(held_cart.balance) if held_cart.balance else 0
                    print(f"🔍 DEBUG: existing_balance={existing_balance}")
                except (ValueError, TypeError):
                    existing_balance = 0
                
                # ✅ CORRECT BALANCE CALCULATION WITH BALANCE PAYMENT SUPPORT
                if is_balance_payment and existing_balance > 0:
                    # If this is a balance payment, only pay the existing balance
                    total_amount = existing_balance
                    new_balance = existing_balance - amount_paid
                    if new_balance < 0:
                        new_balance = 0
                    balance = new_balance
                    print(f"🔍 BALANCE PAYMENT: existing_balance={existing_balance}, amount_paid={amount_paid}, new_balance={new_balance}")
                else:
                    # Normal payment - calculate against total
                    if existing_balance > 0:
                        new_balance = existing_balance - amount_paid
                    else:
                        new_balance = held_cart_total - amount_paid
                    
                    if new_balance < 0:
                        new_balance = 0
                    
                    total_amount = held_cart_total
                    balance = new_balance
                    print(f"🔍 NORMAL PAYMENT: held_cart_total={held_cart_total}, existing_balance={existing_balance}, amount_paid={amount_paid}, new_balance={new_balance}")
            else:
                # If held cart not found, use the data from request
                total_amount = float(data['total'])
                balance = total_amount - amount_paid
                if balance < 0:
                    balance = 0
        else:
            # No held cart, use data from request
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

        # ✅ UPDATE HELD CART - FIXED STATUS LOGIC
        if held_cart_id and held_cart:
            # ✅ Debug: Log before update
            print(f"🔍 BEFORE UPDATE: held_cart_id={held_cart_id}, balance={balance}, current_status={held_cart.status}, current_paid_status={held_cart.paid_status}")
            
            # Update held cart status and balance
            if balance <= 0:
                # ✅ Fully paid - mark as Success
                held_cart.status = "Confirmed"
                held_cart.paid_status = "Success"
                held_cart.balance = "0"
                print(f"✅ Held cart {held_cart_id} marked as SUCCESS (balance: {balance})")
            else:
                # ✅ Partial payment - mark as Pending
                held_cart.status = "Pending"
                held_cart.paid_status = "Pending"
                held_cart.balance = str(balance)
                print(f"⏳ Held cart {held_cart_id} marked as PENDING (balance: {balance})")
            
            # ✅ Debug: Log after update
            print(f"🔍 AFTER UPDATE: held_cart_id={held_cart_id}, status={held_cart.status}, paid_status={held_cart.paid_status}, balance={held_cart.balance}")
            
            # Update customer if provided
            if customer_obj:
                held_cart.customer = customer_name
            
            # Update note if provided
            if data.get('note'):
                held_cart.note = data.get('note')
            
            # Update table if provided
            if data.get('table'):
                held_cart.table = data.get('table')

        db.session.commit()

        # ✅ Debug: Log final response
        print(f"✅ FINAL RESPONSE: order_id={new_order.id}, balance={balance}, held_cart_status={held_cart.status if held_cart else None}, held_cart_paid_status={held_cart.paid_status if held_cart else None}")

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
        print(f"❌ Error in create_orders: {str(e)}")
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
            HeldCart.user_id == user_id,
            HeldCart.paid_status == "Pending"
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
                    "note": order.note,
                    "waiter": order.waiter,
                    "company_name": order.company_name,
                    "status": order.status,
                    "digital_printing_status": order.contain_digital_printing,
                    "working_on": order.working_on,
                    "working_on_id": order.working_on_id,
                    "created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format the datetime
                })

        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON for order {order.id}: {e}")  # Debugging

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
            filtered_items = [item for item in items if item.get("family") == "digital_printing" and item.get("confirmed") == True]  
            print(f"Filtered items for order {order.id}:", filtered_items)  # Debugging

            if filtered_items:  # Only include orders with unconfirmed food items
                orders_list.append({
                    "id": order.id,
                    "items": filtered_items,
                    "total": order.total,
                    "note": order.note,
                    "waiter": order.waiter,
                     "working_on_id": order.working_on_id,
                     "working_on": order.working_on,
                    "company_name": order.company_name,
                    "status": order.status,
                    "created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format the datetime
                })

        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON for order {order.id}: {e}")  # Debugging

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
                    "waiter": order.waiter,
                    "company_name": order.company_name,
                    "status": order.status,
                     "working_on_id": order.working_on_id,
                     "working_on": order.working_on,
                    "large_format_status": order.contain_large_format
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
            filtered_items = [item for item in items if item.get("family") == "large_format" and item.get("confirmed") == True]
            print(f"Filtered items for order {order.id}:", filtered_items)

            if filtered_items:
                orders_list.append({
                    "id": order.id,
                    "items": filtered_items,
                    "total": order.total,
                    "note": order.note,
                    "waiter": order.waiter,
                    "company_name": order.company_name,
                    "working_on": order.working_on,
                    "working_on_id": order.working_on_id,
                    "status": order.status,
                    "created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format the datetime
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
                    "waiter": order.waiter,
                    "company_name": order.company_name,
                    "status": order.status,
                    "working_on": order.working_on,
                    "working_on_id": order.working_on_id,
                    "label_status": order.contain_label
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
            filtered_items = [item for item in items if item.get("family") == "label" and item.get("confirmed") == True]
            print(f"Filtered items for order {order.id}:", filtered_items)

            if filtered_items:
                orders_list.append({
                   "id": order.id,
                    "items": filtered_items,
                    "total": order.total,
                    "note": order.note,
                    "waiter": order.waiter,
                    "company_name": order.company_name,
                    "status": order.status,
                    "working_on": order.working_on,
                    "working_on_id": order.working_on_id,
                    "created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format the datetime
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
                    "waiter": order.waiter,
                    "company_name": order.company_name,
                    "status": order.status,
                    "working_on": order.working_on,
                    "working_on_id": order.working_on_id,
                    "dtf_status": order.contain_dtf
                })

        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON for order {order.id}: {e}")

    return jsonify(orders_list), 200






@guest.route('/update_delivery_status', methods=['POST'])
@flask_praetorian.auth_required
def update_delivery_status():
    try:
        data = request.json
        order_id = data.get('id')
        delivered_by = data.get('delivered_by')
        contact = data.get('contact')
        address = data.get('address')
        note = data.get('note')
        status = data.get('status', 'in_delivery')

        if not order_id:
            return jsonify({"error": "Order ID required"}), 400

        held_cart = HeldCart.query.filter_by(id=order_id).first()
        if not held_cart:
            return jsonify({"error": "Order not found"}), 404

        # Update delivery fields
        held_cart.delivered_by = delivered_by
        held_cart.delivery_contact = contact
        held_cart.delivery_address = address
        held_cart.delivery_note = note
        held_cart.delivery_status = status
        
        if status == 'delivered':
            held_cart.delivery_date = datetime.now()

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Delivery status updated",
            "order_id": order_id,
            "status": status
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error updating delivery: {str(e)}")
        return jsonify({"error": str(e)}), 500

@guest.route('/get_helding_orders_givers', methods=['GET'])
@flask_praetorian.auth_required
def get_helding_orders_givers():
    user = flask_praetorian.current_user()
    us = User.query.filter_by(id=user.id).first()

    if not us:
        return jsonify({"error": "User not found"}), 404

    # Get only pending delivery orders
    held_orders = HeldCart.query.filter_by(
        delivery_status="pending"
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
                "waiter": order.waiter,
                "company_name": order.company_name,
                "status": order.status,
                "delivery_status": getattr(order, 'delivery_status', 'pending'),
                "customer": order.customer,
                "note": order.note,
                "created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else None,
                "dtf_confirm": order.dtf_confirm,
                "working_on": order.working_on,
                "working_on_id": order.working_on_id
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
            filtered_items = [item for item in items if item.get("family") == "dtf" and item.get("confirmed") == True]
            print(f"Filtered items for order {order.id}:", filtered_items)

            if filtered_items:
                orders_list.append({
                    "id": order.id,
                    "items": filtered_items,
                    "total": order.total,
                    "note": order.note,
                    "waiter": order.waiter,
                    "company_name": order.company_name,
                    "status": order.status,
                    "created_at": order.created_at.strftime('%Y-%m-%d %H:%M:%S')  # Format the datetime
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
        email = request.json.get("phone", "").strip()
        # Validate required fields
        if not firstname or not lastname:
            resp = jsonify({"error": "Firstname and lastname are required"})
            resp.status_code = 400
            return resp
        
        # Create new customer WITHOUT customer_id
        customer = Customer(
            firstname=firstname,
            lastname=lastname,
            phone=phone,
            company_name=user.company_name,
            email=email,
            created_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
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

        start = datetime.strptime(from_date, "%Y-%m-%d")
        end = datetime.strptime(to_date, "%Y-%m-%d")

        # -----------------------------------------------------
        #                      INCOME
        # -----------------------------------------------------
        income_records = Income.query.filter(
            Income.created_date >= start,
            Income.created_date <= end
        ).all()

        total_income = sum(float(i.amount or 0) for i in income_records)

        # -----------------------------------------------------
        #                     EXPENSES
        # -----------------------------------------------------
        expense_records = Expenses.query.filter(
            Expenses.session >= start,
            Expenses.session <= end
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
        receivable_records = HeldCart.query.filter(
            HeldCart.session >= start,
            HeldCart.session <= end,
            HeldCart.paid_status == "pending"
        ).all()

        accounts_receivable = sum(float(c.total or 0) for c in receivable_records)

        # -----------------------------------------------------
        #            STOCK AVAILABLE FOR SALE (Iteman)
        #            price × quantity
        # -----------------------------------------------------
        iteman_records = Iteman.query.filter_by(is_vip="no").all()

        stock_for_sale = sum(
            float(item.price or 0) * float(item.quantity or 0)
            for item in iteman_records
        )

        # -----------------------------------------------------
        #                    STOCK IN STORE
        # -----------------------------------------------------
        stock_records = Stock.query.all()

        stock_in_store = sum(
            float(s.quantity or 0)
            for s in stock_records
        )

        # -----------------------------------------------------
        #                     NET ASSETS
        # -----------------------------------------------------
        net_assets = (
            total_income
            + accounts_receivable
            + stock_for_sale
            + stock_in_store
            - total_expenses
        )

        # -----------------------------------------------------
        #                    RETURN DATA
        # -----------------------------------------------------
        return jsonify({
            "date": to_date,
            "income_total": total_income,
            "accounts_receivable": accounts_receivable,
            "stock_for_sale": stock_for_sale,
            "stock_in_store": stock_in_store,
            "total_expenses": total_expenses,
            "net": net_assets,
            "expense_groups": grouped_expenses,
            "expense_totals": category_totals
        })

    except Exception as e:
        print("Balance sheet error:", str(e))
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
@guest.route('/sales_report', methods=['POST'])
@flask_praetorian.auth_required
def sales_report():
    try:
        user = current_user()
        data = request.json
        
        # Get date range from request
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        
        # Build query - include both Success and Pending paid_status
        query = HeldCart.query.filter_by(
            user_id=user.id,
            company_name=user.company_name
        ).filter(
            HeldCart.paid_status.in_(['Success', 'Pending'])
        )
        
        # Apply date filter if provided
        if date_from and date_to:
            from_date = datetime.strptime(date_from, '%Y-%m-%d')
            to_date = datetime.strptime(date_to, '%Y-%m-%d')
            to_date_end = to_date + timedelta(days=1) - timedelta(seconds=1)
            query = query.filter(
                HeldCart.created_at >= from_date,
                HeldCart.created_at <= to_date_end
            )
        elif date_from:
            from_date = datetime.strptime(date_from, '%Y-%m-%d')
            query = query.filter(HeldCart.created_at >= from_date)
        elif date_to:
            to_date = datetime.strptime(date_to, '%Y-%m-%d')
            to_date_end = to_date + timedelta(days=1) - timedelta(seconds=1)
            query = query.filter(HeldCart.created_at <= to_date_end)
        
        # Get all matching orders
        orders = query.all()
        
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
            date_key = order.created_at.strftime('%Y-%m-%d') if order.created_at else 'unknown'
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
                'created_at': order.created_at.isoformat() if order.created_at else None
            })
        
        # Prepare response
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
            'daily_breakdown': daily_sales,
            'orders': [
                {
                    'id': order.id,
                    'total': order.total,
                    'balance': order.balance or "0",
                    'customer': order.customer or 'Walk-in',
                    'created_at': order.created_at.isoformat() if order.created_at else None,
                    'paid_status': order.paid_status,
                    'table': order.table,
                    'waiter': order.waiter,
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
        order = HeldCart.query.get_or_404(order_id)
        order.working_on = flask_praetorian.current_user().firstname + " " + flask_praetorian.current_user().lastname
        order.working_on_id = str(flask_praetorian.current_user().id)
        db.session.commit()
        return jsonify({"message": "Order accepted successfully"}), 200
    except Exception as e:
        print(f"Error in accept_order: {str(e)}")
        return jsonify({"error": str(e)}), 500