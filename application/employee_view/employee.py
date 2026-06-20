from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app
# from application.forms import LoginForm
from application.database.user.user_db import db,Guests,User,Booking,Rooms,Payment,Employee,Attendance,Todo,Item,Session,SalaryTemplate,SalaryPayment,Expenses
from sqlalchemy import or_,desc,and_
from datetime import datetime
from datetime import date
from flask import session



employee = Blueprint("employee", __name__)


        
    
class employeeSchema(ma.Schema):
    class Meta:
        fields=("id","first_name","last_name","address","employment_date","checkout_date","session","city","country","id_type","id_number","id_upload","dob","gender","work","remark","phone",
                "region","email","photo","arrival_date","position")

class TodoSchema(ma.Schema):
    class Meta:
        fields=("id","name","description","created_for","created_date","position","created_by")

class SalaryTemplateSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "position", "earnings", "deductions", "created_at")

class SalaryPaymentSchema(ma.Schema):
    class Meta:
        fields = (
            "id",
            "employee_id",
            "employee_name",
            "position",
            "gross_salary",
            "total_deductions",
            "net_salary",
            "payment_method",
            "payment_date",
            "note",
            "session"
        )


class ItemSchema(ma.Schema):
    class Meta:
        fields=("id","item_name","item_type","description","open_price","open_item","last_price",
                "last_date","last_quantity","voided","recipe","created_date","base_unit","item_number",
                "evaluation_price","receiving_store","auth_level","open_item","created_date")


        
        
class PaySchema(ma.Schema):
    class Meta:
        fields=("id","name","amount","method","children","adult","payment","checkin_date","checkout_date","room_type","discount","status","payment_date")


class AttendanceSchema(ma.Schema):
    class Meta:
        fields=("id","name","attendance","position","created_date","time_in","time_out")

salary_payment_schema = SalaryPaymentSchema(many=True)
employee_schema = employeeSchema(many=True)
attendance_schema = AttendanceSchema(many=True)
salary_template_schema = SalaryTemplateSchema(many=True)
item_schema = ItemSchema(many=True)
pay_schema = PaySchema(many=True)
todo_schema= TodoSchema(many=True)

@employee.route("/get_employees",methods=["GET"])
@flask_praetorian.auth_required
def get_employees():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    emp = Employee.query.filter_by(company_name=us.company_name)
    result = employee_schema.dump(emp)
    return jsonify(result)




@employee.route("/add_employee",methods=["POST"])
@flask_praetorian.auth_required
def add_employee():
       us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    #   id_upload=request.json["id_upload"],
        #  photo=request.json["photo"],
       emp = Employee(
        first_name=request.json["first_name"],
        last_name=request.json["last_name"],
        email=request.json["email"],
        session=request.json["session"],
        position=request.json["position"],
        dob=request.json["dob"],
        employment_date=request.json["employment_date"],
        phone =request.json["phone"],
        gender =request.json["gender"],
        id_type =request.json["id_type"],
      
   
        address=request.json["address"],
        id_number=request.json["id_number"],
        remark=request.json["remark"],
        city=request.json["city"],
        created_by_id = flask_praetorian.current_user().id,company_name=us.company_name
           

       )

       db.session.add(emp)
       db.session.commit()
       resp = jsonify("success")
       resp.status_code=200
       return resp
     

@app.route("/get_employee_details/<id>",methods=["GET"])
def get_employee_details(id):
     emp  = Employee.query.filter_by(id=id).all()
     result = employee_schema.dump(emp)
     return jsonify(result)



@employee.route("/update_employee",methods=["PUT"])
@flask_praetorian.auth_required
def update_employee():
        id= request.json["id"]
        emp = Employee.query.filter_by(id=id).first()
        emp.first_name=request.json["first_name"]
        emp.last_name=request.json["last_name"]
        emp.email=request.json["email"]
        emp.session=request.json["session"]
        emp.position=request.json["position"]
        emp.dob=request.json["dob"]
        emp.employment_date=request.json["employment_date"]
        emp.phone =request.json["phone"]
        emp.gender =request.json["gender"]
     
        emp.address=request.json["address"]
        emp.remark=request.json["remark"]
        emp.city=request.json["city"]
      
           

        db.session.commit()
        resp = jsonify("success")
        resp.status_code=200
        return resp



@app.route("/delete_employee/<id>",methods=["DELETE"])
@flask_praetorian.auth_required
def delete_employee(id):
     emp  = Employee.query.filter_by(id=id).first()
   
     db.session.delete(emp)
     db.session.commit()
     resp = jsonify("success")
     resp.status_code=200
     return resp




