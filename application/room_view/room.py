from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app
# from application.forms import LoginForm
from application.database.user.user_db import db,RoomType,Rooms,Booking,RoomReport,Task,Payment,User
from sqlalchemy import or_,desc,and_
from datetime import datetime
from datetime import date
from flask import session



room = Blueprint("room", __name__)


        
class PaySchema(ma.Schema):
    class Meta:
        fields=("id","name","amount","balance","method","children","adult","payment","checkin_date","checkout_date","room_type","discount","status","payment_date","guest_id")


class Room_schema(ma.Schema):
    class Meta:
        fields=("id","name","room_type","base_occupancy","extral_bed_price","kids_occupancy","base_price",
                "amenities","description","image_one","image_two","image_three","occupied_state","status","occupied_by",
                "reserved","session","duration","floor","room_number","assignee","task","guest_id","has_checkout","booking_id","created_by_id","created_date"
)



class BookingSchema(ma.Schema):
    class Meta:
        fields=("id","name","room_type", "arrival_date","departure_date","country","purpose",
                "children","adult","status","room_type","checkout_date",
                "created_date","room_number","guest_id","has_checkout","booking_id","created_by_id","created_date"
)

class ReportSchema(ma.Schema):
    class Meta:
        fields=("id","employee","description", "created_date","status","room_number","room_type","guest_id")


class TaskSchema(ma.Schema):
    class Meta:
        fields=("name","id")

room_schema = Room_schema(many=True)




pay_schema = PaySchema(many=True)


task_schema =TaskSchema(many=True)


booking_schema = BookingSchema(many=True)

report_schema = ReportSchema(many=True)



@room.route("/get_all_rooms",methods=['GET'])
@flask_praetorian.auth_required
def get_all_rooms():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    info = db.session.query(Rooms).filter_by(company_name=us.company_name)
    results =room_schema.dump(info)
    return jsonify(results)





@room.route("/add_room_type",methods =["POST"])
@flask_praetorian.auth_required
def add_room_type():
    # id =db.Column(db.Integer,primary_key=True)
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()

    type= request.json["type"]
    base_occupancy = request.json["base_occupancy"]
    extral_bed_price=request.json["extral_bed_price"]
    kids_occupancy = request.json["kids_occupancy"]

    base_occupancy=request.json["base_occupancy"]
    amenities =request.json["amenities"]
    description =request.json["description"]
    base_price = request.json["base_price"]
    # image_one =request.json["image_one"]
    # image_two =request.json["image_two"]
    # image_three = request.json["image_three"]

    created_by_id = flask_praetorian.current_user().id
    
    owner = RoomType( room_type=type,base_occupancy=base_occupancy,extral_bed_price=extral_bed_price,
           kids_occupancy=kids_occupancy ,amenities=amenities,company_name=us.company_name,
              description=description ,
              created_by_id= created_by_id,base_price=base_price
              ) 
    db.session.add(owner)
    db.session.commit()
    db.session.close()
    resp = jsonify ("success")
    resp.status_code =200

    return resp

@room.route("/add_task",methods=["POST"])
@flask_praetorian.auth_required
def add_task():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    name = request.json["name"]
    tsk = Task(name=name,company_name=us.company_name)
    db.session.add(tsk)
    db.session.commit()
    db.session.close()
    resp = jsonify ("success")
    resp.status_code =200

    return resp

@room.route("/get_task",methods=["GET"])
@flask_praetorian.auth_required
def get_task():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    tsk= Task.query.filter_by(company_name=us.company_name)
    result = task_schema.dump(tsk)
    return jsonify(result)


