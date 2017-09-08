from flask import jsonify, request
from app.models import User
from functools import wraps

def login_required(func):

    @wraps
    def decorator(*args, **kwargs):
        auth_token = request.headers.get('Authorization')

        if not auth_token:
            responseObject = {
                "message": "Invalid token.Please registe or login",
            }
            return jsonify(responseObject), 401
        if auth_token:
            kwargs['user_id'] = User.decode_token(auth_token)

            if not isinstance(kwargs['user_id'], int):
                message = kwargs['user_id']
                response = {
                    "message": message
                }
                return jsonify(responseObject), 401
            return func(*args, **kwargs)
        return decorator
