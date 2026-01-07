from application.extensions.extensions import *
from application.settings.setup import app
from application.settings.settings import *
from flask_migrate import Migrate
from datetime import datetime, timezone



# from application.database.user.user_db import User

#========  Room database =================#
db = SQLAlchemy(app)
# with app.app_context():
#         db.create_all()
# 
migrate = Migrate(app, db)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    firstname = db.Column(db.String(255))
    company_name= db.Column(db.String(500))  
    lastname = db.Column(db.String(255))
    city = db.Column(db.String(300))  # Changed to 300 if needed
    country = db.Column(db.String(255))
    last_login = db.Column(db.String(255))
    last_logout = db.Column(db.String(255))
    about = db.Column(db.Text)  # Changed to Text for larger content
    phone = db.Column(db.String(20))  # Adjusted for phone length
    email = db.Column(db.String(255), unique=True)
    address = db.Column(db.Text)  # Changed to Text for address
    hashed_password = db.Column(db.Text)
    roles = db.Column(db.Text)  # Changed to Text to store multiple roles
    is_active = db.Column(db.Boolean, default=True)
    created_date = db.Column(db.DateTime)  # Changed to DateTime if you're storing dates
    gender = db.Column(db.String(50))  # Adjusted size

    # Relationships
    messaging_by = db.relationship('Messager', foreign_keys='Messager.reciever_id',
                                   backref='messaging_find', lazy=True)
    room_by = db.relationship('RoomType', foreign_keys='RoomType.created_by_id',
                              backref='sender', lazy=True)
    lonie_by = db.relationship('Loan', foreign_keys='Loan.created_by_id',
                               backref='loan', lazy=True)
    rooms_by = db.relationship('Rooms', foreign_keys='Rooms.created_by_id',
                               backref='roomie', lazy=True)
    insurie = db.relationship('Insurance', foreign_keys='Insurance.created_by_id',
                              backref='insurancee', lazy=True)
    ssbugeter = db.relationship('Budget', foreign_keys='Budget.created_by_id',
                                backref='budhetIBud', lazy=True)
    income = db.relationship('Income', foreign_keys='Income.created_by_id',
                             backref='incm', lazy=True)
    expnses = db.relationship('Expenses', foreign_keys='Expenses.created_by_id',
                              backref='expnsss', lazy=True)
    transaction_for = db.relationship('Transaction', foreign_keys='Transaction.created_by_id',
                                      backref='transiee', lazy=True)
    guest_for = db.relationship('Guests', foreign_keys='Guests.created_by_id',
                                backref='guuu', lazy=True)
    booking_by = db.relationship('Booking', foreign_keys='Booking.created_by_id',
                                 backref='bookie', lazy=True)
    card_for = db.relationship('Card', foreign_keys='Card.created_by_id',
                               backref='carding', lazy=True)
    payment_for = db.relationship('Payment', foreign_keys='Payment.created_by_id',
                                  backref='payiee', lazy=True)
    employee_for = db.relationship('Employee', foreign_keys='Employee.created_by_id',
                                   backref='payiee', lazy=True)
    attendance_for = db.relationship('Attendance', foreign_keys='Attendance.created_by_id',
                                     backref='attendie', lazy=True)
    reservation_for = db.relationship('Reservation', foreign_keys='Reservation.created_by_id',
                                      backref='reservie', lazy=True)
    item_for = db.relationship('Item', foreign_keys='Item.created_by_id',
                               backref='itemiie', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)
    held_orders = db.relationship('HeldCart', backref='user', lazy=True)

    @property
    def identity(self):
        return self.id

    @property
    def rolenames(self):
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @property
    def password(self):
        return self.hashed_password

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    def is_valid(self):
        return self.is_active

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))  # Adjusted column size
    car = db.Column(db.String(255))  # Adjusted column size
    model = db.Column(db.String(255))  # Adjusted column size
    amount = db.Column(db.String(255))  # Adjusted column size
    account_number = db.Column(db.String(255))  # Adjusted column size
    status = db.Column(db.String(100))  # Adjusted column size
    created_date = db.Column(db.DateTime)  # Changed to DateTime for better date handling
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Insurance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))  # Adjusted column size
    policy_number = db.Column(db.String(255))  # Adjusted column size
    email = db.Column(db.String(255))  # Adjusted column size
    phone = db.Column(db.String(20))  # Adjusted column size for phone numbers
    address = db.Column(db.Text)  # Changed to Text for longer addresses
    comments = db.Column(db.Text)  # Changed to Text for comments
    status = db.Column(db.String(100))  # Adjusted column size
    created_date = db.Column(db.DateTime)  # Changed to DateTime
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name= db.Column(db.String(500))
    name = db.Column(db.String(255))  # Adjusted column size


class RoomReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name= db.Column(db.String(500))
    room_number = db.Column(db.String(100))  # Adjusted column size
    room_type = db.Column(db.String(100))  # Adjusted column size
    employee = db.Column(db.String(255))  # Adjusted column size
    status = db.Column(db.String(100))  # Adjusted column size
    type = db.Column(db.String(100))  # Adjusted column size
    description = db.Column(db.Text)  # Changed to Text for description
    created_date = db.Column(db.DateTime)  # Changed to DateTime


class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))  # Adjusted column size
    card_type = db.Column(db.String(100))  # Adjusted column size
    card_number = db.Column(db.String(20))  # Adjusted column size for card numbers
    pin = db.Column(db.String(4))  # Adjusted for PIN length
    expiry_date = db.Column(db.String(7))  # Adjusted for date format (MM/YYYY)
    status = db.Column(db.String(50))  # Adjusted column size
    created_date = db.Column(db.DateTime)  # Changed to DateTime
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Messager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.Text)  # Changed to Text for larger messages
    reciever_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class RoomType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.String(255))  # Adjusted column size
    base_occupancy = db.Column(db.String(100))  # Adjusted column size
    extral_bed_price = db.Column(db.String(100))  # Adjusted column size
    kids_occupancy = db.Column(db.String(100))  # Adjusted column size
    base_price = db.Column(db.String(100))  # Adjusted column size
    amenities = db.Column(db.String(500))  # Adjusted column size for amenities list
    description = db.Column(db.Text)  # Changed to Text for larger descriptions
    image_one = db.Column(db.String(500))  # Adjusted column size
    image_two = db.Column(db.String(500))  # Adjusted column size
    image_three = db.Column(db.String(500))  # Adjusted column size
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_name= db.Column(db.String(500))  