@employee.route("/get_attendance_list",methods=["GET"])
@flask_praetorian.auth_required
def get_attendance_list():
    us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
    attd = db.session.query(Attendance).filter_by(company_name=us.company_name)
#     load = attd.order_by(desc(Attendance.created_date))
    result = attendance_schema.dump(attd)
    return jsonify(result)






@employee.route("/add_attendance",methods=["POST"])
@flask_praetorian.auth_required
def add_attendance():
       us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
       session = Session.query.filter_by(status="current").first()
       attd = Attendance(
        name=request.json["name"],
        position=request.json["position"],
        attendance=request.json["attendance"],
        created_date=datetime.now(),
        time_in = datetime.now(),
       
    
        created_by_id = flask_praetorian.current_user().id,company_name=us.company_name,session=session.open_date
           

       )

       db.session.add(attd)
       db.session.commit()
       resp = jsonify("success")
       resp.status_code=200
       return resp
     



@employee.route("/update_attendance",methods=["PUT"])
@flask_praetorian.auth_required
def update_attendance():
       id = request.json["id"]

       atd_data = Attendance.query.filter_by(id=id).first()
       atd_data.time_out =datetime.now()
       db.session.commit()
       resp = jsonify("success")
       resp.status_code=200
       return resp
     

@employee.route("/get_todo_list",methods=["GET"])
@flask_praetorian.auth_required
def get_todo():
     us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
     todoList = Todo.query.filter_by(company_name=us.company_name)
     result = todo_schema.dump(todoList)
     return jsonify(result)



@employee.route("/get_todo_detail/<id>",methods=["GET"])
@flask_praetorian.auth_required
def get_todo_detail(id):
     todoList = Todo.query.filter_by(id=id).all()
     result = todo_schema.dump(todoList)
     return jsonify(result)
     

@employee.route("/delete_todo/<id>",methods=["DELETE"])
@flask_praetorian.auth_required
def delete_todo(id):
     todoList = Todo.query.filter_by(id=id).first()
     db.session.delete(todoList)
     db.session.commit()
     resp = jsonify("success")
     resp.status_code=200
     return resp
     
     

@employee.route("/add_todo",methods=["POST"])
@flask_praetorian.auth_required
def add_todo():
     
     name = request.json["name"]
     user = User.query.filter_by(id = flask_praetorian.current_user().id).first()
     todoList = Todo(
          name = request.json["name"],
          description =request.json["description"],
          position = request.json["position"],
          created_by = user.firstname,
          created_for = name,
          created_date=datetime.now().strftime('%Y-%m-%d %H:%M'),company_name=user.company_name
          

     )

     db.session.add(todoList)
     db.session.commit()
     db.session.close()
     resp = jsonify("success")
     resp.status_code =200
     
     return resp
     



@employee.route("/update_todo",methods=["PUT"])
@flask_praetorian.auth_required
def update_todo():
     id = request.json["id"]
     todo = Todo.query.filter_by(id = id).first()
    
     todo.name = request.json["name"]
     todo.description =request.json["description"]
     todo.position = request.json["position"]
 
     todo.created_for =  request.json["name"]
    
          

     

  
     db.session.commit()
     db.session.close()
     resp = jsonify("success")
     resp.status_code =200
     
     return resp
     
     
@employee.route("/add_item",methods=["POST"])
@flask_praetorian.auth_required
def add_item():
      us = User.query.filter_by(id = flask_praetorian.current_user().id).first()

      item_name=request.json["item_name"]
      item_type =request.json["item_type"]
      auth_level=request.json["auth_level"]
      evaluation_price=request.json["evaluation_price"]
      item_number=request.json["item_number"]
      description=request.json["description"]
      base_unit=request.json["base_unit"]
      store_unit=request.json["store_unit"]
      expire_date=request.json["expire_date"]
      sales_price=request.json["sales_price"]
      recipe=request.json["recipe"]
      open_price=request.json["open_price"]
      voided=request.json["voided"]
      receiving_store=request.json["receiving_store"]
      open_item=request.json["open_item"]
      last_date=request.json["last_date"]
      last_price=request.json["last_price"]
      last_quantity=request.json["last_quantity"]
      created_date=datetime.now().strftime('%Y-%m-%d %H:%M')
      created_by_id = flask_praetorian.current_user().id
      
      itm = Item(created_by_id =created_by_id,created_date=created_date,receiving_store=receiving_store,last_date=last_date,
                 last_price=last_price,last_quantity=last_quantity,open=open_item,voided=voided,
                 expire_date=expire_date,store_unit=store_unit,recipe=recipe,open_price=open_price,sales_price=sales_price,
                 base_unit=base_unit,description=description,item_number=item_number,evaluation_price=evaluation_price,
                 auth_levl=auth_level,item_type=item_type,item_name=item_name,company_name=us.company_name)
      
      
      db.session.add(itm)
      db.session.commit()
      db.session.close()
      return 200
 
 
