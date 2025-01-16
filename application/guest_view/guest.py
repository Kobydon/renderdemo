from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app
from sqlalchemy import Float

# from application.forms import LoginForm
from application.database.user.user_db import db,Guests,User,Booking,Rooms,Payment,Reservation,Refund,Budget,Income,Expenses,Attendance,Iteman,Family,Category,Unit,Stock,Store,StockTransfer,Department,Vendor,PurchaseOrder,PurchaseRequest,ReceivedItem,returnRequest,GOP
from sqlalchemy import or_,desc,and_
from datetime import datetime
from datetime import date
from flask import session



guest = Blueprint("guest", __name__)


        
        
class Guest_schema(ma.Schema):
    class Meta:
        fields=("id","first_name","last_name","unit","Category","family","department","price","address","has_checkout","checkout_date","arrival","city","country","id_type","id_number","id_upload","dob","gender","work","remark","phone",
                "region","email","username","arrival_date","checkout_date","guest_id","note","amount","created_date","date","type","attendace","name","description","store","quantity","hod","requested_by","item","approved_by",
                "total_cost","unit_price","store","status","Department","attendance","time_in","time_out","position","reason","voided","item_id","request_by","user")


class Refund_Schema(ma.Schema):
    class Meta:
        fields=("id","reason","refund_amount","payment_id","name","refund_time","status","authorized_by")


        
        
class PaySchema(ma.Schema):
    class Meta:
        fields=("id","name","amount","balance","method","children","adult","payment","checkin_date","checkout_date","room_type","discount","status","payment_date","guest_id")

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
    guests = Guests.query.all()
    results = guest_schema.dump(guests)

    return jsonify(results)



