
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
# from  application.settings.settings import *
from  application.settings.setup import app
# from application.forms import LoginForm
from application.database import *
# from application.database.user.user_db import User
from sqlalchemy import or_,desc,and_
from datetime import datetime
from flask import session
from  application.user_view.user import user
from  application.room_view.room import room
from  application.guest_view.guest import guest
from  application.employee_view.employee import employee
from application.database.user.user_db import db
# from  application.client_view.client import client
#from  application.room_view.room import room
#from  application.employee_view.employee import employee
#from  application.guest_view.guest import guest






app =app 

with app.app_context():
             db.create_all()

    


# #========================Blueprint=======================#


app.register_blueprint(user,url_prefix="/user")
app.register_blueprint(room,url_prefix="/room")
app.register_blueprint(guest,url_prefix="/guest")
app.register_blueprint(employee,url_prefix="/employee")




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

