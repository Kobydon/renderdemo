from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app
from sqlalchemy import Float
import json
# from application.forms import LoginForm
from application.database.user.user_db import db,Guests,User,Booking,Rooms,Payment,Reservation,Refund,Budget,Income,Expenses,Attendance,Iteman,Family,Category,Unit,Stock,Store,StockTransfer,Department,Vendor,PurchaseOrder,PurchaseRequest,ReceivedItem,returnRequest,GOP,RoomType,Session,Wifi,Order,StockUsage,PosPayment,OrderItem,HeldCart,FoodChef
from sqlalchemy import or_,desc,and_
from datetime import datetime
from datetime import date
from flask import session

from collections import Counter

guest = Blueprint("guest", __name__)

class OrderSchema(ma.Schema):
    class Meta:
        fields=("id","user_id","item_name","items","total","created_at","company_name","created_at","total","waiter","order_status","order_id","waiter","status",
                "quantity",)








order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
        
class Guest_schema(ma.Schema):
    class Meta:
        fields=("id","first_name","last_name","operation","unit","category","family","open_by","department","price","address","has_checkout","checkout_date","arrival","city","country","id_type","id_number","id_upload","dob","gender","work","remark","phone",
                "region","email","username","arrival_date","checkout_date","guest_id","note","amount","created_date","date","type","attendace","name","description","store","quantity","hod","requested_by","item","approved_by",
                "total_cost","unit_price","store","status","Department","attendance","time_in","time_out","position","reason","voided","item_id","request_by","user",
                    "close_by","open_date","close_date","wifi_code","order_id","waiter","food")






class Refund_Schema(ma.Schema):
    class Meta:
        fields=("id","reason","refund_amount","payment_id","name","refund_time","status","authorized_by","session")


        
        
class PaySchema(ma.Schema):
    class Meta:
        fields=("id","name","amount","balance","method","children","adult","wifi_code","payment","checkin_date","checkout_date","room_type","discount","status","payment_date","guest_id","booking_id","session","code","attendant")

class ReserveSchema(ma.Schema):
    class Meta:
        fields=("id","name","price","status","room_number","room_type","payment_status","arrival","departure","payment_date",
                "adult","children","purpose","departure","room_nmber","created_date","Payment_status","country","email","phone")

refund_schema = Refund_Schema(many=True)
guest_schema = Guest_schema(many=True)

pay_schema = PaySchema(many=True)

reserve_schema =ReserveSchema(many=True)





@guest.route("/add_guest",methods=["POST"])
@flask_praetorian.auth_required

def add_guest():
        us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
        username= request.json["username"]
        email= request.json["email"]
        password= request.json["password"]
        hashed_password= guard.hash_password(password)
        first_name= request.json["first_name"]
        last_name= request.json["last_name"]
        country= request.json["country"]
        address= request.json["address"]
        city = request.json["city"]
        
        phone = request.json["phone"]
       
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
        user =User(username=username,email=email,hashed_password=hashed_password,roles="guest",
                   created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),  firstname= first_name, lastname=last_name,
        country= country,address= address,
        city = city,  phone = phone,company_name=us.company_name)
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
    guests = Guests.query.filter_by(company_name=us.company_name)
    results = guest_schema.dump(guests)

    return jsonify(results)



@guest.route("/add_expense",methods=['POST'])
@flask_praetorian.auth_required
def add_expense():
    # us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    amount =request.json["amount"]
    note= request.json["note"]
    date =request.json["date"]
    usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    exp = Expenses(name=name,amount=amount,note=note,date=date,
                   user=usr,created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date,company_name=user.company_name)
  
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