@room.route("/update_room_type",methods =["PUT"])
@flask_praetorian.auth_required
def update_room_type():
    # id =db.Column(db.Integer,primary_key=True)
    id = request.json["id"]
    room = RoomType.query.filter_by(id=id).first()
    room.room_type= request.json["type"]
    # room.base_occupancy = request.json["base_occupancy"]
    # room.extral_bed_price=request.json["extral_bed_price"]
    # room.kids_occupancy = request.json["kids_occupancy"]

    room.base_price=request.json["base_price"]
    room.amenities =request.json["amenities"]
    # room.description =request.json["description"]

    # room.image_one =request.json["image_one"]
    # room.image_two =request.json["image_two"]
    # room.image_three = request.json["image_three"]

    room.created_by_id = flask_praetorian.current_user().id
    
   
    db.session.commit()
    resp = jsonify ("success")
    resp.status_code =200

    return resp







@room.route("/update_room",methods =["PUT"])
@flask_praetorian.auth_required
def update_room():
    # id =db.Column(db.Integer,primary_key=True)
    id = request.json["id"]
    room = Rooms.query.filter_by(id=id).first()
    room.room_number=request.json["room_number"] 
    room.room_type=request.json["room_type"]
    room.floor=request.json["floor"]
    room.duration=request.json["duration"]
    room.reserved=request.json["reserved"]
    room.description=request.json["description"]
    # room.image_one = request.json["image_one"]
    room.session=request.json["session"]
    room.status =request.json["status"]
    # room.occupied_by = request.json["occupied_by"]
    # room.occupancy_state =  request.json["ocupancy_state"]
    room.created_by_id =  flask_praetorian.current_user().id
      
        
    # room.image_one =request.json["image_one"]
    # mydata.image_two =request.json["image_two"]
    # mydata.image_three = request.json["image_three"]

    room.created_by_id = flask_praetorian.current_user().id
    
   
    db.session.commit()
    resp = jsonify ("success")
    resp.status_code =200

    return resp





@room.route("/add_room",methods=["POST"])
@flask_praetorian.auth_required

def add_room():
        us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
        owner =Rooms( room_number=request.json["room_number"],  room_type=request.json["room_type"], 
                     floor=request.json["room_type"],company_name=us.company_name,
                      duration=request.json["duration"],
                      reserved=request.json["reserved"],
                      description=request.json["description"],
                    #   image_one = request.json["image_one"], 
                      session=request.json["session"], 
                      status = "clean",
                      occupied_by =  "none",occupied_state =  "available",
                    #   maintance_state = "good",
                    #   assignee = "not yet",
                      created_by_id =  flask_praetorian.current_user().id
      
        )

        db.session.add(owner)
        db.session.commit()
        resp = jsonify("success")
        resp.status_code=200
        return resp


@room.route("/get_rooms",methods=["GET"])
@flask_praetorian.auth_required
def get_rooms():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    rooms = db.session.query(Rooms).filter_by(company_name=us.company_name)
    results = room_schema.dump(rooms)

    return jsonify(results)


@room.route("/get_room_type",methods=["GET"])
@flask_praetorian.auth_required
def get_room_type():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    rooms = RoomType.query.filter_by(company_name=us.company_name)
    results = room_schema.dump(rooms)

    return jsonify(results)


@room.route("/get_room_details/<id>",methods=["GET"])
@flask_praetorian.auth_required
def get_room_details(id):
    rooms = db.session.query(RoomType).filter_by(id =id).all()
    results = room_schema.dump(rooms)

    return jsonify(results)


@room.route("/get_rooms_details/<id>",methods=["GET"])
@flask_praetorian.auth_required
def get_rooms_details(id):
    rooms = db.session.query(Rooms).filter_by(id =id).all()
    results = room_schema.dump(rooms)

    return jsonify(results)

@room.route("/get_by_type/<type>",methods=["GET"])
@flask_praetorian.auth_required
def get_by_type(type):
    rooms = db.session.query(Rooms).filter_by(room_type =type,occupied_state="available").all()
    results = room_schema.dump(rooms)

    return jsonify(results)


@room.route("/get_by_type_two/<type>",methods=["GET"])
@flask_praetorian.auth_required
def get_by_type_two(type):
    rooms = db.session.query(RoomType).filter_by(room_type =type).all()
    results = room_schema.dump(rooms)

    return jsonify(results)





