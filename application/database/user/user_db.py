from application.extensions.extensions import *
from application.settings.setup import app
from application.settings.settings import *
from flask_migrate import Migrate



# from application.database.user.user_db import User

#========  Room database =================#
db = SQLAlchemy(app)
# with app.app_context():
#         db.create_all()
# 
migrate = Migrate(app, db)

class User(db.Model):
    id = db.Column(db.Integer,primary_key =True)
    username = db.Column(db.String(255),unique=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    city = db.Column(db.String(255))
    country = db.Column(db.String(255))
   
    about = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    email = db.Column(db.String(255),unique=True)
    address = db.Column(db.String(255))
    hashed_password = db.Column(db.Text)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default="true")
    created_date = db.Column(db.String(255))
    gender = db.Column(db.String(255))

    city=db.Column(db.String(300))
     
    
 
    created_date=db.Column(db.String(300))

  
    @property
    def identity(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has an ``identity`` instance
        attribute or property that provides the unique id of the user instance
        """
        return self.id

    @property
    def rolenames(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has a ``rolenames`` instance
        attribute or property that provides a list of strings that describe the roles
        attached to the user instance
        """
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @property
    def password(self):
        """
        *Required Attribute or Property*

        flask-praetorian requires that the user class has a ``password`` instance
        attribute or property that provides the hashed password assigned to the user
        instance
        """
        return self.hashed_password

    @classmethod
    def lookup(cls, username):
        """
        *Required Method*

        flask-praetorian requires that the user class implements a ``lookup()``
        class method that takes a single ``username`` argument and returns a user
        instance if there is one that matches or ``None`` if there is not.
        """
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        """
        *Required Method*

        flask-praetorian requires that the user class implements an ``identify()``
        class method that takes a single ``id`` argument and returns user instance if
        there is one that matches or ``None`` if there is not.
        """
        return cls.query.get(id)

    def is_valid(self):
        return self.is_active




    messaging_by = db.relationship('Messager',foreign_keys='Messager.reciever_id',
    backref='messaging_find',lazy=True)

    room_by  = db.relationship('RoomType', 
    foreign_keys ='RoomType.created_by_id',
    backref = 'sender',
    lazy=True
    
    )
    lonie_by  = db.relationship('Loan', 
    foreign_keys ='Loan.created_by_id',
    backref = 'loan',
    lazy=True
    
    )

    rooms_by  = db.relationship('Rooms', 
    foreign_keys ='Rooms.created_by_id',
    backref = 'roomie',
    lazy=True
    
    )
    insurie  = db.relationship('Insurance', 
    foreign_keys ='Insurance.created_by_id',
    backref = 'insurancee',
    lazy=True
    
    )

    ssbugeter  = db.relationship('Budget', 
    foreign_keys ='Budget.created_by_id',
    backref = 'budhetIBud',
    lazy=True)
    
    income  = db.relationship('Income', 
    foreign_keys ='Income.created_by_id',
    backref = 'incm',
    lazy=True)

    expnses  = db.relationship('Expenses', 
    foreign_keys ='Expenses.created_by_id',
    backref = 'expnsss',
    lazy=True)
                 
    transaction_for  = db.relationship('Transaction', 
    foreign_keys ='Transaction.created_by_id',
    backref = 'transiee',
    lazy=True
    
    )
    guest_for  = db.relationship('Guests', 
    foreign_keys ='Guests.created_by_id',
    backref = 'guuu',
    lazy=True
    
    )
    # todo_by  = db.relationship('Todo', 
    # foreign_keys ='Todo.created_by_id',
    # backref = 'todie',
    # lazy=True
    
    # )

    booking_by  = db.relationship('Booking', 
    foreign_keys ='Booking.created_by_id',
    backref = 'bookie',
    lazy=True
    
    )

    
    card_for  = db.relationship('Card', 
    foreign_keys ='Card.created_by_id',
    backref = 'carding',
    lazy=True
    
    )
    
    payment_for  = db.relationship('Payment', 
    foreign_keys ='Payment.created_by_id',
    backref = 'payiee',
    lazy=True
    
    )


      
    employee_for  = db.relationship('Employee', 
    foreign_keys ='Employee.created_by_id',
    backref = 'payiee',
    lazy=True
    
    )

    
      
    attendance_for  = db.relationship('Attendance', 
    foreign_keys ='Attendance.created_by_id',
    backref = 'attendie',
    lazy=True
    
    )
          
    reservation_for  = db.relationship('Reservation', 
    foreign_keys ='Reservation.created_by_id',
    backref = 'reservie',
    lazy=True
    
    )
    
            
    item_for  = db.relationship('Item', 
    foreign_keys ='Item.created_by_id',
    backref = 'itemiie',
    lazy=True
    
    )


class Loan(db.Model):
          id= db.Column(db.Integer,primary_key=True)
          name= db.Column(db.String(400))
          car= db.Column(db.String(400))
          model= db.Column(db.String(400))
          amount= db.Column(db.String(400))
          account_number= db.Column(db.String(400))

          status= db.Column(db.String(400))
          created_date = db.Column(db.String(400))
          created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
         


class Insurance(db.Model):
      id = db.Column(db.Integer,primary_key=True)
      name = db.Column(db.String(400))
      policy_number = db.Column(db.String(400))
      email = db.Column(db.String(400))
      phone = db.Column(db.String(400))
      address = db.Column(db.String(400))
      comments = db.Column(db.String(400))
      
      status = db.Column(db.String(400))
      created_date = db.Column(db.String(400))
      created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
     

class Task(db.Model):
      id = db.Column(db.Integer,primary_key=True)
      name = db.Column(db.String(300))

class RoomReport(db.Model):
          id =db.Column(db.Integer,primary_key=True)
          room_number =db.Column(db.String(400))
          room_type =db.Column(db.String(400))
          employee =db.Column(db.String(400))
          status =db.Column(db.String(400))
          type =db.Column(db.String(400))
          description =db.Column(db.String(400))
         
          created_date =db.Column(db.String(400))
         
      

# class Message(db.Model):
#       id = db.Column(db.Integer,primary_key=True)
#       name = db.Column(db.String(400))
#       message = db.Column(db.String(400))
#       client = db.Column(db.String(400)) 
     

# class Messager(db.Model):
#       id = db.Column(db.Integer,primary_key=True)
#       name = db.Column(db.String(400))
#       message = db.Column(db.String(400))
#       client = db.Column(db.String(400)) 
     
     
  
      







class Card(db.Model):
          id = db.Column(db.Integer,primary_key=True)
          name = db.Column(db.String(400))
          card_type = db.Column(db.String(400))
          card_number = db.Column(db.String(400))
          pin = db.Column(db.String(400))    
     
          expiry_date = db.Column(db.String(400))
  

          status = db.Column(db.String(400))
          created_date =db.Column(db.String(400))
          created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))




