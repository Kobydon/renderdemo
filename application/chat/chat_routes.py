# chat_routes.py
from flask import Blueprint, request, jsonify
from flask_praetorian import auth_required, current_user
from flask import Blueprint,render_template
from flask.helpers import make_response
from sqlalchemy.sql.functions import current_time
from  application.extensions.extensions import *
from  application.settings.settings import *
from  application.settings.setup import app

import json
# from application.forms import LoginForm
# from application.database.user.user_db import db,Guests,User,Booking,Rooms,Payment,Reservation,Refund,Budget,Income,Expenses,Attendance,Iteman,Family,Category,Unit,Stock,Store,StockTransfer,Department,Vendor,PurchaseOrder,PurchaseRequest,ReceivedItem,returnRequest,GOP,RoomType,Session,Wifi,Order,StockUsage,PosPayment,OrderItem,HeldCart,FoodChef,EventPayment,StockTransferOut,Cart,CanceldOrder,Customer,Credit,AccountGroup
from application.database.user.user_db import *
from sqlalchemy import or_,desc,and_
from datetime import datetime
from datetime import date
from flask import session
from flask import jsonify, request
import json
from flask_praetorian import auth_required, current_user

from datetime import datetime
import json


chat_bp = Blueprint('chat', __name__)

# Store online users (in production, use Redis)
online_users = {}

@chat_bp.route('/users/online', methods=['GET'])
@auth_required
def get_online_users():
    """Get list of online users (staff with role 'online' or 'admin')"""
    try:
        user = current_user()
        
        # Get all online user IDs
        online_user_ids = list(online_users.keys())
        
        # Query users with role 'online' or 'admin'
        online_users_list = User.query.filter(
            User.roles.in_(['online','customer','admin','large_format','digital_printing','label','dtf']),
            User.id.in_(online_user_ids) if online_user_ids else False
        ).all()
        
        result = []
        for u in online_users_list:
            result.append({
                'id': u.id,
                'firstname': u.firstname,
                'lastname': u.lastname,
                'email': u.email,
                'role': u.roles,
                'online': True
            })
        
        # Also get offline users with role 'online' or 'admin'
        offline_users = User.query.filter(
            User.roles.in_(['online','customer','admin','large_format','digital_printing','label','dtf']),
            User.id.in_(online_user_ids) if online_user_ids else True
        ).all()
        
        for u in offline_users:
            result.append({
                'id': u.id,
                'firstname': u.firstname,
                'lastname': u.lastname,
                'email': u.email,
                'role': u.roles,
                'online': False
            })
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"❌ Error getting online users: {str(e)}")
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/messages/<int:receiver_id>', methods=['GET'])
@auth_required
def get_chat_messages(receiver_id):
    """Get chat history between current user and receiver"""
    try:
        user = current_user()
        
        # Get messages between current user and receiver
        messages = ChatMessage.query.filter(
            ((ChatMessage.sender_id == user.id) & (ChatMessage.receiver_id == receiver_id)) |
            ((ChatMessage.sender_id == receiver_id) & (ChatMessage.receiver_id == user.id))
        ).order_by(ChatMessage.timestamp.asc()).all()
        
        result = [msg.to_dict() for msg in messages]
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"❌ Error getting messages: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@chat_bp.route('/messages', methods=['POST'])
@auth_required
def send_chat_message():
    """Send a message with optional attachment"""
    try:
        user = current_user()
        data = request.get_json()
        
        receiver_id = data.get('receiver_id')
        message = data.get('message', '')
        attachment_data = data.get('attachment_data')  # Base64 data
        attachment_name = data.get('attachment_name')
        attachment_type = data.get('attachment_type')
        attachment_size = data.get('attachment_size')
        
        if not receiver_id:
            return jsonify({'error': 'receiver_id is required'}), 400
        
        if not message and not attachment_data:
            return jsonify({'error': 'Either message or attachment is required'}), 400
        
        # Create room ID
        room = f"chat_{min(user.id, receiver_id)}_{max(user.id, receiver_id)}"
        
        # Save message to database
        chat_message = ChatMessage(
            sender_id=user.id,
            receiver_id=receiver_id,
            message=message,
            room=room,
            timestamp=datetime.utcnow(),
            read=False,
            attachment_name=attachment_name,
            attachment_type=attachment_type,
            attachment_data=attachment_data,  # Store Base64 data
            attachment_size=attachment_size,
            is_attachment=bool(attachment_data)
        )
        db.session.add(chat_message)
        db.session.commit()
        
        return jsonify(chat_message.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error sending message: {str(e)}")
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/messages/<int:message_id>/read', methods=['PUT'])
@auth_required
def mark_message_read(message_id):
    """Mark a message as read"""
    try:
        user = current_user()
        
        message = ChatMessage.query.get(message_id)
        if not message:
            return jsonify({'error': 'Message not found'}), 404
        
        # Only allow marking as read if user is the receiver
        if message.receiver_id != user.id:
            return jsonify({'error': 'Unauthorized'}), 403
        
        message.read = True
        db.session.commit()
        
        return jsonify({'success': True, 'message_id': message_id}), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error marking message as read: {str(e)}")
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/messages/unread', methods=['GET'])
@auth_required
def get_unread_count():
    """Get count of unread messages for current user"""
    try:
        user = current_user()
        
        unread_count = ChatMessage.query.filter_by(
            receiver_id=user.id,
            read=False
        ).count()
        
        return jsonify({'unread_count': unread_count}), 200
        
    except Exception as e:
        print(f"❌ Error getting unread count: {str(e)}")
        return jsonify({'error': str(e)}), 500