class Rooms(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(100))  # Adjusted column size
    room_type = db.Column(db.String(100))  # Adjusted column size
    floor = db.Column(db.String(50))  # Adjusted column size
    duration = db.Column(db.String(50))  # Adjusted column size
    reserved = db.Column(db.String(50))  # Adjusted column size
    description = db.Column(db.Text)  # Changed to Text for larger descriptions
    image_one = db.Column(db.String(500))  # Adjusted column size for image paths
    session = db.Column(db.String(50))  # Adjusted column size
    status = db.Column(db.String(50))  # Adjusted column size
    occupied_by = db.Column(db.String(100))  # Adjusted column size
    occupied_state = db.Column(db.String(50))  # Adjusted column size
    assignee = db.Column(db.String(100))  # Adjusted column size
    task = db.Column(db.String(100))  # Adjusted column size
    date_booked = db.Column(db.DateTime)  # Changed to DateTime
    company_name= db.Column(db.String(500))  
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))  # Adjusted column size
    bank_name = db.Column(db.String(255))  # Adjusted column size
    branch_name = db.Column(db.String(255))  # Adjusted column size
    transaction_pin = db.Column(db.String(6))  # Adjusted for PIN length
    debit_account = db.Column(db.String(255))  # Adjusted column size
    amount = db.Column(db.String(100))  # Adjusted column size
    account_number = db.Column(db.String(255))  # Adjusted column size
    status = db.Column(db.String(50))  # Adjusted column size
    type = db.Column(db.String(50))  # Adjusted column size
    created_date = db.Column(db.DateTime)  # Changed to DateTime
    company_name= db.Column(db.String(500))  
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Guests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.String(100))  # Adjusted column size
    company_name= db.Column(db.String(500))  
    username = db.Column(db.String(255))  # Adjusted column size
    email = db.Column(db.String(255))  # Adjusted column size
    password = db.Column(db.String(255))  # Adjusted column size
    dob = db.Column(db.String(100))  # Adjusted column size
    country = db.Column(db.String(100))  # Adjusted column size
    arrival_date = db.Column(db.String(500))  # Changed to DateTime
    photo = db.Column(db.String(500))  # Adjusted column size for image paths
    id_type = db.Column(db.String(50))  # Adjusted column size
    id_upload = db.Column(db.String(500))  # Adjusted column size for file paths
    id_number = db.Column(db.String(100))  # Adjusted column size
    checkout_date = db.Column(db.String(500))  # Changed to DateTime
    remark = db.Column(db.String(255))  # Adjusted column size
    work = db.Column(db.String(255))  # Adjusted column size
    city = db.Column(db.String(100))  # Adjusted column size
    gender = db.Column(db.String(10))  # Adjusted column size
    phone = db.Column(db.String(20))  # Adjusted column size for phone numbers
    address = db.Column(db.String(255))  # Adjusted column size
    first_name = db.Column(db.String(255))  # Adjusted column size
    last_name = db.Column(db.String(255))  # Adjusted column size
    region = db.Column(db.String(100))  # Adjusted column size
    has_checkout = db.Column(db.String(10))  # Adjusted column size
    bookingsa = db.relationship('Booking', backref='guest', lazy=True)
    payssan = db.relationship('Payment', backref='payta', lazy=True)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name= db.Column(db.String(500))  
    name = db.Column(db.String(255))  # Adjusted column size
    room_type = db.Column(db.String(100))  # Adjusted column size
    country = db.Column(db.String(100))  # Adjusted column size
    purpose = db.Column(db.String(255))  # Adjusted column size
    departure_date = db.Column(db.String(500))  # Changed to DateTime
    arrival_date = db.Column(db.String(500))  # Changed to DateTime
    adult = db.Column(db.String(10))  # Adjusted column size
    children = db.Column(db.String(10))  # Adjusted column size
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'))
    has_checkout = db.Column(db.Boolean, default=False)
    room_number = db.Column(db.String(100))  # Adjusted column size
    status = db.Column(db.String(50))  # Adjusted column size
    session = db.Column(db.String(50))  # Adjusted column size
    create_date = db.Column(db.DateTime)  # Changed to DateTime
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Refund(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name= db.Column(db.String(500))  
    refund_amount = db.Column(db.String(100))  # Adjusted column size
    name = db.Column(db.String(255))  # Adjusted column size
    status = db.Column(db.String(50))  # Adjusted column size
    refund_time = db.Column(db.DateTime)  # Changed to DateTime
    payment_id = db.Column(db.String(100))  # Adjusted column size
    reason = db.Column(db.String(255))  # Adjusted column size
    session = db.Column(db.String(50))  # Adjusted column size
    authorized_by = db.Column(db.String(255))  # Adjusted column size


class Wifi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name= db.Column(db.String(500))  
    code = db.Column(db.String(100))  # Adjusted column size
    state = db.Column(db.String(255))  # Adjusted column size]
    duration =db.Column(db.String(255)) 
  # Adjusted column size


class Session(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name= db.Column(db.String(500))  
    open_date = db.Column(db.DateTime)  # Changed to DateTime
    close_date = db.Column(db.DateTime)  # Changed to DateTime
    status = db.Column(db.String(50))  # Adjusted column size
    open_by = db.Column(db.String(255))  # Adjusted column size
    close_by = db.Column(db.String(255))  # Adjusted column size

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.String(500))  # JSON string of order items
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    company_name = db.Column(db.String(500))
    order_status = db.Column(db.String(500), default="Pending")  # Pending, Confirmed, Completed
    waiter = db.Column(db.String(500))
    status = db.Column(db.String(20), default="paid")  # Status: paid, pending
    session  =db.Column(db.String(200))

    # Relationship to OrderItem
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade="all, delete-orphan")
    
    
    
    
class Credit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(db.String(500))  # JSON string of order items
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    company_name = db.Column(db.String(500))
    order_status = db.Column(db.String(500), default="Pending")  # Pending, Confirmed, Completed
    waiter = db.Column(db.String(500))
    status = db.Column(db.String(20), default="paid")  # Status: paid, pending
    session  =db.Column(db.String(200))
    customer  =db.Column(db.String(200))
    phone  =db.Column(db.String(200))

    # Relationship to OrderItem
    