@room.route("/delete_room_type/<id>",methods=["DELETE"])
@flask_praetorian.auth_required
def delete_room_type(id):
    room = db.session.query(RoomType).filter_by(id =id).first()
    db.session.delete(room)
    db.session.commit()
    resp = jsonify("success")
    resp.status_code=200

    return resp




@room.route("/delete_room/<id>",methods=["DELETE"])
@flask_praetorian.auth_required
def delete_room(id):
    room = db.session.query(Rooms).filter_by(id =id).first()
    db.session.delete(room)
    db.session.commit()
    resp = jsonify("success")
    resp.status_code=200

    return resp






@room.route("/get_all_bookings", methods=["GET"])
@flask_praetorian.auth_required
def get_all_bookings():
    # Fetch all bookings ordered by creation date in descending order
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    bookings = Booking.query.filter_by(company_name=us.company_name).order_by(Booking.create_date.desc()).all()
    
    # Serialize the results
    results = booking_schema.dump(bookings)

    # Return the serialized results as JSON
    return jsonify(results)


@room.route("/get_new_bookings", methods=["GET"])
@flask_praetorian.auth_required
def get_new_bookings():
    # Fetch all bookings where has_checkout is False, ordered by creation date in descending order
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    bookings = Booking.query.filter_by(has_checkout=False,company_name=us.company_name).order_by(Booking.create_date.desc()).all()
    
    # Serialize the results using the booking schema
    results = booking_schema.dump(bookings)

    # Return the serialized results as JSON
    return jsonify(results)



@room.route("/get_booking_details/<id>",methods=["GET"])
@flask_praetorian.auth_required
def get_booking_details(id):
    rooms = db.session.query(Booking).filter_by(id = id).all()
    results = booking_schema.dump(rooms)

    return jsonify(results)








@room.route("/update_booking",methods=["PUT"])
@flask_praetorian.auth_required
def update_booking():
    room_number=request.json["room_number"]
    name=request.json["name"]
    id=request.json["id"]
    booking = Booking.query.filter_by(id =id).first()
    booking.name=request.json["name"]
    booking.room_type=request.json["room_type"]
    booking.country=request.json["country"]
    
    booking.purpose=request.json["purpose"]
    day= request.json["day"]
      
     
    booking.departure_date=request.json["departure_date"]
     
    booking.arrival_date =request.json["arrival_date"]
    booking.adult =request.json["adult"]
    booking.children=request.json["children"]



    booking.room_number=request.json["room_number"]
     
    booking.status=request.json["status"]
   
    
    room = Rooms.query.filter_by(room_number=room_number).first()
    room.occupied_by = name
    room.occupied_state =  "occupied"
    
    # payie = Payment.query.filter_by(name=name).first()
    # base_p = RoomType.query.filter_by(room_type=payie.room_type).first()
    # to_pay = int(base_p.base_price) * int(day)
    # if int(payie.amount) >  to_pay:
    #     payie.balance = int(payie.amount) - to_pay
        
    # else:
    #     payie.balance = to_pay - int(payie.amount)
 
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code=200
    
    return resp




@room.route("/add_room_report",methods=["POST"])
@flask_praetorian.auth_required
def add_room_report():
          us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
          rpt = RoomReport(
                    description =request.json["description"],company_name=us.company_name,
                    room_number =request.json["room_number"],
                    room_type =request.json["room_type"],
                    employee =flask_praetorian.current_user().firstname+" "+flask_praetorian.current_user().firstname ,
                    status ="Not attended",
                    created_date =datetime.now()
          )

          db.session.add(rpt)
          db.session.commit()
          db.session.close()
          resp = jsonify("success")
          resp.status_code=200
          return resp
       

@room.route("/get_room_report",methods=["GET"])
@flask_praetorian.auth_required
def get_room_report():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    rpt = RoomReport.query.filter_by(company_name=us.company_name)
    results = report_schema.dump(rpt)
    return jsonify(results)



