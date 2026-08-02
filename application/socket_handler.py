# socket_handler.py
from flask import request
from flask_socketio import emit, join_room, leave_room
from application.database.user.user_db import *
from datetime import datetime

# Store online users with their session IDs
online_users = {}

def register_socket_handlers(socketio):
    """Register all Socket.IO event handlers"""
    
    @socketio.on('connect')
    def handle_connect():
        """Handle user connection"""
        try:
            # Get user_id from query string
            user_id = request.args.get('user_id')
            
            if user_id:
                user_id = int(user_id)
                online_users[str(user_id)] = {
                    'sid': request.sid,
                    'user_id': user_id,
                    'joined_at': datetime.now().isoformat()
                }
                
                # Broadcast online users list
                emit('online_users', list(online_users.keys()), broadcast=True)
                print(f"✅ User {user_id} connected (SID: {request.sid})")
            else:
                print(f"⚠️ Connection attempt without user_id")
                
        except Exception as e:
            print(f"❌ Connection error: {e}")

    @socketio.on('disconnect')
    def handle_disconnect():
        """Handle user disconnection"""
        try:
            user_id = None
            for uid, data in online_users.items():
                if data['sid'] == request.sid:
                    user_id = uid
                    break
            
            if user_id:
                del online_users[user_id]
                emit('online_users', list(online_users.keys()), broadcast=True)
                print(f"✅ User {user_id} disconnected")
                
        except Exception as e:
            print(f"❌ Disconnect error: {e}")

    @socketio.on('join_chat')
    def handle_join_chat(data):
        """Join a chat room"""
        try:
            room = data.get('room')
            user_id = data.get('user_id')
            
            if room and user_id:
                join_room(room)
                print(f"✅ User {user_id} joined room: {room}")
                emit('room_joined', {'room': room, 'user_id': user_id}, room=room)
                
        except Exception as e:
            print(f"❌ Join room error: {e}")

    @socketio.on('leave_chat')
    def handle_leave_chat(data):
        """Leave a chat room"""
        try:
            room = data.get('room')
            user_id = data.get('user_id')
            
            if room and user_id:
                leave_room(room)
                print(f"✅ User {user_id} left room: {room}")
                
        except Exception as e:
            print(f"❌ Leave room error: {e}")

    @socketio.on('send_message')
    def handle_send_message(data):
        """Send and store message"""
        try:
            room = data.get('room')
            sender_id = data.get('sender_id')
            receiver_id = data.get('receiver_id')
            message = data.get('message')
            timestamp = datetime.now().isoformat()
            
            if not all([room, sender_id, receiver_id, message]):
                emit('error', {'error': 'Missing required fields'})
                return
            
            # Save message to database
            chat_message = ChatMessage(
                sender_id=sender_id,
                receiver_id=receiver_id,
                message=message,
                room=room,
                timestamp=datetime.utcnow(),
                read=False
            )
            db.session.add(chat_message)
            db.session.commit()
            
            # Prepare response data
            response_data = {
                'id': chat_message.id,
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'message': message,
                'timestamp': timestamp,
                'read': False
            }
            
            # Emit message to room
            emit('new_message', response_data, room=room)
            
            # Also emit to sender (for confirmation)
            emit('message_sent', response_data, room=request.sid)
            
            print(f"💬 Message sent from {sender_id} to {receiver_id} in room {room}")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Message error: {e}")
            emit('error', {'error': str(e)})

    @socketio.on('typing')
    def handle_typing(data):
        """Handle typing indicator"""
        try:
            room = data.get('room')
            user_id = data.get('user_id')
            is_typing = data.get('is_typing', False)
            
            if room and user_id:
                emit('user_typing', {
                    'user_id': user_id,
                    'is_typing': is_typing
                }, room=room)
                
        except Exception as e:
            print(f"❌ Typing error: {e}")

    @socketio.on('mark_as_read')
    def handle_mark_as_read(data):
        """Mark messages as read"""
        try:
            message_id = data.get('message_id')
            room = data.get('room')
            
            if message_id:
                message = ChatMessage.query.get(message_id)
                if message:
                    message.read = True
                    db.session.commit()
                    
                    emit('message_read', {
                        'message_id': message_id,
                        'read': True
                    }, room=room)
                    
                    print(f"✅ Message {message_id} marked as read")
                    
        except Exception as e:
            db.session.rollback()
            print(f"❌ Mark read error: {e}")

    @socketio.on('get_online_users')
    def handle_get_online_users():
        """Get list of online users"""
        try:
            emit('online_users', list(online_users.keys()))
        except Exception as e:
            print(f"❌ Get online users error: {e}")

    @socketio.on('ping')
    def handle_ping():
        """Handle ping to keep connection alive"""
        emit('pong', {'timestamp': datetime.now().isoformat()})