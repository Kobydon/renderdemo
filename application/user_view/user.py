from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app
# from application.forms import LoginForm
from application.database.user.user_db import User,db
from sqlalchemy import or_,desc,and_
from datetime import datetime
from datetime import date
from flask import session



user = Blueprint("user", __name__)
guard.init_app(app, User)


class User_schema(ma.Schema):
    class Meta:
        fields=("id","firstname","lastname","about","email","username","hashed_password",
                "roles","city","country","address","phone","created_date",
                "account_status",
                    "state","transaction_pin" ,"photo","company_name"
)
        







# class MessageSchema(ma.Schema):
#     class Meta:
#         fields=("id","message","client"
# )


# message_schema = MessageSchema(many=True)




user_schema=User_schema(many=True)


@user.route("/register_quick",methods=["POST"])
@flask_praetorian.auth_required
def register_quick():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    firstname =request.json["firstname"]
    username = request.json["username"]
    password = request.json["password"]
    lastname =request.json["lastname"]
    about = request.json["about"]
    country = request.json["country"]
    city = request.json["city"]

    email = request.json["email"]
    address = request.json["address"]


    role = request.json["role"]
    phone = request.json["phone"]
    # confirm_password= request.json["confirm_password"]
    hashed_password= guard.hash_password(password)
    # if password == confirm_password:
    owner = User(firstname=firstname,lastname=lastname,about=about,country=country,company_name=us.company_name,
                    city=city ,phone=phone,username=username,hashed_password=hashed_password,roles=role,address=address,
                    email=email,created_date=datetime.now().strftime('%Y-%m-%d %H:%M'))
    db.session.add(owner)
    db.session.commit()
    resp = jsonify ("success")
    resp.status_code =200

    return resp




@user.route("/find_cashier", methods=["POST"])
def find_cashier():
    user = User.query.filter_by(password=request.json["password"],roles="cashier").first()
    
    if user:
        return jsonify({"message": "success"}), 200  # ✅ Return JSON with status code
    
    return jsonify({"message": "unauthorized"}), 401  # ✅ Return JSON with status code

@user.route("/register", methods=["POST"])
def register():
    try:
        firstname = request.json["firstname"]
        username = request.json["username"]
        password = request.json["password"]
        lastname = request.json["lastname"]
        company_name = request.json["company_name"]
        email = request.json["email"]
        role = request.json["role"]

        hashed_password = guard.hash_password(password)

        owner = User(
            firstname=firstname,
            lastname=lastname,
            username=username,
            hashed_password=hashed_password,
            roles=role,
            company_name=company_name,
            email=email,
            created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
        )

        db.session.add(owner)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 200

    except Exception as e:
        db.session.rollback()  # Rollback in case of an error
        return jsonify({"error": str(e)}), 500

    finally:
        db.session.close()  # Ensure the session is closed

@user.route('/get_signin_client',methods=['GET','POST'] )
#@login_required

def get_signin_client(): 
    
        req = request.get_json(force=True)
        username = req.get("username", None)
        password = req.get("password", None)
        # owner= User.query.filter_by(username=username).first()
       
        
        user = guard.authenticate(username,password)
        
        ret = {"id_token": guard.encode_jwt_token(user)}


     
        return ( ret,200)


@user.route("/get_info",methods=['GET'])
@flask_praetorian.auth_required
def get_info():
    info = db.session.query(User).filter_by(id=flask_praetorian.current_user().id).all()
    results =user_schema.dump(info)
    return jsonify(results)




@user.route("/get_users",methods=['GET'])
@flask_praetorian.auth_required
def get_users():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    info = db.session.query(User).filter_by(company_name=us.company_name)
    results =user_schema.dump(info)
    return jsonify(results)

@user.route("/delete_user/<id>",methods=['DELETE'])
@flask_praetorian.auth_required
def delete_user(id):
    # id = request.json["id"]
    info = db.session.query(User).filter_by(id=id).first()
    db.session.delete(info)
    db.session.commit()
    res = jsonify("sucess")
    res.status_code=200
    return res




@user.route("/get_user_details/<id>",methods=['GET'])
@flask_praetorian.auth_required
def get_user_details(id):
    # id = request.json["id"]
    info = db.session.query(User).filter_by(id=id).all()
    results =user_schema.dump(info)
    return jsonify(results)




@user.route("/update_user_profile",methods=['PUT'])
@flask_praetorian.auth_required
def update_user_profile():
    
            id = request.json["id"]

            # firstname =request.json["firstname"]
            # about =request.json["about"]
            # lastname =request.json["lastname"]
            # phone =  request.json["phone"]
            # username = request.json["username"]
            # password = request.json["password"]
            # country = request.json["country"]
            # city =  request.json["city"]
            # address = request.json["address"]
            # email = request.json["email"]
            password = request.json["password"]

            user = User.query.filter_by(id=id).first()
            user.firstname =request.json["firstname"]
            user.about =request.json["about"]
            user.lastname =request.json["lastname"]
            user.phone =  request.json["phone"]
            user.username = request.json["username"]
            password = request.json["password"]
            user.country = request.json["country"]
            user.city =  request.json["city"]
            user.address = request.json["address"]
            user.email = request.json["email"]
            user.roles =  request.json["role"]
         
    
    
     
            # user.gender=request.json["gender"]
            # user.photo=request.json["photo"]
           
            user.hashed_password =  guard.hash_password(password)
            db.session.commit()
            res = jsonify("sucess")
            res.status_code=200
            return res


