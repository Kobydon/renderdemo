from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app
# from application.forms import LoginForm
from application.database.user.user_db import db,Guests,User,Booking,Rooms,Payment,Reservation,Refund
from sqlalchemy import or_,desc,and_
from datetime import datetime
from datetime import date
from flask import session



guest = Blueprint("guest", __name__)


        
        
class Guest_schema(ma.Schema):
    class Meta:
        fields=("id","first_name","last_name","address","has_checkout","checkout_date","arrival","city","country","id_type","id_number","id_upload","dob","gender","work","remark","phone",
                "region","email","username","arrival_date","checkout_date","guest_id")


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



# @guest.route("/add_expense",methods=['POST'])
# @flask_praetorian.auth_required
# def add_expense():
#     user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
#     name= request.json["name"]
#     amount =request.json["amount"]
#     note= request.json["note"]
#     date =request.json["date"]
#     usr = user.firstname +" " + user.lastname
#     created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
#     exp = Expenses(name=name,amount=amount,note=note,date=date,
#                    user=usr,created_by_id=flask_praetorian.current_user().id ,
#                    created_date=created_date)
  
#     db.session.add(exp)
#     db.session.commit()
#     db.session.close()
#     resp = jsonify("success")
#     resp.status_code =200
#     return resp



# @guest.route("/get_expense_list",methods=['GET'])
# @flask_praetorian.auth_required
# def get_expense_list():
#     user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
#     exp = Expenses.query.filter_by(created_by_id=user.id)
#     result = guest_schema.dump(exp)
#     return jsonify(result)



# @guest.route("/get_expense/<id>",methods=['GET'])
# @flask_praetorian.auth_required
# def get_expense(id):

#     exp = Expenses.query.filter_by(id=id)
#     result = guest_schema.dump(exp)
#     return jsonify(result)




# @guest.route("/update_expense",methods=['PUT'])
# @flask_praetorian.auth_required
# def update_expense():
#     id = request.json["id"]
#     sub_data = Expenses.query.filter_by(id=id).first()
#     sub_data.name = request.json["name"]
#     sub_data.amount =request.json["amount"]
#     sub_data.note = request.json["note"]
#     sub_data.date =request.json["date"]
#     db.session.commit()
#     db.session.close()
#     resp = jsonify("success")
#     resp.status_code =201
#     return resp

# @guest.route("/delete_expense/<id>",methods=['DELETE'])
# @flask_praetorian.auth_required
# def delete_expense(id):
#       sub_data = Expenses.query.filter_by(id=id).first()
      
#       db.session.delete(sub_data)
#       db.session.commit()
#       db.session.close()
#       resp = jsonify("success")
#       resp.status_code =201
#       return resp






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
        status="success",
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



@guest.route("/search_refund_dates",methods=["POST"])
@flask_praetorian.auth_required
def search_refund_dates():
    date = request.json["date"]
    print(date)
    refund = Refund.query.filter(Refund.refund_time.contains(date) )
    lst = refund.order_by(desc(Refund.refund_time))
    result = refund_schema.dump(lst)
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







@guest.route("/update_payment",methods=["PUT"])
@flask_praetorian.auth_required
def update_payment():
          amount = request.json["amount"]
          id = request.json["id"]
          pay = Payment.query.filter_by(id=id).first()
          pay.amount = request.json["amount"] + int(amount)
          pay.method = request.json["method"]
          pay.room_type  = request.json["room_type"]
          pay.discount  = request.json["discount"]
          pay.children  = request.json["children"]
          pay.adult  = request.json["adult"]
        

          pay.checkin_date  = request.json["checkin_date"]
          pay.balance  = int(amount) + int(pay.balance) - int(amount)
          pay.checkout_date  = request.json["checkout_date"]
          pay.status  = request.json["status"]
        #   created_by_id = flask_praetorian.current_user().id
          
     
          db.session.commit()
          db.session.close()
          
          resp = jsonify("success")
          resp.status_code =200
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
    guest = Guests.query.filter_by(id=id).first()
    if not guest:
        return jsonify({"error": "Guest not found"}), 404

    # Mark all bookings for this guest as checked out
    bookings = Booking.query.filter_by(guest_id=id).all()
    for booking in bookings:
        booking.has_checkout = True

    # Calculate the total payment balance for the guest
    payments = Payment.query.filter_by(guest_id=id).all()
    total_balance = sum(payment.balance for payment in payments)

    # Check if the balance is non-positive to allow checkout
    if total_balance <= 0:
        room = Rooms.query.filter_by(room_number=guest.room_number).first()
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

    # Fetch and update the reservation record
    rsv = Reservation.query.filter_by(id=reservation_id).first()
    if not rsv:
        return jsonify({"error": "Reservation not found"}), 404

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
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

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
    try:
        refund_amount = int(refund.refund_amount)
        payment_amount = int(payment.amount)
        if refund_amount > payment_amount:
            return jsonify({"error": "Refund amount cannot exceed payment amount"}), 400
    except ValueError:
        return jsonify({"error": "Invalid refund amount or payment amount"}), 400

    # Update the payment amount and balance
    payment.amount = payment_amount - refund_amount
    payment.balance = max(0, payment.balance - refund_amount)  # Ensure balance doesn't go negative

    # Commit changes to the database
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()

    # Create email message
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