class Messager(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    info = db.Column(db.String(5000))
    reciever_id =db.Column(db.Integer,db.ForeignKey('user.id'))
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
    



class RoomType(db.Model):
    id =db.Column(db.Integer,primary_key=True)
   
    room_type= db.Column(db.String(5000))
    base_occupancy = db.Column(db.String(5000))
    extral_bed_price=db.Column(db.String(5000))
    kids_occupancy = db.Column(db.String(5000))

    base_price=db.Column(db.String(5000))
    amenities =db.Column(db.String(5000))
    description =db.Column(db.String(5000))

    image_one =    db.Column(db.String(5000))
    image_two = db.Column(db.String(5000))
    image_three =  db.Column(db.String(5000))

    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
    



class Rooms(db.Model):
        id=db.Column(db.Integer,primary_key=True)
        room_number=db.Column(db.String(5000))
        room_type=db.Column(db.String(5000))

    
        floor=db.Column(db.String(5000))
        duration=db.Column(db.String(5000))
        reserved=db.Column(db.String(5000))
        description=db.Column(db.String(5000))
        image_one = db.Column(db.String(5000))
    
        session=db.Column(db.String(5000))
        status = db.Column(db.String(5000))
        occupied_by =  db.Column(db.String(5000))
        occupied_state =  db.Column(db.String(5000))
        assignee = db.Column(db.String(400))
        task = db.Column(db.String(400))
        date_booked = db.Column(db.String(400))
      
        created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))


class Transaction(db.Model):
          id =db.Column(db.Integer,primary_key=True)
          name =db.Column(db.String(400))
          bank_name =db.Column(db.String(400))
          branch_name =db.Column(db.String(400))
          transaction_pin =db.Column(db.String(400))
          debit_accout =db.Column(db.String(400))
          amount =db.Column(db.String(400))
          account_umber =db.Column(db.String(400))
          status =db.Column(db.String(400))
          type =db.Column(db.String(400))
          created_date =db.Column(db.String(400))
          created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))

      
      