# ✅ Order Items Model
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('iteman.id'), nullable=False)  # Link to inventory
    quantity = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(500))
    waiter = db.Column(db.String(400))
    status = db.Column(db.String(500), default="Pending")  # Pending, In Progress, Completed
    item_name = db.Column(db.String(500))
    company_name = db.Column(db.String(400))
    created_date = db.Column(db.String(400))
    family =db.Column(db.String(500))
    table = db.Column(db.String(100))
    session  =db.Column(db.String(200))
    item = db.relationship('Iteman', backref=db.backref('order_items', lazy=True))


# ✅ Held Orders Model (For Holding Carts)
class HeldCart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    items = db.Column(db.String(2000000))  # JSON string of cart items
    total = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    company_name = db.Column(db.String(500))
    status = db.Column(db.String(500))
    waiter = db.Column(db.String(500))
    table = db.Column(db.String(100))
    paid_status= db.Column(db.String(500))
    onetime =db.Column(db.String(200))
    contain_food =db.Column(db.String(200))
    contain_drink =db.Column(db.String(200))
    food_confirm =db.Column(db.String(200))
    drink_confirm =db.Column(db.String(200))
    food_confirm_at= db.Column(db.String(200))
    drink_confirm_at =db.Column(db.String(200))
    session  =db.Column(db.String(200))

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name= db.Column(db.String(500))  
    refund_amount = db.Column(db.String(100))  # Adjusted column size
    name = db.Column(db.String(255))  # Adjusted column size
    amount = db.Column(db.String(100))  # Adjusted column size
    method = db.Column(db.String(50))  # Adjusted column size
    room_type = db.Column(db.String(100))  # Adjusted column size
    discount = db.Column(db.String(50))  # Adjusted column size
    payment_date = db.Column(db.String(500))  # Changed to DateTime
    balance = db.Column(db.String(100))  # Adjusted column size
    booking_id = db.Column(db.String(100))  # Adjusted column size
    checkin_date = db.Column(db.String(500))  # Changed to DateTime
    children = db.Column(db.String(10))  # Adjusted column size
    adult = db.Column(db.String(10))  # Adjusted column size
    checkout_date = db.Column(db.String(500))  # Changed to DateTime
    status = db.Column(db.String(50))  # Adjusted column size
    session = db.Column(db.String(50))  # Adjusted column size
    wifi_code = db.Column(db.String(500)) 
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'))
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))




class PosPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name= db.Column(db.String(500))  
    name = db.Column(db.String(255))  # Adjusted column size
    amount = db.Column(db.String(100))  # Adjusted column size
    payment_date = db.Column(db.String(500))  # Changed to DateTime
    attendant= db.Column(db.String(100)) 
    quantity= db.Column(db.String(100)) 
    method= db.Column(db.String(100)) 
    cashier= db.Column(db.String(100))
    customer = db.Column(db.String(400)) 
    phone = db.Column(db.String(400)) 
    
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session=db.Column(db.String(200))
    category = db.Column(db.String(200))
    cat  =db.Column(db.String(200))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name= db.Column(db.String(500))  
    item_name = db.Column(db.String(255))  # Adjusted column size
    item_type = db.Column(db.String(100))  # Adjusted column size
    auth_level = db.Column(db.String(50))  # Adjusted column size
    evaluation_price = db.Column(db.String(100))  # Adjusted column size
    item_number = db.Column(db.String(100))  # Adjusted column size
    description = db.Column(db.Text)  # Changed to Text for larger descriptions
    base_unit = db.Column(db.String(50))  # Adjusted column size
    store_unit = db.Column(db.String(50))  # Adjusted column size
    expire_date = db.Column(db.DateTime)  # Changed to DateTime
    sales_price = db.Column(db.String(100))  # Adjusted column size
    recipe = db.Column(db.String(255))  # Adjusted column size
    open_price = db.Column(db.String(100))  # Adjusted column size
    voided = db.Column(db.String(50))  # Adjusted column size
    receiving_store = db.Column(db.String(100))  # Adjusted column size
    open_item = db.Column(db.String(50))  # Adjusted column size
    last_date = db.Column(db.DateTime)  # Changed to DateTime
    last_price = db.Column(db.String(100))  # Adjusted column size
    last_quantity = db.Column(db.String(100))  # Adjusted column size
    created_date = db.Column(db.DateTime)  # Changed to DateTime

    created_by_id =db.Column(db.Integer,db.ForeignKey('user.id'))
    
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name= db.Column(db.String(500))  
    first_name = db.Column(db.String(400))
    last_name = db.Column(db.String(400))
    email = db.Column(db.String(400))
    session = db.Column(db.String(400))
    position = db.Column(db.String(400))
    dob = db.Column(db.String(400))
    employment_date = db.Column(db.String(400))
    phone = db.Column(db.String(400))
    gender = db.Column(db.String(400))
    id_type = db.Column(db.String(400))
    id_upload = db.Column(db.String(400))
    photo = db.Column(db.Text)
    id_number = db.Column(db.String(400))
    address = db.Column(db.String(400))
    remark = db.Column(db.String(400))
    city = db.Column(db.String(400))
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Employee(id={self.id}, name={self.first_name} {self.last_name}, email={self.email})>"

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name= db.Column(db.String(500))  
    name = db.Column(db.String(400))
    attendance = db.Column(db.String(400))
    position = db.Column(db.String(400))
    time_in = db.Column(db.String(400))
    time_out = db.Column(db.String(400))
    created_date = db.Column(db.String(400))
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Attendance(id={self.id}, name={self.name}, attendance={self.attendance})>"

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400))
    adult = db.Column(db.String(400))
    arrival = db.Column(db.String(400))
    departure = db.Column(db.String(400))
    children = db.Column(db.String(400))
    phone = db.Column(db.String(400))
    email = db.Column(db.String(400))
    purpose = db.Column(db.String(400))
    room_number = db.Column(db.String(400))
    country = db.Column(db.String(400))
    room_type = db.Column(db.String(400))
    price = db.Column(db.String(400))
    created_date = db.Column(db.String(400))
    payment_status = db.Column(db.Text)
    status = db.Column(db.Text)
    company_name= db.Column(db.String(500))  
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Reservation(id={self.id}, name={self.name}, room_number={self.room_number}, status={self.status})>"

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400))
    description = db.Column(db.String(400))
    position = db.Column(db.String(400))
    created_for = db.Column(db.String(400))
    created_date = db.Column(db.String(400))
    company_name= db.Column(db.String(500))  
    created_by = db.Column(db.String(400))

    def __repr__(self):
        return f"<Todo(id={self.id}, name={self.name}, created_for={self.created_for})>"

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    amount = db.Column(db.Text)
    date = db.Column(db.Text)
    note = db.Column(db.String(400))
    user = db.Column(db.String(400))
    created_date = db.Column(db.String(400))
    company_name= db.Column(db.String(500))  
    session = db.Column(db.String(200))
    subcategory = db.Column(db.String(200))
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Expenses(id={self.id}, name={self.name}, amount={self.amount}, date={self.date})>"