@guest.route("/confirm_oder",methods=['PUT'])
@flask_praetorian.auth_required
def confirm_oder():
    id = request.json["id"]
    sub_data = HeldCart.query.filter_by(id=id).first()
    if sub_data:
        sub_data.status="Confirmed"
    db.session.commit()
    resp = jsonify("success")
    resp.status_code =201
    return resp





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
    if session:
        open_date=session.open_date
    room_number=request.json["room_number"]
    name=request.json["name"]
    guest_id = request.json["guest_id"]
    booking = Booking(name=request.json["name"],  room_type=request.json["room_type"],country=request.json["country"],session=open_date,
    
     purpose=request.json["purpose"],
      
     
     departure_date=request.json["departure_date"],
     
     arrival_date =request.json["arrival_date"],
     adult =request.json["adult"],
     children=request.json["children"],



     room_number=request.json["room_number"],
     has_checkout=False,
     
     status=request.json["status"],
     create_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
     created_by_id = flask_praetorian.current_user().id,guest_id=guest_id,company_name=us.company_name
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
    if session:
        open_date=session.open_date
    amount = request.json.get("amount")
    room_number = request.json.get("room_number")
    name = request.json.get("name")
    status = request.json.get("status")
    booking_id = request.json.get("booking_id")
    days = request.json["days"]  # Use .get() to avoid KeyError
    
    if not days:
        return jsonify({"error": "Missing 'days' in request"}), 400  # Return error if days is missing

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
        payment_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        checkin_date=request.json.get("checkin_date"),
        checkout_date=request.json.get("checkout_date"),
        status=status,booking_id=booking_id,session=open_date,
        created_by_id=flask_praetorian.current_user().id,company_name=us.company_name)
    
    inc = Income(
            amount=amount,
            date=datetime.now().strftime('%Y-%m-%d'),
            note=request.json.get("room_type"),
            created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
            created_by_id=flask_praetorian.current_user().id
        )


    # Update room status
    room = Rooms.query.filter_by(room_number=room_number).first()
    if room:
        room.occupied_by = name
        room.occupied_state = "occupied"
        room.date_booked = datetime.now().strftime('%Y-%m-%d %H:%M')

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
    payment_date = datetime.now().strftime('%Y-%m-%d %H:%M')

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
    mail.send(msg)

    # Return a success response
    return jsonify("success"), 200


     
     

# query_list = db.session.query(Ads).filter(Ads.category=="electronics")
# #                  imb =  query_list.order_by(desc(Ads.post_on))

@guest.route("/get_payment",methods=["GET"])
@flask_praetorian.auth_required
def get_payment():
     us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
     pay = Payment.query.filter_by(company_name=us.company_name)
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
    refund = returnRequest.query.filter_by(company_name=us.company_name).order_by(returnRequest.created_date)
    
    result = guest_schema.dump(refund)
    return jsonify(result)



