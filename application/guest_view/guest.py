from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app
# from application.forms import LoginForm
from application.database.user.user_db import db,Guests,User,Booking,Rooms,Payment,Reservation
from sqlalchemy import or_,desc,and_
from datetime import datetime
from datetime import date
from flask import session



guest = Blueprint("guest", __name__)


        
        
class Guest_schema(ma.Schema):
    class Meta:
        fields=("id","first_name","last_name","address","has_checkout","checkout_date","arrival","city","country","id_type","id_number","id_upload","dob","gender","work","remark","phone",
                "region","email","username","arrival_date","checkout_date")




        
        
class PaySchema(ma.Schema):
    class Meta:
        fields=("id","name","amount","method","children","adult","payment","checkin_date","checkout_date","room_type","discount","status","payment_date")

class ReserveSchema(ma.Schema):
    class Meta:
        fields=("id","name","price","status","room_number","room_type","payment_status","arrival","departure","payment_date",
                "adult","children","purpose","departure","room_nmber","created_date","Payment_status","country")


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
    booking = Booking(name=request.json["name"],  room_type=request.json["room_type"],country=request.json["country"],
    
     purpose=request.json["purpose"],
      
     
     departure_date=request.json["departure_date"],
     
     arrival_date =request.json["arrival_date"],
     adult =request.json["adult"],
     children=request.json["children"],



     room_number=request.json["room_number"],
     
     status=request.json["status"],
     create_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
     created_by_id = flask_praetorian.current_user().id
    )
    room = Rooms.query.filter_by(room_number=room_number).first()
    guest = Guests.query.filter(Guests.first_name + ' ' +Guests.last_name == name).first()
    guest.room_number = room_number
    room.occupied_by = name
    room.occupied_state =  "occupied"
    db.session.add(booking)
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code=200
    
    return resp



@guest.route("/add_payment",methods=["POST"])
@flask_praetorian.auth_required
def add_payment():
          
          pay = Payment( name = request.json["name"],
          amount = request.json["amount"],
          method = request.json["method"],
          room_type  = request.json["room_type"],
          discount  = request.json["discount"],
          children  = request.json["children"],
          adult  = request.json["adult"],
          payment_date  = datetime.now().strftime('%Y-%m-%d %H:%M'),

          checkin_date  = request.json["checkin_date"],
          checkout_date  = request.json["checkout_date"],
          status  = request.json["status"],
          created_by_id = flask_praetorian.current_user().id
          )
          db.session.add(pay)
          db.session.commit()
          db.session.close()
          
          resp = jsonify("success")
          resp.status_code =200
          return resp
         

     

# query_list = db.session.query(Ads).filter(Ads.category=="electronics")
# #                  imb =  query_list.order_by(desc(Ads.post_on))

@guest.route("/get_payment",methods=["GET"])
@flask_praetorian.auth_required
def get_payment():
     pay = Payment.query.all()
     lst =  pay.order_by(desc(Payment.payment_date))
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
          id = request.json["id"]
          pay = Payment.query.filter_by(id=id).first()
          pay.amount = request.json["amount"]
          pay.method = request.json["method"]
          pay.room_type  = request.json["room_type"]
          pay.discount  = request.json["discount"]
          pay.children  = request.json["children"]
          pay.adult  = request.json["adult"]
        

          pay.checkin_date  = request.json["checkin_date"]
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
      

@guest.route("/checkout/<id>",methods=["PUT"])
@flask_praetorian.auth_required
def checkout(id):
  
    guest =  Guests.query.filter_by(id=id).first()
    print(guest.first_name)
    room = Rooms.query.filter_by(room_number =guest.room_number).first()
    room.occupied_by = "none"
    room.occupied_state =  "available"
    guest.has_checkout =datetime.now().strftime('%Y-%m-%d %H:%M')
    db.session.commit()
    db.session.close()
    resp= jsonify("success")
    resp.status_code=200
    return resp


@guest.route("/add_reservation",methods=["POST"])
@flask_praetorian.auth_required
def add_reservation():
        rsv = Reservation(
        adult=request.json["adult"],
        name = request.json["name"],
        arrival =request.json["arrival"],
        departure=request.json["departure"],
        children =request.json["children"],

        purpose=request.json["purpose"],
        room_type=request.json["room_type"],
        room_nmber ="Not Assigned",
        Payment_status ="Not Yet",
        status ="Pending",
       
     
        country =request.json["country"],
        price =request.json["price"],
        created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        created_by_id =flask_praetorian.current_user().id
        )
      
        db.session.add(rsv)
        db.session.commit()
        db.session.close()
        resp = jsonify("success")
        resp.status_code =200
        return resp



@guest.route("/get_reserve",methods=["GET"])
@flask_praetorian.auth_required
def get_reserve():
      rsv = db.session.query(Reservation).filter(Reservation.created_by_id ==flask_praetorian.current_user().id)
      lst = rsv.order_by(desc(Reservation.created_date))
      result = reserve_schema.dump(lst)
      return jsonify(result)


@guest.route("/get_all_reserve",methods=["GET"])
@flask_praetorian.auth_required
def get_all_reserve():
      rsv = db.session.query(Reservation).filter(Reservation.created_date)
      lst = rsv.order_by(desc(Reservation.created_date))
      result = reserve_schema.dump(lst)
      return jsonify(result)


@guest.route("/get_reserve_for/<id>",methods=["GET"])
@flask_praetorian.auth_required
def get_reserve_for(id):
      rsv = db.session.query(Reservation).filter_by(id=id).all()
      result = reserve_schema.dump(rsv)
      return jsonify(result)



@guest.route("/update_reservation",methods=["PUT"])
@flask_praetorian.auth_required
def update_reservation():
        room_number = request.josn["room_number"]
        id = request.json["id"]
        rsv = Reservation.query.filter_by(id=id).first()
        rsv.adult=request.json["adult"]
        rsv.name = request.json["name"]
        rsv.arrival =request.json["arrival"]
        rsv.departure=request.json["departure"]
        rsv.children =request.json["children"]

        rsv.purpose=request.json["purpose"]
        rsv.room_type=request.json["room_type"]
        rsv.room_nmber =request.json["room_number"]
        rsv.Payment_status =request.json["payment_status"]
        rsv.status =request.json["status"]
       
     
        rsv.country =request.json["country"]
        price =request.json["price"]

        room = Rooms.query.filter_by(room_number=room_number).first()
        room.occupied_by = request.json["name"]    
        room.occupied_state ="occupied"
        
      
        db.session.commit()
        db.session.close()
        resp = jsonify("success")
        resp.status_code =200
        return resp



@guest.route("/cancel_reservation/<id>",methods=["PUT"])
def cancel_reservation(id):
      rsv = Reservation.query.filter_by(id=id).first()
      rsv.status="Cancelled"
      
      db.session.commit()
      db.session.close()
      resp = jsonify("success")
      resp.status_code =200
      return resp