@employee.route("/get_item",methods=["GET"])
@flask_praetorian.auth_required
def get_item():
      us = User.query.filter_by(id = flask_praetorian.current_user().id).first()
      itm = Item.query.filyter_by(company_name=us.company_name)
      result = item_schema.dump(itm)
      return jsonify(result)
    
    
@employee.route("/create_salary_template", methods=["POST"])
@flask_praetorian.auth_required
def create_salary_template():
    data = request.get_json()
    user = flask_praetorian.current_user()

    template = SalaryTemplate(
        name=data['name'],
        position=data['position'],
        earnings=data['earnings'],
        deductions=data['deductions'],
        company_name=user.company_name
    )

    db.session.add(template)
    db.session.commit()
    return jsonify({"message": "Salary template created"}), 201

@employee.route("/get_salary_templates", methods=["GET"])
@flask_praetorian.auth_required
def get_salary_templates():
    user = flask_praetorian.current_user()
    templates = SalaryTemplate.query.filter_by(company_name=user.company_name)
    return jsonify(salary_template_schema.dump(templates))

@employee.route("/get_salary_template/<int:id>", methods=["GET"])
@flask_praetorian.auth_required
def get_salary_template(id):
    template = SalaryTemplate.query.get_or_404(id)
    return jsonify({
        "id": template.id,
        "name": template.name,
        "position": template.position,
        "earnings": template.earnings,
        "deductions": template.deductions
    })

@employee.route("/update_salary_template/<int:id>", methods=["PUT"])
@flask_praetorian.auth_required
def update_salary_template(id):
    data = request.get_json()
    template = SalaryTemplate.query.get_or_404(id)

    template.name = data['name']
    template.position = data['position']
    template.earnings = data['earnings']
    template.deductions = data['deductions']

    db.session.commit()
    return jsonify({"message": "Salary template updated"})

@employee.route("/delete_salary_template/<int:id>", methods=["DELETE"])
@flask_praetorian.auth_required
def delete_salary_template(id):
    template = SalaryTemplate.query.get_or_404(id)
    db.session.delete(template)
    db.session.commit()
    return jsonify({"message": "Salary template deleted"})
@employee.route("/bulk_pay_salary", methods=["POST"])
@flask_praetorian.auth_required
def bulk_pay_salary():
    data = request.get_json()
    user = flask_praetorian.current_user()

    template = SalaryTemplate.query.get_or_404(data['template_id'])

    employees = Employee.query.filter_by(
        position=template.position,
        company_name=user.company_name
    ).all()

    if not employees:
        return jsonify({"message": "No employees found for this template"}), 400

    # Calculate totals from template
    gross = sum(float(e['amount']) for e in template.earnings)
    deductions = sum(float(d['amount']) for d in template.deductions)
    net = gross - deductions

    payments_done = []

    for emp in employees:

        # Prevent double payment
        exists = SalaryPayment.query.filter_by(
            employee_id=emp.id,
            session=data['session'],
            company_name=user.company_name
        ).first()

        if exists:
            continue

        payment = SalaryPayment(
            employee_id=emp.id,
            employee_name=f"{emp.first_name} {emp.last_name}",
            position=emp.position,
            template_id=template.id,
            gross_salary=gross,
            total_deductions=deductions,
            net_salary=net,
            session=data['session'],
            payment_method=data.get('payment_method', 'cash'),
            company_name=user.company_name,
            created_by_id=user.id
        )

        db.session.add(payment)

        # Insert into Expenses
        expense = Expenses(
            name=f"Salary - {emp.first_name} {emp.last_name}",
            amount=str(net),
            date=datetime.utcnow().strftime('%Y-%m-%d'),
            note=f"Salary payment ({data['session']})",
            user=user.username,
            created_date=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            company_name=user.company_name,
            session=data['session'],
            subcategory="Salary",
            created_by_id=user.id
        )

        db.session.add(expense)
        payments_done.append(emp.id)

    db.session.commit()

    return jsonify({
        "message": "Bulk salary payment completed",
        "employees_paid": len(payments_done)
    }), 201
@employee.route("/salary_payment_history", methods=["GET"])
@flask_praetorian.auth_required
def salary_payment_history():
    user = flask_praetorian.current_user()
    payments = SalaryPayment.query.filter_by(
        company_name=user.company_name
    ).order_by(SalaryPayment.payment_date.desc())

    return jsonify(salary_payment_schema.dump(payments))