class Guests(db.Model):
        id = db.Column(db.Integer,primary_key=True)
        room_number= db.Column(db.String(400))
        username= db.Column(db.String(400))
        email= db.Column(db.String(400))
        password= db.Column(db.String(400))
       
        dob= db.Column(db.String(400))
        country= db.Column(db.String(400))
        arrival_date = db.Column(db.String(400))
        photo = db.Column(db.String(5000))
        id_type = db.Column(db.String(400))
        id_upload= db.Column(db.String(5000))

        id_number= db.Column(db.String(400))
        checkout_date= db.Column(db.String(400))
        remark= db.Column(db.String(400))
        work= db.Column(db.String(400))
        city = db.Column(db.String(400))
        gender = db.Column(db.String(400))
        phone = db.Column(db.String(400))
        address= db.Column(db.String(400))
        first_name= db.Column(db.String(400))
        last_name= db.Column(db.String(400))
        region= db.Column(db.String(400))
        has_checkout =db.Column(db.String(400))
        bookingsa = db.relationship('Booking', backref='guest', lazy=True)
        payssan = db.relationship('Payment',backref='payta',lazy=True)
        created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))



       


class Booking(db.Model):
     id = db.Column(db.Integer,primary_key=True)
     name=db.Column(db.String(400))
     room_type=db.Column(db.String(400))
     country=db.Column(db.String(400))
    
     purpose=db.Column(db.String(400))
      
     
     departure_date=db.Column(db.String(400))
     room_type=db.Column(db.String(400))
     
     arrival_date =db.Column(db.String(400))
     adult =db.Column(db.String(400))
     children=db.Column(db.String(400))


     guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'))
     has_checkout = db.Column(db.Boolean, default=False)
     room_number=db.Column(db.String(400))
     
     status=db.Column(db.String(400))
     create_date = db.Column(db.String(400))
     created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))


class Refund(db.Model):
          id = db.Column(db.Integer,primary_key=True)
          refund_amount =  db.Column(db.String(400))  
          name = db.Column(db.String(400))
          status  = db.Column(db.String(400))
          refund_time = db.Column(db.String(400))
          
          payment_id =  db.Column(db.String(400))
          reason  = db.Column(db.String(400))
          authorized_by  = db.Column(db.String(400))
          

class Payment(db.Model):
          id = db.Column(db.Integer,primary_key=True)
          refund_amount =  db.Column(db.String(400))  
          name = db.Column(db.String(400))
          amount = db.Column(db.String(400))
          method = db.Column(db.String(400))
          room_type  = db.Column(db.String(400))
          discount  = db.Column(db.String(400))
          payment_date  = db.Column(db.String(400))
          balance=db.Column(db.String(400))

          checkin_date  = db.Column(db.String(400))
          children  = db.Column(db.String(400))
          adult  = db.Column(db.String(400))
          checkout_date  = db.Column(db.String(400))
          status  = db.Column(db.String(400))
          guest_id =db.Column(db.Integer,db.ForeignKey('guests.id'))
          created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))

class Item(db.Model):
      id = db.Column(db.Integer,primary_key=True)
      item_name=db.Column(db.String(400))
      item_type =db.Column(db.String(400))
      auth_level=db.Column(db.String(400))
      evaluation_price=db.Column(db.String(400))
      item_number=db.Column(db.String(400))
      description=db.Column(db.String(400))
      base_unit=db.Column(db.String(400))
      store_unit=db.Column(db.String(400))
      expire_date=db.Column(db.String(400))
      sales_price=db.Column(db.String(400))
      recipe=db.Column(db.String(400))
      open_price=db.Column(db.String(400))
      voided=db.Column(db.String(400))
      receiving_store=db.Column(db.String(400))
      open_item=db.Column(db.String(400))
      last_date=db.Column(db.String(400))
      last_price=db.Column(db.String(400))
      last_quantity=db.Column(db.String(400))
      created_date=db.Column(db.String(400))
      created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
    
class Employee(db.Model):
        id=db.Column(db.Integer,primary_key=True)
      
        first_name=db.Column(db.String(400))
        last_name=db.Column(db.String(400))
        email=db.Column(db.String(400))
        session=db.Column(db.String(400))
        position=db.Column(db.String(400))
        dob=db.Column(db.String(400))
        employment_date=db.Column(db.String(400))
        phone =db.Column(db.String(400))
        gender =db.Column(db.String(400))
        id_type =db.Column(db.String(400))
        id_upload=db.Column(db.String(400))
        photo=db.Column(db.String(5000))
        id_number =db.Column(db.String(400))
        address=db.Column(db.String(400))



        id_number=db.Column(db.String(400))
       
        remark=db.Column(db.String(400))
   
        city =db.Column(db.String(400))
        created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
   

