"""Module that contains decorator."""
from flask import jsonify, request
from ..models import User
from functools import wraps


def login_required(func):
    """Return a decorator."""
    @wraps(func)
    def decorator(*args, **kwargs):
        """Wrap function and return message."""
        auth_token = request.headers.get('Authorization')

        if not auth_token:
            responseObject = {
                "message": "Invalid token.Please register or login",
            }
            return jsonify(responseObject), 401
        if auth_token:
            kwargs['user_id'] = User.decode_token(auth_token)

            if not isinstance(kwargs['user_id'], int):
                message = kwargs['user_id']
                response = {
                    "message": message
                }
                return jsonify(response), 401
        return func(*args, **kwargs)
    return decorator
