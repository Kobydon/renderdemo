from application.extensions.extensions import *
from application.settings.setup import app
from application.settings.settings import *


# from application.database.user.user_db import User

#========  Room database =================#
db = SQLAlchemy(app)
# with app.app_context():
#         db.create_all()
# 

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
    account_number=db.Column(db.String(300))
    transaction_pin=db.Column(db.String(300))
    
    city=db.Column(db.String(300))
     
    state=db.Column(db.String(300))
     
    premier_account=db.Column(db.String(300))
    created_date=db.Column(db.String(300))
    account_status=db.Column(db.String(300))
    gender=db.Column(db.String(300))
    photo=db.Column(db.String(4000000))
    isa_savings=db.Column(db.String(300))
    other_savings=db.Column(db.String(300))
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
    info = db.Column(db.String(4000))
    reciever_id =db.Column(db.Integer,db.ForeignKey('user.id'))
    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
    



class RoomType(db.Model):
    id =db.Column(db.Integer,primary_key=True)
   
    room_type= db.Column(db.String(4000))
    base_occupancy = db.Column(db.String(4000))
    extral_bed_price=db.Column(db.String(4000))
    kids_occupancy = db.Column(db.String(4000))

    base_price=db.Column(db.String(4000))
    amenities =db.Column(db.String(4000))
    description =db.Column(db.String(4000))

    image_one =    db.Column(db.String(4000))
    image_two = db.Column(db.String(4000))
    image_three =  db.Column(db.String(4000))

    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
    



class Rooms(db.Model):
        id=db.Column(db.Integer,primary_key=True)
        room_number=db.Column(db.String(4000))
        room_type=db.Column(db.String(4000))

    
        floor=db.Column(db.String(4000))
        duration=db.Column(db.String(4000))
        reserved=db.Column(db.String(4000))
        description=db.Column(db.String(4000))
        image_one = db.Column(db.String(4000))
    
        session=db.Column(db.String(4000))
        status = db.Column(db.String(4000))
        occupied_by =  db.Column(db.String(4000))
        occupied_state =  db.Column(db.String(4000))
        # assignee = db.Column(db.String(400))
        # maintance_state = db.Column(db.String(400))

      
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
        photo = db.Column(db.String(4000))
        id_type = db.Column(db.String(400))
        id_upload= db.Column(db.String(4000))

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



     room_number=db.Column(db.String(400))
     
     status=db.Column(db.String(400))
     create_date = db.Column(db.String(400))
     created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))



class Payment(db.Model):
          id = db.Column(db.Integer,primary_key=True)
                
          name = db.Column(db.String(400))
          amount = db.Column(db.String(400))
          method = db.Column(db.String(400))
          room_type  = db.Column(db.String(400))
          discount  = db.Column(db.String(400))
          payment_date  = db.Column(db.String(400))

          checkin_date  = db.Column(db.String(400))
          children  = db.Column(db.String(400))
          adult  = db.Column(db.String(400))
          checkout_date  = db.Column(db.String(400))
          status  = db.Column(db.String(400))
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
        photo=db.Column(db.String(4000))
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

        purpose=db.Column(db.String(400))
        room_nmber=db.Column(db.String(400))
       
     
        country =db.Column(db.String(400))
        room_type =db.Column(db.String(400))
        price =db.Column(db.String(400))
        created_date=db.Column(db.String(400))
        Payment_status =  db.Column(db.String(4000))
        status =  db.Column(db.String(4000))
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