@room.route("/get_report_detail/<id>",methods=["GET"])
@flask_praetorian.auth_required
def get_report_detail(id):
    rpt = RoomReport.query.filter_by(id = id).all()
    results = report_schema.dump(rpt)
    return jsonify(results)



@room.route("/update_room_report",methods=["PUT"])
@flask_praetorian.auth_required
def update_room_report():
    id = request.json["id"]
    rpt = RoomReport.query.filter_by(id = id).first()
    rpt.status = request.json["status"]
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code=200
    return resp





@room.route("/delete_booking/<id>",methods=["DELETE"])
@flask_praetorian.auth_required
def delete_booking(id):
    book = db.session.query(Booking).filter_by(id =id).first()
    
    room = Rooms.query.filter_by(room_number=book.room_number).first()
    room.occupied_by = "none"
    room.occupied_state =  "available"
 
    
    db.session.delete(book)

    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code=200

    return resp



@room.route("/update_house",methods=["PUT"])
@flask_praetorian.auth_required
def update_house():
       req = request.get_json()
       json_data = request.json
       for  s in range(len(json_data)):
            # if json_data[s]["brand"]:
            #     name =json_data[s]["brand"]
            # if json_data[s]["sr_no"]:
            #     sr_no = json_data[s]["sr_no"]

            if json_data[s][ "id" and " room_type" and "room_number"
                and "occupancy_state" and "task_get"  and "assignee" and "status_r"]:
                
                room = Rooms.query.filter_by(id=json_data[s]["id"]).first()

                room.room_type =json_data[s]["room_type"]
                room.assignee =json_data[s]["assignee"]
                room.status = json_data[s]["status_r"]
                room.occupied_state = json_data[s]["occupancy_state"]
                room.task =json_data[s]["task"]
                print(room.task)
      
  
                db.session.commit()
                db.session.close()
       resp = jsonify("success")
       return(resp,201)
   
   
   
   
@room.route("/search_house",methods=["POST"])
@flask_praetorian.auth_required
def search_house():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    room_type = request.json["room_type"]
    room_number = request.json["room_number"]
    status = request.json["status"]
    occupancy_state =request.json["occupancy_state"]
    
    room = Rooms.query.filter(Rooms.room_number.contains(room_number ) ,Rooms.status.contains(status ),Rooms.company_name.contains(us.company_name))

    result = room_schema.dump(room)
    return jsonify(result)


   
@room.route("/search_room_date",methods=["POST"])
@flask_praetorian.auth_required
def search_room_date():
        us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
        date = request.json["date"]
        room = Rooms.query.filter(Rooms.date_booked.contains(date ) ,Rooms.company_name.contains(us.company_name))

        result = room_schema.dump(room)
        return jsonify(result)
    



@room.route("/search_room_dates_two", methods=["POST"])
@flask_praetorian.auth_required
def search_room_dates_two():
    current_user = flask_praetorian.current_user()
    us = User.query.filter_by(id=current_user.id).first()

    date = request.json.get("date")
    datetwo = request.json.get("datetwo")

    if not date or not datetwo:
        return jsonify({"error": "Both 'date' and 'datetwo' must be provided"}), 400

    try:
        room_query = Rooms.query.filter(
            func.date(Rooms.date_booked).between(date, datetwo),
            Rooms.company_name == us.company_name
        ).order_by(Rooms.date_booked.desc())

        result = room_schema.dump(room_query)
        return jsonify(result), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An error occurred while fetching data"}), 500

   
@room.route("/search_yesterday_date",methods=["POST"])
@flask_praetorian.auth_required
def search_yesterday_date():
        us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
        date = request.json["date"]
        pay = Payment.query.filter(Payment.payment_date.contains(date ),Payment.company_name.contains(us.company_name) )

        result = pay_schema.dump(pay)
        return jsonify(result)
    
    