class Attendance(db.Model):
        id= db.Column(db.Integer,primary_key=True)
      
        name = db.Column(db.String(400))
        attendance =db.Column(db.String(400))
        position=db.Column(db.String(400))
        created_date=db.Column(db.String(400))
        created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
  






class Reservation(db.Model):
        id=db.Column(db.Integer,primary_key=True)
        name=db.Column(db.String(400))
        adult=db.Column(db.String(400))
        arrival =db.Column(db.String(400))
        departure=db.Column(db.String(400))
        children =db.Column(db.String(400))
        phone=db.Column(db.String(400))
        email =db.Column(db.String(400))
        purpose=db.Column(db.String(400))
        room_nmber=db.Column(db.String(400))
       
     
        country =db.Column(db.String(400))
        room_type =db.Column(db.String(400))
        price =db.Column(db.String(400))
      
        created_date=db.Column(db.String(400))
        Payment_status =  db.Column(db.String(5000))
        status =  db.Column(db.String(5000))
        created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))



class Todo(db.Model):
        id=db.Column(db.Integer,primary_key=True)
      
        name = db.Column(db.String(400))
        description =db.Column(db.String(400))
        position =db.Column(db.String(400))
        created_for =db.Column(db.String(400))
        position=db.Column(db.String(400))
        created_date=db.Column(db.String(400))
        created_by= db.Column(db.String(400))







class Expenses(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(5000))
    amount = db.Column(db.String(5000))
    date = db.Column(db.String(5000))
    note = db.Column(db.String(400)) 
    # school_name = db.Column(db.String(400))
    user = db.Column(db.String(400))
    created_date = db.Column(db.String(400))
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
  
      
class Income(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(5000))
    amount = db.Column(db.String(5000))
    date = db.Column(db.String(5000))
    note = db.Column(db.String(400))
    created_date = db.Column(db.String(400))
    # school_name = db.Column(db.String(400))
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))



class Budget(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(5000))
    amount = db.Column(db.String(5000))
    type = db.Column(db.String(5000))
    note = db.Column(db.String(400))

    created_date = db.Column(db.String(400))
    # school_name = db.Column(db.String(400))
 
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
  

class Family(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(5000))
    description = db.Column(db.String(5000))
    created_date = db.Column(db.String(400))
    # school_name = db.Column(db.String(400))
    # created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))


# class Itemi(db.Model):
#     id =db.Column(db.Integer,primary_key=True)
#     name = db.Column(db.String(5000))
#     description = db.Column(db.String(5000))
#     created_date = db.Column(db.String(400))
#     Category = db.Column(db.String(5000))
#     family = db.Column(db.String(5000))
#     unit = db.Column(db.String(400))
    # school_name = db.Column(db.String(400))
    # created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))



class Iteman(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(5000))
    description = db.Column(db.String(5000))
    created_date = db.Column(db.String(400))
    Category = db.Column(db.String(5000))
    family = db.Column(db.String(5000))
    price = db.Column(db.String(400))
    unit = db.Column(db.String(400))

class Unit(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(5000))
    description = db.Column(db.String(5000))
    created_date = db.Column(db.String(400))




class Stock(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(5000))
    store = db.Column(db.String(5000))
    quantity = db.Column(db.String(5000))
    created_date = db.Column(db.String(400))


class Store(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(5000))
    Category = db.Column(db.String(5000))
    description = db.Column(db.String(5000))
    created_date = db.Column(db.String(400))



class StockTransfer(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(5000))
    department = db.Column(db.String(5000))
    quantity = db.Column(db.String(5000))
    
    created_date = db.Column(db.String(400))



class Department(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(5000))
    description = db.Column(db.String(5000))
    hod = db.Column(db.String(5000))
    created_date = db.Column(db.String(400))




class Vendor(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(5000))
    phone = db.Column(db.String(5000))
    address = db.Column(db.String(5000))
    created_date = db.Column(db.String(400))



class Category(db.Model):
    id =db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(5000))
    description = db.Column(db.String(5000))
    created_date = db.Column(db.String(400))
    # school_name = db.Column(db.String(400))
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))