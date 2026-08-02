# app.py
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from application.extensions.extensions import *
from application.settings.setup import app
from application.database import *
from sqlalchemy import or_, desc, and_
from datetime import datetime
from flask import session, request
from application.user_view.user import user
from application.room_view.room import room
from application.guest_view.guest import guest
from application.employee_view.employee import employee
from application.chat.chat_routes import chat_bp
from application.database.user.user_db import db


# ✅ Import Socket.IO and handlers
from flask_socketio import SocketIO, emit, join_room, leave_room
from application.socket_handler import register_socket_handlers, online_users

# ✅ Import CORS if not already imported
from flask_cors import CORS

app = app

# ✅ Initialize CORS
CORS(app, origins="*")

with app.app_context():
    db.create_all()

# ===================== SOCKET.IO SETUP =====================

# ✅ Initialize SocketIO
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode='threading',
    ping_timeout=60,
    ping_interval=25,
    max_http_buffer_size=1e6
)

# ✅ Register Socket.IO handlers
register_socket_handlers(socketio)

# Make online_users accessible to routes
app.config['ONLINE_USERS'] = online_users

# ===================== BLUEPRINT REGISTRATION =====================

app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(room, url_prefix="/room")
app.register_blueprint(guest, url_prefix="/guest")
app.register_blueprint(employee, url_prefix="/employee")
app.register_blueprint(chat_bp, url_prefix="/chat")

# ===================== HEALTH CHECK =====================

@app.route('/')
def index():
    return jsonify({
        'status': 'Chat server running',
        'online_users': len(online_users),
        'timestamp': datetime.now().isoformat()
    }), 200

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'online_users': len(online_users),
        'timestamp': datetime.now().isoformat()
    }), 200

# ===================== RUN APPLICATION =====================

if __name__ == '__main__':
    # ✅ Run with SocketIO instead of app.run()
    socketio.run(
        app,
        host='0.0.0.0',
        port=5000,
        debug=True,
        allow_unsafe_werkzeug=True
    )