class GOP(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    amount = db.Column(db.Text)
    date = db.Column(db.Text)
    company_name= db.Column(db.String(500))  
    note = db.Column(db.String(400))
    user = db.Column(db.String(400))
    created_date = db.Column(db.String(400))
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<GOP(id={self.id}, name={self.name}, amount={self.amount}, date={self.date})>"

class Income(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    amount = db.Column(db.Text)
    date = db.Column(db.Text)
    note = db.Column(db.String(400))
    attendant= db.Column(db.String(400))
    company_name= db.Column(db.String(500))  
    cashier= db.Column(db.String(300))  
    created_date = db.Column(db.String(400))
    customer = db.Column(db.String(400))
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session  =db.Column(db.String(200))
    cat  =db.Column(db.String(200))
    method=db.Column(db.String(200))
    category = db.Column(db.String(200))
    discount = db.Column(db.String(200))
    phone = db.Column(db.String(200))
    def __repr__(self):
        return f"<Income(id={self.id}, name={self.name}, amount={self.amount}, date={self.date})>"


class CanceldOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    amount = db.Column(db.Text)
    date = db.Column(db.Text)
    attendant= db.Column(db.String(400))
    company_name= db.Column(db.String(500))  
    # cashier= db.Column(db.String(300))  
    created_date = db.Column(db.String(400))
    # created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session  =db.Column(db.String(200))
   
    def __repr__(self):
        return f"<CanceldOrder(id={self.id}, name={self.name}, amount={self.amount}, date={self.date})>"


class EventPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    amount = db.Column(db.Text)
    date = db.Column(db.Text)
    note = db.Column(db.String(400))
    balance = db.Column(db.String(400))
    customer_name = db.Column(db.Text)
    customer_phone = db.Column(db.String(400))
    start_time = db.Column(db.Text)
    end_time = db.Column(db.String(400))
    company_name= db.Column(db.String(500))  
    received_by= db.Column(db.String(300))  
    status= db.Column(db.String(300))  
    created_date = db.Column(db.String(400))
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    session  =db.Column(db.String(200))
    method=db.Column(db.String(200))
    def __repr__(self):
        return f"<Income(id={self.id}, name={self.name}, amount={self.amount}, date={self.date})>"
    

class FoodChef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    food = db.Column(db.Text)
    date = db.Column(db.Text)
    company_name= db.Column(db.String(500))  
    created_date = db.Column(db.String(400))
    created_by_id = db.Column(db.String(400))
    session = db.Column(db.String(200))

class Budget(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    amount = db.Column(db.Text)
    type = db.Column(db.Text)
    note = db.Column(db.String(400))
    company_name= db.Column(db.String(500))  
    created_date = db.Column(db.String(400))
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Budget(id={self.id}, name={self.name}, amount={self.amount}, type={self.type})>"

class Family(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    company_name= db.Column(db.String(500))  
    created_date = db.Column(db.String(400))

    def __repr__(self):
        return f"<Family(id={self.id}, name={self.name}, description={self.description})>"

class Iteman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)  # Change to TEXT
    description = db.Column(db.Text)  # Change to TEXT
    created_date = db.Column(db.String(400))
    category = db.Column(db.Text)  # Change to TEXT
    family = db.Column(db.Text)  # Change to TEXT
    price = db.Column(db.String(400))
    whole_price = db.Column(db.String(400))
    unit = db.Column(db.String(400))
    voided = db.Column(db.String(400))
    is_vip = db.Column(db.String(400))
    quantity= db.Column(db.String(500))
   
    company_name= db.Column(db.String(500))  

    def __repr__(self):
        return f"<Iteman(id={self.id}, name={self.name}, price={self.price}, voided={self.voided})>"

class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    created_date = db.Column(db.String(400))
    company_name= db.Column(db.String(500))  

    def __repr__(self):
        return f"<Unit(id={self.id}, name={self.name})>"

class ReceivedItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    company_name= db.Column(db.String(500))  
    quantity = db.Column(db.Text)
    created_date = db.Column(db.String(400))
    batch_number = db.Column(db.String(400))
    expired_date = db.Column(db.String(400)) 


    def __repr__(self):
        return f"<ReceivedItem(id={self.id}, name={self.name}, quantity={self.quantity})>"
    
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.Text)
    company_name= db.Column(db.String(500))  
    lastname = db.Column(db.Text)
    created_date = db.Column(db.String(400))
    phone= db.Column(db.String(400))
    coupon_value = db.Column(db.String(400))
    coupon_applied= db.Column(db.String(400))

class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    store = db.Column(db.Text)
    quantity = db.Column(db.Text)
    company_name= db.Column(db.String(500))  
    created_date = db.Column(db.String(400))
    session = db.Column(db.String(100))

    def __repr__(self):
        return f"<Stock(id={self.id}, name={self.name}, store={self.store}, quantity={self.quantity})>"
    

class StockUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    store = db.Column(db.Text)
    operation = db.Column(db.String(500))  
    quantity = db.Column(db.Text)
    company_name= db.Column(db.String(500))  
    created_date = db.Column(db.String(400))
    session = db.Column(db.String(100))




class returnRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Text)
    item_id = db.Column(db.Text)
    requested_by = db.Column(db.Text)
    quantity = db.Column(db.Text)
    reason = db.Column(db.Text)
    status = db.Column(db.String(400))
    company_name= db.Column(db.String(500))  
    
    created_date = db.Column(db.String(400))

    def __repr__(self):
        return f"<ReturnRequest(id={self.id}, item={self.item}, quantity={self.quantity}, status={self.status})>"

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    category = db.Column(db.Text)
    description = db.Column(db.Text)
    company_name= db.Column(db.String(500))  
    created_date = db.Column(db.String(400))

    def __repr__(self):
        return f"<Store(id={self.id}, name={self.name}, category={self.category})>"

class StockTransfer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    department = db.Column(db.Text)
    company_name= db.Column(db.String(500))  
    quantity = db.Column(db.Text)
    created_date = db.Column(db.String(400))

    def __repr__(self):
        return f"<StockTransfer(id={self.id}, name={self.name}, quantity={self.quantity})>"
    

class StockTransferOut(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    department = db.Column(db.Text)
    company_name= db.Column(db.String(500))  
    quantity = db.Column(db.Text)
    created_date = db.Column(db.String(400))

    def __repr__(self):
        return f"<StockTransferOut(id={self.id}, name={self.name}, quantity={self.quantity})>"

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    hod = db.Column(db.Text)
    company_name= db.Column(db.String(500))  
    created_date = db.Column(db.String(400))

    def __repr__(self):
        return f"<Department(id={self.id}, name={self.name}, hod={self.hod})>"

class Vendor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    phone = db.Column(db.Text)
    address = db.Column(db.Text)
    company_name= db.Column(db.String(500))  
    created_date = db.Column(db.String(400))

    def __repr__(self):
        return f"<Vendor(id={self.id}, name={self.name}, phone={self.phone})>"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    company_name= db.Column(db.String(500))  
    created_date = db.Column(db.String(400))
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, description={self.description})>"
    
    
    

class AccountGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    subcategory= db.Column(db.String(400))
    created_date=created_date = db.Column(db.String(400))
    
class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    amount = db.Column(db.Text)
    subcategory= db.Column(db.String(400))
    created_date=created_date = db.Column(db.String(400))
  



class PurchaseRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Text)
    requested_by = db.Column(db.Text)
    created_date = db.Column(db.String(400))
    department = db.Column(db.Text)
    quantity = db.Column(db.Text)
    unit_price = db.Column(db.Text)
    company_name= db.Column(db.String(500))  
    total_cost = db.Column(db.Text)
    status = db.Column(db.String(400))
    store = db.Column(db.String(400))
    approved_by = db.Column(db.Text)
    approved_date = db.Column(db.Text)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.id'))

    def __repr__(self):
        return f"<PurchaseRequest(id={self.id}, item={self.item}, requested_by={self.requested_by}, status={self.status})>"

class PurchaseOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Text)
    company_name= db.Column(db.String(500))  
    store = db.Column(db.Text)
    created_date = db.Column(db.String(400))
    voided = db.Column(db.String(400))
    quantity = db.Column(db.Text)

    def __repr__(self):
        return f"<PurchaseOrder(id={self.id}, item={self.item}, quantity={self.quantity})>"
    

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requested_by = db.Column(db.String(255))
    company_name = db.Column(db.String(255))
    created_date = db.Column(db.String(100))
    status = db.Column(db.String(100), default='Pending')

    # Relationship to link to PurchaseRequest
    requests = db.relationship('PurchaseRequest', backref='cart', lazy=True)


    