@guest.route("/search_stock_usuage",methods=["POST"])
@flask_praetorian.auth_required
def search_stock_usuage():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    print(date)
    refund = StockUsage.query.filter(StockUsage.created_date.contains(date) ,StockUsage.company_name.contains(us.company_name))
    lst = refund.order_by(desc(StockUsage.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)


@guest.route("/search_refund_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_refund_dates():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    print(date)
    refund = Refund.query.filter(Refund.session.contains(date) ,Refund.company_name.contains(us.company_name))
    lst = refund.order_by(desc(Refund.session))
    result = refund_schema.dump(lst)
    return jsonify(result)


@guest.route("/search_return_date",methods=["POST"])
@flask_praetorian.auth_required
def search_return_date():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    print(date)
    refund = returnRequest.query.filter(returnRequest.created_date.contains(date),returnRequest.status.contains("Success") ,
                                        returnRequest.company_name.contains(us.company_name))
    lst = refund.order_by(desc(returnRequest.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)




    

@guest.route("/search_purchase_date",methods=["POST"])
@flask_praetorian.auth_required
def search_purchase_date():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    print(date)
    refund = PurchaseRequest.query.filter(PurchaseRequest.created_date.contains(date),PurchaseRequest.company_name.contains(us.company_name) )
    lst = refund.order_by(desc(PurchaseRequest.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)





@guest.route("/search_order_date",methods=["POST"])
@flask_praetorian.auth_required
def search_order_date():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    print(date)
    refund = PurchaseOrder.query.filter(PurchaseOrder.created_date.contains(date) ,PurchaseOrder.company_name.contains(us.company_name))
    lst = refund.order_by(desc(PurchaseOrder.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)


@guest.route("/search_received_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_received_dates():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
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
    refund = Stock.query.filter(Stock.created_date.contains(date) ,Stock.company_name.contains(us.company_name))
    lst = refund.order_by(desc(Stock.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)



@guest.route("/searchdates",methods=["POST"])
@flask_praetorian.auth_required
def searchdates():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    print(date)
    pay = Payment.query.filter(Payment.session.contains(date),Payment.company_name.contains(us.company_name) )
    lst = pay.order_by(desc(Payment.session))
    result = pay_schema.dump(lst)
    return jsonify(result)



@guest.route("/search_held_order_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_held_order_dates():
    # Get the current user
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Get date from request
    date = request.json.get("date")
    if not date:
        return jsonify({"error": "Date is required"}), 400

    # Query HeldCart with filtering
    held_orders = HeldCart.query.filter(
        HeldCart.created_at.contains(date),
        HeldCart.company_name == user.company_name
    ).order_by(desc(HeldCart.created_at)).all()

    # Deserialize 'items' field before returning JSON response
    result = []
    for order in held_orders:
        try:
            order_items = json.loads(order.items)  # Convert string to list
        except json.JSONDecodeError:
            order_items = []  # Handle bad JSON data gracefully
        
        result.append({
            "id": order.id,
            "company_name": order.company_name,
            "created_at": order.created_at,
            "status": order.status,
            "total": order.total,
            "waiter": order.waiter,
            "items": order_items  # Now 'items' is a proper list
        })

    return jsonify(result), 200


@guest.route("/searchdates_pos",methods=["POST"])
@flask_praetorian.auth_required
def searchdates_pos():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json["date"]
    # print(date)
    pay = PosPayment.query.filter(PosPayment.payment_date.contains(date),PosPayment.company_name.contains(us.company_name) )
    lst = pay.order_by(desc(PosPayment.payment_date))
    result = pay_schema.dump(lst)
    return jsonify(result)



@guest.route("/search_payment_date_two", methods=["POST"])
@flask_praetorian.auth_required
def search_payment_date_two():
    # Extract the 'date' and 'date_two' from the request payload
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json.get("date")
    date_two = request.json.get("date_two")
    
    # Validate that 'date' is provided
    if not date:
        return jsonify({"error": "Date is required"}), 400
    
    # Query to find payments with balance > 0 and payment date matching either 'date' or 'date_two'
    payments = Payment.query.filter(
        or_(
            Payment.session.contains(date),
            Payment.session.contains(date_two)
        )
    ).filter(
        Payment.balance.cast(Float) > 0  # Ensure balance is greater than 0, casting to Float for proper comparison
    ).filter(
        Payment.session != None  # Make sure payment_date is not None
    ).filter(Payment.company_name.conatins(us.company_name)).order_by(Payment.session.desc())  # Order by payment date in descending order

    # Serialize the payment data
    result = pay_schema.dump(payments)
    
    # Return the result as JSON response
    return jsonify(result)


@guest.route("/search_payment_date", methods=["POST"])
@flask_praetorian.auth_required
def search_payment_date():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # Extract date from the request payload
    date = request.json.get("date")
    date_two = request.json.get("date_two")
    
    if not date:
        return jsonify({"error": "Date is required"}), 400
    
    # Query to find payments with balance greater than 0, and payment date containing the given date
    payments = Payment.query.filter(
        Payment.session.contains(date),Payment.company_name.contains(us.company_name),
        Payment.balance.cast(Float) > 0  # Cast balance to a float for comparison
    ).order_by(Payment.session.desc())

    # Serialize the payments data
    result = pay_schema.dump(payments)
    
    # Return the results as JSON
    return jsonify(result)




@guest.route("/search_payment_held_date", methods=["POST"])
@flask_praetorian.auth_required
def search_payment_held_date():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    # Extract date from the request payload
    date = request.json.get("date")
    date_two = request.json.get("date_two")
    
    if not date:
        return jsonify({"error": "Date is required"}), 400
    
    # Query to find payments with balance greater than 0, and payment date containing the given date
    payments = HeldCart.query.filter(
        HeldCart.created_at.contains(date),HeldCart.company_name.contains(us.company_name),
        HeldCart.total.cast(Float) > 0 ,HeldCart.status=="Pending"
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
    
    total_balance = sum(float(payment.balance) for payment in payments if payment.balance and payment.balance.replace('.', '', 1).isdigit())
    if total_balance<=0:
        book.has_checkout = True
        room.occupied_by = "none"
        room.occupied_state = "available"
        guest.has_checkout = datetime.now().strftime('%Y-%m-%d %H:%M')
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

    # Calculate the total payment balance for the guest
    payments = Payment.query.filter_by(guest_id=booking.guest_id, status="success").all()
    if not payments:
        return jsonify({"error": "No successful payments found for this guest"}), 404
    
    total_balance = sum(float(payment.balance) for payment in payments if payment.balance and payment.balance.replace('.', '', 1).isdigit())

    # Get the room details for checkout logic
    room = Rooms.query.filter_by(room_number=booking.room_number).first()
    if not room:
        return jsonify({"error": "Room not found"}), 404

    room_type = RoomType.query.filter_by(room_type=room.room_type).first()
    if not room_type:
        return jsonify({"error": "Room type not found"}), 404

    # Get current time for checkout logic
    current_time = datetime.now()
    current_time_str = current_time.strftime('%Y-%m-%d %H:%M')

    # Check if the current date is past the departure date
    departure_date = datetime.strptime(booking.departure_date, "%Y-%m-%d")
    
    # Case: Checkout after the departure date, charge for extra days
    if current_time > departure_date:
        # Calculate the extra days the guest stayed beyond the departure date
        extra_days = (current_time - departure_date).days
        
        # Apply charges for extra days
        extra_charge_per_day = 1.0 * float(room_type.base_price)  # Modify as per your pricing rules
        extra_charge = extra_days * extra_charge_per_day
        
        total_balance += extra_charge  # Add extra charge for extra days stayed
        
        # Debugging output to check extra charge calculation
        print(f"Guest stayed {extra_days} extra days. Extra charge: {extra_charge}")

    # Update the payment balance (whether for late checkout or not)
    last_payment = payments[-1]  # Assuming the last successful payment is the one to update
    last_payment.balance = str(total_balance)  # Convert total_balance back to string for storage

    # Debugging output to check balance before commit
    print(f"Updating payment balance for guest {guest.id}: {last_payment.balance}")

    try:
        db.session.commit()
    except Exception as e:
        print(f"Error during commit: {e}")
        db.session.rollback()
        return jsonify({"error": "Failed to commit changes"}), 401  # Return error response

    # Update room state and guest checkout timestamp
    room.occupied_by = "none"
    room.occupied_state = "available"
    guest.has_checkout = current_time_str
    booking.has_checkout = True

    # Commit the changes to the database again (room and guest updates)
    try:
        db.session.commit()
        print("Room and guest commit successful.")
    except Exception as e:
        print(f"Error during commit: {e}")
        db.session.rollback()
        return jsonify({"error": "Failed to commit changes"}), 401  # Return error response

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
        created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        created_by_id=flask_praetorian.current_user().id,company_name=us.company_name
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
      rsv = db.session.query(Reservation).filter(Reservation.created_by_id ==flask_praetorian.current_user().id,company_name=us.company_name)
    #   lst = rsv.order_by(desc(Reservation.created_date))
      result = reserve_schema.dump(rsv)
      return jsonify(result)


@guest.route("/get_all_reserve",methods=["GET"])
@flask_praetorian.auth_required
def get_all_reserve():
      us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
      rsv = db.session.query(Reservation).filter_by(company_name=us.company_name)

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
          refund = Refund( name = request.json["name"],session=open_date,
          refund_amount = request.json["refund_amount"],
        #   description = request.json["description"],
          reason=request.json["reason"],
          authorized_by=request.json["authorized_by"],
          payment_id = request.json["id"],company_name=us.company,
      

          status = "pending",
          refund_time =datetime.now().strftime('%Y-%m-%d %H:%M')
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
    refund_list = Refund.query.filter_by(company_name=us.company_name).order_by(Refund.refund_time.desc()).all()
    
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
    mail.send(msg)

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
    name= request.json["name"]
    amount =request.json["amount"]
    note= request.json["note"]
    date =request.json["date"]
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    inc = Income(name=name,amount=amount,note=note,date=date,
                   created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date,company_name=user.company_name)
  
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
    inc = Income.query.filter_by(company_name=us.company_name)
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
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    inc = Iteman(name=name,description=description,price=price,quantity="0",
                   created_date=created_date,family=family,category=category,unit=unit,company_name=us.company_name)
  
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
    inc = Iteman.query.filter_by(company_name=us.company_name)
    result = guest_schema.dump(inc)
    return jsonify(result)



@guest.route("/get_item/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_item(id):
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Iteman.query.filter_by(id=id,company_name=us.company_name)
    result = guest_schema.dump(inc)
    return jsonify(result)



@guest.route("/get_food/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_food(id):
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    cat = Category.query.filter_by(id=id,company_name=us.company_name).first()

    inc = Iteman.query.filter_by(category=cat.name,company_name=us.company_name)
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
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    inc = Category(name=name,description=description,
                   created_date=created_date,company_name=us.company_name)
  
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
    inc = Category.query.filter_by(company_name=us.company_name)
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
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    inc = Family(name=name,description=description,
                   created_date=created_date,company_name=us.company_name)
  
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
    inc = Family.query.filter_by(company_name=us.company_name)
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
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
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
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
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

@guest.route("/search_income_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_income_dates():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    """
    Searches for income records by a specific date.
    """
    try:
        # Extract the date from the JSON request body
        date = request.json.get("date")
        
        if not date:
            return jsonify({"error": "Date is required"}), 400

        # Query the Income table for records containing the specified date
        income_records = Income.query.filter(Income.date.contains(date),Income.company_name.contains(us.company_name))

        # Order the results by date in descending order
        ordered_records = income_records.order_by(desc(Income.date))

        # Serialize the query result
        result = guest_schema.dump(ordered_records)

        # Return the serialized data as a JSON response
        return jsonify(result), 200

    except Exception as e:
        # Handle unexpected errors
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


@guest.route("/search_income_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_income_dates_two():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json.get("date")
    date_two = request.json.get("datetwo")

    # if not date or not date_two:
    #     return jsonify({"error": "Both 'date' and 'datetwo' must be provided"}), 400

    try:
        pay = Income.query.filter(
            or_(
                Income.date.contains(date),
                Income.date.contains(date_two)
            )
        ).filter(Income.company_name.contains(us.company_name)).order_by(desc(Income.date)).all()

        result = guest_schema.dump(pay)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred while fetching data"}), 500



@guest.route("/searchdates_two", methods=["POST"])
@flask_praetorian.auth_required
def searchdates_two():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json.get("date")
    date_two = request.json.get("date_two")

    # if not date or not date_two:
    #     return jsonify({"error": "Both 'date' and 'datetwo' must be provided"}), 400

    try:
        pay = Payment.query.filter(
            or_(
                Payment.session.contains(date),
                Payment.session.contains(date_two)
            )
        ).filter(Payment.company_name.contains(us.company_name)).order_by(desc(Payment.session)).all()

        result = pay_schema.dump(pay)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred while fetching data"}), 500



@guest.route("/search_purchase_date_two", methods=["POST"])
@flask_praetorian.auth_required
def search_purchase_date_two():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json.get("date")
    date_two = request.json.get("date_two")

    # if not date or not date_two:
    #     return jsonify({"error": "Both 'date' and 'datetwo' must be provided"}), 400

    try:
        pay = PurchaseOrder.query.filter(
            or_(
                PurchaseOrder.created_date.contains(date),
                PurchaseOrder.created_date.contains(date_two)
            )
        ).filter(PurchaseOrder.company_name.contains(us.company_name)).order_by(desc(PurchaseOrder.created_date)).all()

        result = guest_schema.dump(pay)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred while fetching data"}), 500




@guest.route("/search_refund_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_refund_dates_two():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    date = request.json.get("date")
    date_two = request.json.get("date_two")

    # if not date or not date_two:
    #     return jsonify({"error": "Both 'date' and 'datetwo' must be provided"}), 400

    try:
        pay = Refund.query.filter(
            or_(
                Refund.session.contains(date),
                Refund.session.contains(date_two)
            )
        ).filter(Refund.company_name.contains(us.company_name)).order_by(desc(Refund.refund_time)).all()

        result = refund_schema.dump(pay)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred while fetching data"}), 500




# @guest.route("/search_salary_dates",methods=["POST"])
# @flask_praetorian.auth_required
# def search_salary_dates():
#     date = request.json["date"]
#     print(date)
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
                Expenses.date.contains(date),
                Expenses.date.contains(date_two)
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
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
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
    inc = Store.query.filter_by(company_name=us.company_name)
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
    name= request.json["name"]
    store =request.json["store"]
    quantity= request.json["quantity"]
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    st = Stock.query.filter_by(name=name).first()
    if st:
        st.quantity= int(st.quantity) + int(quantity)

    inc = Stock(name=name,store=store,quantity=quantity,company_name=user.company_name,
                   created_date=created_date)
    
      
    stu = StockUsage(name=name,operation="Added",store=store,quantity=quantity,created_date=created_date,company_name=user.company_name,
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
    sub_data.store= int(quantity) + int(sub_data.quantity) 
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
    name= request.json["name"]
    department =request.json["department"]
    quantity= request.json["quantity"]
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    inc = StockTransfer(name=name,quantity=quantity,department=department,
                   created_date=created_date,company_name=user.company_name)
    
    stu = StockUsage(name=name,operation="Transfer",store=department,quantity=quantity,created_date=created_date,company_name=user.company_name,
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
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
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
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')

    inc = PurchaseRequest(item=item,quantity=quantity,unit_price=unit_price,total_cost=total_cost,status=status,company_name=user.company_name,
                          department=department, requested_by=requested_by,store=store,created_date=created_date)
    
    # usr = user.firstname +" " + user.lastname

  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_purchase_list",methods=['GET'])
@flask_praetorian.auth_required
def get_purchase_list():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = PurchaseRequest.query.filter_by(company_name=user.company_name)
    result = guest_schema.dump(inc)
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

        new_order = PurchaseOrder(item=item, store=store, created_date=created_date, quantity=quantity)

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
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
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




















@guest.route("/add_received_item",methods=['POST'])
@flask_praetorian.auth_required
def add_received_item():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    # store =request.json["store"]
    quantity= request.json["quantity"]
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    # st = Stock.query.filter_by(name=name).first()
    # if st:
    #     st.quantity= int(st.quantity) + int(quantity)

    itm = ReceivedItem(name=name,quantity=quantity,company_name=user.company_name,
                   created_date=created_date)
  
    db.session.add(itm)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_received",methods=['GET'])
@flask_praetorian.auth_required
def get_received():    
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    itm = ReceivedItem.query.filter_by(company_name=us.company_name)
    result = guest_schema.dump(itm)
    return jsonify(result)




@guest.route("/update_received_item",methods=['PUT'])
@flask_praetorian.auth_required
def update_received_item():

    id = request.json["id"]
   
    sub_data = ReceivedItem.query.filter_by(id=id).first()
    sub_data.name = request.json["name"]
    sub_data.quantity= request.json["store"]
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
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    user = User.query.filter_by(id =flask_praetorian.current_user().id).first()
    request_by= user.firstname +" "+ user.lastname

    a = returnRequest(item_id=item_id,item=item,quantity=qty,reason=reason,created_date=created_date,request_by=request_by,status="Pending",company_name=us.company_name)
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
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
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
    created_date = datetime.now().strftime('%Y-%m-%d %H:%M')

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
   

    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
  
    usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
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
    session_data =  Session.query.filter_by(status="current",company_name=us.company_name).all()
    results = guest_schema.dump(session_data)
    return jsonify(results)



@guest.route("/get_all_session")
@flask_praetorian.auth_required
def get_all_session():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    session_data =  Session.query.filter_by(company_name=us.company_name).order_by(desc(Session.open_date))
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


@guest.route('/create_orders', methods=['POST'])
@flask_praetorian.auth_required
def create_orders():
    us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    data = request.json

    print("Incoming data:", data)  # ✅ Debug incoming request

    if not data or 'cartItems' not in data or 'total' not in data:
        return jsonify({"error": "Invalid request"}), 400

    # ✅ Always store valid JSON
    items = json.dumps(data.get('cartItems', []))

    new_order = Order(
        user_id=us.id,
        items=items,
        total=float(data['total']),
        company_name=us.company_name,
        waiter=us.firstname,
        order_status="Pending",
        status="paid",
     
    )
    db.session.add(new_order)
    db.session.commit()

    # ✅ Deduct Stock & Create Order Items
    for cart_item in data['cartItems']:
        item_name = cart_item.get('name')
        item_quantity = int(cart_item.get('qty', 0))
        category = cart_item.get('category')
        family = cart_item.get('family')
        price  = cart_item.get('price')
        total_price = int(price) * int(item_quantity)
        item = Iteman.query.filter_by(name=item_name).first()
        if not item:
            return jsonify({"error": f"Item '{item_name}' not found"}), 404
        if int(item.quantity) < int( item_quantity):
            return jsonify({"error": f"Not enough stock for {item_name}"}), 400
        old_quantity = int(item.quantity)


        item.quantity =   old_quantity -item_quantity  # 🔻 Deduct stock

        order_item = OrderItem(
            item_name=item_name,
            order_id=new_order.id,
            item_id=item.id,
            quantity=item_quantity,
            category=category,
            waiter=us.firstname + " " + us.lastname,
            status="Pending",
            company_name=us.company_name,   created_date=datetime.now().strftime('%Y-%m-%d %H:%M') ,
            family =family
        )

        pos_payment = PosPayment(company_name=us.company_name,name=item_name,amount=total_price,
                                 quantity=item_quantity,attendant=us.firstname +" "+us.lastname,created_by_id=us.id,
                                 payment_date=datetime.now().strftime('%Y-%m-%d %H:%M'))
        

        income = Income(name=item_name + "-"+ us.firstname +" "+us.lastname,amount =total_price,date =datetime.now().strftime('%Y-%m-%d %H:%M'),
                        note="Pos Payment",company_name=us.company_name,created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
                        created_by_id=us.id)

    

        
        db.session.add(pos_payment)
        db.session.add(income)
        db.session.add(order_item)
        db.session.commit()



       

  

    return jsonify({
        "id": new_order.id,
        "company_name": new_order.company_name,
        "created_at": new_order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        "items": items,
        "order_status": new_order.order_status,
        "total": new_order.total,
        "user_id": new_order.user_id,
        "waiter": new_order.waiter
    }), 201


@guest.route('/get_orders', methods=['GET'])
@flask_praetorian.auth_required
def get_orders():
    user = flask_praetorian.current_user()
    orders = OrderItem.query.filter_by(company_name=user.company_name,family="food").order_by(OrderItem.id.desc()).all()
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

@guest.route('/hold_order', methods=['POST'])
@flask_praetorian.auth_required
def hold_order():
    user = flask_praetorian.current_user()
    data = request.json

    # Validate request body
    if not data or 'id' not in data or 'cartItems' not in data or 'total' not in data:
        return jsonify({"error": "Invalid request"}), 400

    hold_id = int(data['id'])  # Get hold ID

    try:
        existing_hold = HeldCart.query.filter_by(user_id=user.id, status="Pending", id=hold_id).first()

        if existing_hold:
            existing_items = json.loads(existing_hold.items)
            new_items = data['cartItems']

            item_dict = {item['id']: item for item in existing_items}

            for new_item in new_items:
                new_item_id = new_item['id']
                new_item_qty = int(new_item['qty'])

                if new_item_id in item_dict:
                    item_dict[new_item_id]['qty'] = new_item_qty
                else:
                    new_item['qty'] = new_item_qty
                    item_dict[new_item_id] = new_item

            existing_hold.items = json.dumps(list(item_dict.values()))
            existing_hold.total = data['total']
        else:
            for item in data['cartItems']:
                item['qty'] = int(item['qty'])

            existing_hold = HeldCart(
                user_id=user.id,
                items=json.dumps(data['cartItems']),
                total=float(data['total']),
                company_name=user.company_name,
                status="Pending",
                waiter=f"{user.firstname} {user.lastname}"
            )
            db.session.add(existing_hold)

        db.session.commit()
        return jsonify({"message": "Order held successfully", "id": existing_hold.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while holding the order", "details": str(e)}), 500



@guest.route('/held_orders/<id>', methods=['GET'])
@flask_praetorian.auth_required
def get_held_orders(id):
    user_id = flask_praetorian.current_user().id
    held_orders = HeldCart.query.filter_by(user_id=user_id).all()
    return jsonify(orders_schema.dump(held_orders))

@guest.route('/get_helding_orders', methods=['GET'])
@flask_praetorian.auth_required
def get_helding_orders():
    user = flask_praetorian.current_user()
    us = User.query.filter_by(id=user.id).first()
    
    held_orders = HeldCart.query.filter_by(status="Pending", company_name=us.company_name).all()
    orders_list = []

    for order in held_orders:
        items = json.loads(order.items)  # Convert JSON string to list
        filtered_items = [item for item in items if item.get("family") == "food"]  # Filter items by family
        
        if filtered_items:  # Only include orders that have food items
            orders_list.append({
                "id": order.id,
                "items": filtered_items,
                "total": order.total,
                "waiter": order.waiter,
                "company_name": order.company_name,
                "status": order.status
            })

    return jsonify(orders_list)


@guest.route('/get_helding_orders_drinks', methods=['GET'])
@flask_praetorian.auth_required
def get_helding_orders_drinks():
    user = flask_praetorian.current_user()
    us = User.query.filter_by(id=user.id).first()
    
    held_orders = HeldCart.query.filter_by(status="Pending", company_name=us.company_name).all()
    orders_list = []

    for order in held_orders:
        items = json.loads(order.items)  # Convert JSON string to list
        filtered_items = [item for item in items if item.get("family") == "drink"]  # Filter items by family
        
        if filtered_items:  # Only include orders that have drink items
            orders_list.append({
                "id": order.id,
                "items": filtered_items,
                "total": order.total,
                "waiter": order.waiter,
                "company_name": order.company_name,
                "status": order.status
            })

    return jsonify(orders_list)



    


@guest.route('/remove_held_order/<int:hold_id>', methods=['DELETE'])
@flask_praetorian.auth_required
def remove_held_order(hold_id):
    held_order = HeldCart.query.get(hold_id)
    if not held_order:
        return jsonify({"error": "Held order not found"}), 404

    db.session.delete(held_order)
    db.session.commit()

    return jsonify({"message": f"Held order {hold_id} removed"}), 200


@guest.route('/load_held_order/<int:hold_id>', methods=['GET'])
@flask_praetorian.auth_required
def load_held_order(hold_id):
    held_order = HeldCart.query.get(hold_id)
    if not held_order:
        return jsonify({"error": "Held order not found"}), 404

    return jsonify({
        "id": held_order.id,
        "items": json.loads(held_order.items),
        "total": held_order.total
    }), 200


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
        items=json.dumps(merged_items),
        total=total,
        company_name=flask_praetorian.current_user().company_name
    )
    db.session.add(new_held)

    # Delete old held carts
    for order in orders:
        db.session.delete(order)

    db.session.commit()
    return jsonify({"message": "Orders merged successfully", "id": new_held.id}), 200




@guest.route("/search_most_item", methods=["POST"])
@flask_praetorian.auth_required
def search_most_item():
    user = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    date = request.json.get("date")

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not date:
        return jsonify({"error": "Date is required"}), 400

    # Query OrderItem instead of Order to get item details directly
    order_items = OrderItem.query.filter(
        OrderItem.created_date.contains(date),
        OrderItem.company_name == user.company_name
    ).all()

    # Count occurrences of each item_name
    item_counts = Counter(item.item_name for item in order_items)

    # Convert to a list of dictionaries for JSON response
    result = [{"name": name, "count": count} for name, count in item_counts.most_common()]

    return jsonify(result), 200





@guest.route("/search_most_attendant", methods=["POST"])
@flask_praetorian.auth_required
def search_most_attendant():
    us = User.query.filter_by(id=flask_praetorian.current_user().id).first()
    date = request.json.get("date")

    if not date:
        return jsonify({"error": "Date is required"}), 400

    # Query orders from the given date
    orders = Order.query.filter(
        Order.created_at.contains(date), 
        Order.company_name == us.company_name
    ).all()

    # Count appearances of each attendant (assuming 'attendant' is a string field)
    attendant_counts = Counter(order.waiter for order in orders if order.waiter)

    # Convert to a list of dictionaries for JSON response
    result = [{"waiter": waiter, "count": count} for waiter, count in attendant_counts.most_common()]

    return jsonify(result), 200





@guest.route("/add_chef",methods=['POST'])
@flask_praetorian.auth_required
def add_chef():

    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    food =request.json["food"]
    
    date =request.json["date"]
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    inc = FoodChef(name=name,food=food,date=date,
                   created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date,company_name=user.company_name)
  
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
    inc = FoodChef.query.filter_by(company_name=us.company_name)
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


