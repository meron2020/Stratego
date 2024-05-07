from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import request, jsonify

from Backend.FlaskServer.api.Users.UserHandler import UserHandler


class Authenticator:
    @classmethod
    def authenticate(cls, username, password):
        # Retrieve user data from JSON file based on the provided username
        user = UserHandler.get_user(username)

        # Check if user exists and password matches
        if user and user.password == password:
            return True

        return False

    @classmethod
    def create_token(cls, user_id, last_activity):
        payload = {
            'exp': datetime.utcnow() + timedelta(minutes=30),
            'iat': datetime.utcnow(),
            'sub': user_id,
            'last_activity': last_activity
        }
        return jwt.encode(payload, "yoav_key", algorithm='HS256').decode('utf-8')

    @classmethod
    def decode_token(cls, token, secret_key):
        return jwt.decode(token, secret_key, algorithms=['HS256'])

    @classmethod
    def jwt_required(cls, f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Authorization token is missing'}), 403
            try:
                payload = jwt.decode(token, "yoav_key", algorithms=['HS256'])
                last_activity = datetime.fromtimestamp(payload['last_activity'])
                if (datetime.utcnow() - last_activity) > timedelta(minutes=5):
                    return jsonify({'message': 'Session has expired due to inactivity'}), 401
                # Update last activity in token
                new_last_activity = datetime.utcnow().timestamp()
                new_token = Authenticator.create_token(payload['sub'], new_last_activity)
                response = f(*args, **kwargs)
                response.headers['New-Token'] = new_token  # Update the response headers with the new token
                return response
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token has expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'message': 'Invalid token'}), 401
            except Exception as e:
                return jsonify({'message': str(e)}), 500

        return decorated_function