@guest.route("/add_expense",methods=['POST'])
@flask_praetorian.auth_required
def add_expense():
    user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    amount =request.json["amount"]
    note= request.json["note"]
    date =request.json["date"]
    usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    exp = Expenses(name=name,amount=amount,note=note,date=date,
                   user=usr,created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date)
  
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
    exp = Expenses.query.filter_by(created_by_id=user.id)
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
    room_number=request.json["room_number"]
    name=request.json["name"]
    guest_id = request.json["guest_id"]
    booking = Booking(name=request.json["name"],  room_type=request.json["room_type"],country=request.json["country"],
    
     purpose=request.json["purpose"],
      
     
     departure_date=request.json["departure_date"],
     
     arrival_date =request.json["arrival_date"],
     adult =request.json["adult"],
     children=request.json["children"],



     room_number=request.json["room_number"],
     has_checkout=False,
     
     status=request.json["status"],
     create_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
     created_by_id = flask_praetorian.current_user().id,guest_id=guest_id,
    )
    room = Rooms.query.filter_by(room_number=room_number).first()
    guest = Guests.query.filter_by(id=guest_id).first()
    guest.room_number = room_number
   
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
    amount = request.json.get("amount")
    room_number = request.json.get("room_number")
    name = request.json.get("name")
    status = request.json.get("status")
    # Create a new payment entry
    pay = Payment(
        name=name,
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
        status=status,
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
     pay = Payment.query.all()
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
    # date = request.json["date"]
    # print(date)
    refund = returnRequest.query.order_by(returnRequest.created_date)
    
    result = guest_schema.dump(refund)
    return jsonify(result)



@guest.route("/search_refund_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_refund_dates():
    date = request.json["date"]
    print(date)
    refund = Refund.query.filter(Refund.refund_time.contains(date) )
    lst = refund.order_by(desc(Refund.refund_time))
    result = refund_schema.dump(lst)
    return jsonify(result)


@guest.route("/search_return_date",methods=["POST"])
@flask_praetorian.auth_required
def search_return_date():
    date = request.json["date"]
    print(date)
    refund = returnRequest.query.filter(returnRequest.created_date.contains(date),returnRequest.status.contains("Success") )
    lst = refund.order_by(desc(returnRequest.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)




    

@guest.route("/search_purchase_date",methods=["POST"])
@flask_praetorian.auth_required
def search_purchase_date():
    date = request.json["date"]
    print(date)
    refund = PurchaseRequest.query.filter(PurchaseRequest.created_date.contains(date) )
    lst = refund.order_by(desc(PurchaseRequest.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)





@guest.route("/search_order_date",methods=["POST"])
@flask_praetorian.auth_required
def search_order_date():
    date = request.json["date"]
    print(date)
    refund = PurchaseOrder.query.filter(PurchaseOrder.created_date.contains(date) )
    lst = refund.order_by(desc(PurchaseOrder.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)


@guest.route("/search_received_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_received_dates():
    date = request.json["date"]
    # print(date)
    refund = ReceivedItem.query.filter(ReceivedItem.created_date.contains(date) )
    lst = refund.order_by(desc(ReceivedItem.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)

@guest.route("/search_stock_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_stock_dates():
    date = request.json["date"]
    # print(date)
    refund = Stock.query.filter(Stock.created_date.contains(date) )
    lst = refund.order_by(desc(Stock.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)



@guest.route("/searchdates",methods=["POST"])
@flask_praetorian.auth_required
def searchdates():
    date = request.json["date"]
    print(date)
    pay = Payment.query.filter(Payment.payment_date.contains(date) )
    lst = pay.order_by(desc(Payment.payment_date))
    result = pay_schema.dump(lst)
    return jsonify(result)

@guest.route("/search_payment_date_two", methods=["POST"])
@flask_praetorian.auth_required
def search_payment_date_two():
    # Extract the 'date' and 'date_two' from the request payload
    date = request.json.get("date")
    date_two = request.json.get("date_two")
    
    # Validate that 'date' is provided
    if not date:
        return jsonify({"error": "Date is required"}), 400
    
    # Query to find payments with balance > 0 and payment date matching either 'date' or 'date_two'
    payments = Payment.query.filter(
        or_(
            Payment.payment_date.contains(date),
            Payment.payment_date.contains(date_two)
        )
    ).filter(
        Payment.balance.cast(Float) > 0  # Ensure balance is greater than 0, casting to Float for proper comparison
    ).filter(
        Payment.payment_date != None  # Make sure payment_date is not None
    ).order_by(Payment.payment_date.desc())  # Order by payment date in descending order

    # Serialize the payment data
    result = pay_schema.dump(payments)
    
    # Return the result as JSON response
    return jsonify(result)


@guest.route("/search_payment_date", methods=["POST"])
@flask_praetorian.auth_required
def search_payment_date():
    # Extract date from the request payload
    date = request.json.get("date")
    date_two = request.json.get("date_two")
    
    if not date:
        return jsonify({"error": "Date is required"}), 400
    
    # Query to find payments with balance greater than 0, and payment date containing the given date
    payments = Payment.query.filter(
        Payment.payment_date.contains(date),
        Payment.balance.cast(Float) > 0  # Cast balance to a float for comparison
    ).order_by(Payment.payment_date.desc())

    # Serialize the payments data
    result = pay_schema.dump(payments)
    
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
    # Retrieve the guest
    booka = Booking.query.filter_by(id=id).first()
    guest = Guests.query.filter_by(id=booka.guest_id).first()
    if not guest:
        return jsonify({"error": "Guest not found"}), 404

    # Mark all bookings for this guest as checked out
    bookings = Booking.query.filter_by(id=id).all()
    for booking in bookings:
        booking.has_checkout = True

    # Calculate the total payment balance for the guest
    payments = Payment.query.filter_by(guest_id=booka.guest_id,status="success").all()
 # Convert payment.balance to an integer for summation
    total_balance = sum(int(payment.balance) for payment in payments if payment.balance and payment.balance.isdigit())
  
    print(total_balance)

    # Check if the balance is non-positive to allow checkout
    if total_balance <= 0:
        room = Rooms.query.filter_by(room_number=booka.room_number).first()
        if room:
            room.occupied_by = "none"
            room.occupied_state = "available"
        
        guest.has_checkout = datetime.now().strftime('%Y-%m-%d %H:%M')
        
        db.session.commit()  # Commit all changes

        return jsonify({"message": "Checkout successful", "balance": total_balance}), 200
    else:
        return jsonify({"error": "Outstanding balance", "balance": total_balance}), 401


@guest.route("/add_reservation", methods=["POST"])
@flask_praetorian.auth_required
def add_reservation():
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
    msg.body = email_message
    mail.send(msg)

    # Return a success response
    return jsonify("success"), 200



@guest.route("/get_reserve",methods=["GET"])
@flask_praetorian.auth_required
def get_reserve():
      rsv = db.session.query(Reservation).filter(Reservation.created_by_id ==flask_praetorian.current_user().id)
    #   lst = rsv.order_by(desc(Reservation.created_date))
      result = reserve_schema.dump(rsv)
      return jsonify(result)


@guest.route("/get_all_reserve",methods=["GET"])
@flask_praetorian.auth_required
def get_all_reserve():
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
        mail.send(msg)

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
          authorized_by=request.json["authorized_by"]
          id = request.json["id"]
          refund_amount = request.json["refund_amount"]
        #   amount= request.json["amount"]
          refund = Refund( name = request.json["name"],
          refund_amount = request.json["refund_amount"],
        #   description = request.json["description"],
          reason=request.json["reason"],
          authorized_by=request.json["authorized_by"],
          payment_id = request.json["id"],
      

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
          mail.send(msg)
          resp = jsonify("success")
          resp.status_code=200
          return resp
      
@guest.route("/get_refund", methods=["GET"])
@flask_praetorian.auth_required
def get_refund():
    # Query the Refund table, ordering by the latest refund time
    refund_list = Refund.query.order_by(Refund.refund_time.desc()).all()
    
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
                   created_date=created_date)
  
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





@guest.route("/add_item",methods=['POST'])
@flask_praetorian.auth_required
def add_item():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    description =request.json["description"]
    price= request.json["price"]
    unit =request.json["unit"]
    category= request.json["category"]
    family= request.json["family"]
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    inc = Iteman(name=name,description=description,price=price,
                   created_date=created_date,family=family,Category=category,unit=unit)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_item_list",methods=['GET'])
@flask_praetorian.auth_required
def get_item_list():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Iteman.query.all()
    result = guest_schema.dump(inc)
    return jsonify(result)



@guest.route("/get_item/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_item(id):

    inc = Iteman.query.filter_by(id=id)
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
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    description =request.json["description"]
    # price= request.json["price"]
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
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
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    description =request.json["description"]
    # price= request.json["price"]
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
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
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    description =request.json["description"]
    # price= request.json["price"]
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    inc = Unit(name=name,description=description,
                   created_date=created_date)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_unit_list",methods=['GET'])
@flask_praetorian.auth_required
def get_unit_list():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Unit.query.all()
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
                   created_date=created_date)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_budget_list",methods=['GET'])
@flask_praetorian.auth_required
def get_budget_list():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Budget.query.all()
    result = guest_schema.dump(inc)
    return jsonify(result)











@guest.route("/search_attendance_date",methods=["POST"])
@flask_praetorian.auth_required
def search_attendance_date():
    date = request.json["date"]
    # print(date)
    pay = Attendance.query.filter(Attendance.created_date.contains(date) )
    lst = pay.order_by(desc(Attendance.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)

@guest.route("/search_income_dates", methods=["POST"])
@flask_praetorian.auth_required
def search_income_dates():
    """
    Searches for income records by a specific date.
    """
    try:
        # Extract the date from the JSON request body
        date = request.json.get("date")
        
        if not date:
            return jsonify({"error": "Date is required"}), 400

        # Query the Income table for records containing the specified date
        income_records = Income.query.filter(Income.date.contains(date))

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
    date = request.json["date"]
    # print(date)
    pay = Budget.query.filter(Budget.created_date.contains(date) )
    lst = pay.order_by(desc(Budget.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)


@guest.route("/search_income_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_income_dates_two():
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
        ).order_by(desc(Income.date)).all()

        result = guest_schema.dump(pay)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred while fetching data"}), 500



@guest.route("/searchdates_two", methods=["POST"])
@flask_praetorian.auth_required
def searchdates_two():
    date = request.json.get("date")
    date_two = request.json.get("date_two")

    # if not date or not date_two:
    #     return jsonify({"error": "Both 'date' and 'datetwo' must be provided"}), 400

    try:
        pay = Payment.query.filter(
            or_(
                Payment.payment_date.contains(date),
                Payment.payment_date.contains(date_two)
            )
        ).order_by(desc(Payment.payment_date)).all()

        result = pay_schema.dump(pay)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred while fetching data"}), 500



@guest.route("/search_purchase_date_two", methods=["POST"])
@flask_praetorian.auth_required
def search_purchase_date_two():
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
        ).order_by(desc(PurchaseOrder.created_date)).all()

        result = guest_schema.dump(pay)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred while fetching data"}), 500




@guest.route("/search_refund_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_refund_dates_two():
    date = request.json.get("date")
    date_two = request.json.get("date_two")

    # if not date or not date_two:
    #     return jsonify({"error": "Both 'date' and 'datetwo' must be provided"}), 400

    try:
        pay = Refund.query.filter(
            or_(
                Refund.refund_time.contains(date),
                Refund.refund_time.contains(date_two)
            )
        ).order_by(desc(Refund.refund_time)).all()

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
    """
    Searches for expense records by a specific date.
    """
    try:
        # Extract the date from the JSON request body
        date = request.json.get("date")
        
        if not date:
            return jsonify({"error": "Date is required"}), 400

        # Query the Expenses table for records containing the specified date
        expense_records = Expenses.query.filter(Expenses.date.contains(date))

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
    """
    Searches for expense records by a specific date.
    """
    try:
        # Extract the date from the JSON request body
        date = request.json.get("date")
        
        if not date:
            return jsonify({"error": "Date is required"}), 400

        # Query the Expenses table for records containing the specified date
        gop_records = GOP.query.filter(Expenses.date.contains(date))

        # Order the results by date in descending order
        ordered_records = gop_records.order_by(desc(Expenses.date))

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
    date = request.json["date"]
    # year =request.json["year"]
    type ="expense"
    # print(date)
    pay = Budget.query.filter(Budget.term.date(date))
    lst = pay.order_by(desc(Budget.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)



@guest.route("/search_income_budget_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_income_budget_dates():
    date = request.json["date"]
    # year =request.json["year"]
    # type ="income"
    # print(date)
    pay = Budget.query.filter(Budget.date.contains(date))
    lst = pay.order_by(desc(Budget.created_date))
    result = guest_schema.dump(lst)
    return jsonify(result)





@guest.route("/search_expense_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_expense_dates_two():
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
        ).order_by(desc(Expenses.date)).all()

        result = guest_schema.dump(pay)
        return jsonify(result), 200
    except Exception as e:
        print(f"Error occurred: {e}")








@guest.route("/add_store",methods=['POST'])
@flask_praetorian.auth_required
def add_store():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    description =request.json["description"]
    category= request.json["category"]
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    inc = Store(name=name,description=description,Category=category,
                   created_date=created_date)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_store_list",methods=['GET'])
@flask_praetorian.auth_required
def get_store_list():
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
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    store =request.json["store"]
    quantity= request.json["quantity"]
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    st = Stock.query.filter_by(name=name).first()
    if st:
        st.quantity= int(st.quantity) + int(quantity)

    inc = Stock(name=name,store=store,quantity=quantity,
                   created_date=created_date)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_stock_list",methods=['GET'])
@flask_praetorian.auth_required
def get_stock_list():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Stock.query.all()
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
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    department =request.json["department"]
    quantity= request.json["quantity"]
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    inc = StockTransfer(name=name,quantity=quantity,department=department,
                   created_date=created_date)
    
    store = Stock.query.filter_by(name=name).first()
    store.quantity = int(store.quantity) - int(quantity)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_stock_transfer",methods=['GET'])
@flask_praetorian.auth_required
def get_stock_transfer():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = StockTransfer.query.all()
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
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    phone =request.json["phone"]
    address= request.json["address"]
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    inc = Vendor(name=name,address=address,phone=phone,
                   created_date=created_date)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_vendor_list",methods=['GET'])
@flask_praetorian.auth_required
def get_vendor_list():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Vendor.query.all()
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

    inc = PurchaseRequest(item=item,quantity=quantity,unit_price=unit_price,total_cost=total_cost,status=status,
                          Department=department, requested_by=requested_by,store=store,created_date=created_date)
    
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
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = PurchaseRequest.query.all()
    result = guest_schema.dump(inc)
    return jsonify(result)


@guest.route("/get_order_list",methods=['GET'])
@flask_praetorian.auth_required
def get_order_list():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = PurchaseOrder.query.all()
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
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name = request.json["name"]
    description = request.json["description"]
    hod = request.json["hod"]
    # created_date = db.Column(db.String(400))
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    inc = Department(name=name,description=description,hod=hod,
                   created_date=created_date)
  
    db.session.add(inc)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_department_list",methods=['GET'])
@flask_praetorian.auth_required
def get_department_list():
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    inc = Department.query.all()
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
    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name= request.json["name"]
    # store =request.json["store"]
    quantity= request.json["quantity"]
    
    # usr = user.firstname +" " + user.lastname
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    # st = Stock.query.filter_by(name=name).first()
    # if st:
    #     st.quantity= int(st.quantity) + int(quantity)

    itm = ReceivedItem(name=name,quantity=quantity,
                   created_date=created_date)
  
    db.session.add(itm)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code =200
    return resp



@guest.route("/get_received",methods=['GET'])
@flask_praetorian.auth_required
def get_received():    # user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    itm = ReceivedItem.query.all()
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
    item_id = request.json["id"]
    item = request.json["item"]
    qty = request.json["quantity"]
    reason = request.json["reason"]
    # itm = Iteman.query.filter_by(id=id).first()
    # itm.voided="yes"
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
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
    created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
    gop = GOP(name=name,amount=amount,note=note,date=date,
                   user=usr,created_by_id=flask_praetorian.current_user().id ,
                   created_date=created_date)
  
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
    gop = GOP.query.filter_by(created_by_id=user.id)
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







