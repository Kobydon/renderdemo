from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app
# from application.forms import LoginForm
from application.database.user.user_db import db,RoomType,Rooms,Booking,RoomReport,Task
from sqlalchemy import or_,desc,and_
from datetime import datetime
from datetime import date
from flask import session



room = Blueprint("room", __name__)


        
        
class Room_schema(ma.Schema):
    class Meta:
        fields=("id","name","room_type","base_occupancy","extral_bed_price","kids_occupancy","base_price",
                "amenities","description","image_one","image_two","image_three","occupied_state","status","occupied_by",
                "reserved","session","duration","floor","room_number"
)



class BookingSchema(ma.Schema):
    class Meta:
        fields=("id","name","room_type", "arrival_date","departure_date","country","purpose",
                "children","adult","status","room_type","checkout_date"
                "created_date","room_number"
)

class ReportSchema(ma.Schema):
    class Meta:
        fields=("id","employee","description", "created_date","status","room_number","room_type")


class TaskSchema(ma.Schema):
    class Meta:
        fields=("name","id")

room_schema = Room_schema(many=True)






task_schema =TaskSchema(many=True)


booking_schema = BookingSchema(many=True)

report_schema = ReportSchema(many=True)



@room.route("/get_all_rooms",methods=['GET'])
@flask_praetorian.auth_required
def get_all_rooms():
    info = db.session.query(Rooms).all()
    results =room_schema.dump(info)
    return jsonify(results)





@room.route("/add_room_type",methods =["POST"])
@flask_praetorian.auth_required
def add_room_type():
    # id =db.Column(db.Integer,primary_key=True)

    type= request.json["type"]
    base_occupancy = request.json["base_occupancy"]
    extral_bed_price=request.json["extral_bed_price"]
    kids_occupancy = request.json["kids_occupancy"]

    base_occupancy=request.json["base_occupancy"]
    amenities =request.json["amenities"]
    description =request.json["description"]

    image_one =request.json["image_one"]
    # image_two =request.json["image_two"]
    # image_three = request.json["image_three"]

    created_by_id = flask_praetorian.current_user().id
    
    owner = RoomType( room_type=type,base_occupancy=base_occupancy,extral_bed_price=extral_bed_price,
           kids_occupancy=kids_occupancy ,amenities=amenities,
              description=description ,image_one=image_one,
              created_by_id= created_by_id
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
    name = request.json["name"]
    tsk = Task(name=name)
    db.session.add(tsk)
    db.session.commit()
    db.session.close()
    resp = jsonify ("success")
    resp.status_code =200

    return resp

@room.route("/get_task",methods=["GET"])
@flask_praetorian.auth_required
def get_task():
    tsk= Task.query.all()
    result = task_schema.dump(tsk)
    return jsonify(result)


@room.route("/update_room_type",methods =["PUT"])
@flask_praetorian.auth_required
def update_room_type():
    # id =db.Column(db.Integer,primary_key=True)
    id = request.json["id"]
    room = RoomType.query.filter_by(id=id).first()
    room.room_type= request.json["type"]
    room.base_occupancy = request.json["base_occupancy"]
    room.extral_bed_price=request.json["extral_bed_price"]
    room.kids_occupancy = request.json["kids_occupancy"]

    room.base_price=request.json["base_price"]
    room.amenities =request.json["amenities"]
    room.description =request.json["description"]

    room.image_one =request.json["image_one"]
    room.image_two =request.json["image_two"]
    room.image_three = request.json["image_three"]

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
      
        
    room.image_one =request.json["image_one"]
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
        owner =Rooms( room_number=request.json["room_number"],  room_type=request.json["room_type"], 
                     floor=request.json["room_type"],
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
    rooms = db.session.query(Rooms).filter_by(created_by_id = flask_praetorian.current_user().id).all()
    results = room_schema.dump(rooms)

    return jsonify(results)


@room.route("/get_room_type",methods=["GET"])
@flask_praetorian.auth_required
def get_room_type():
    rooms = db.session.query(RoomType).filter_by(created_by_id=flask_praetorian.current_user().id).all()
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






@room.route("/get_all_bookings",methods=["GET"])
@flask_praetorian.auth_required
def get_all_bookings():
    rooms = db.session.query(Booking).filter(Booking.create_date,Booking.created_by_id==flask_praetorian.current_user().id)
    lst = rooms.order_by(desc(Booking.create_date))
    results = booking_schema.dump(lst)

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
      
     
    booking.departure_date=request.json["departure_date"]
     
    booking.arrival_date =request.json["arrival_date"]
    booking.adult =request.json["adult"]
    booking.children=request.json["children"]



    booking.room_number=request.json["room_number"]
     
    booking.status=request.json["status"]
   
    
    room = Rooms.query.filter_by(room_number=room_number).first()
    room.occupied_by = name
    room.occupied_state =  "occupied"
 
    db.session.commit()
    db.session.close()
    resp = jsonify("success")
    resp.status_code=200
    
    return resp




@room.route("/add_room_report",methods=["POST"])
@flask_praetorian.auth_required
def add_room_report():
          rpt = RoomReport(
                    description =request.json["description"],
                    room_number =request.json["room_number"],
                    room_type =request.json["room_type"],
                    employee =flask_praetorian.current_user().firstname+" "+flask_praetorian.current_user().firstname ,
                    status ="Not attended",
                    created_date =datetime.now().strftime('%Y-%m-%d %H:%M')
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
    rpt = RoomReport.query.all()
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


