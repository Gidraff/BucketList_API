"""Module that handle user functionalities."""
import uuid
import re
from flask import Blueprint, jsonify, request, g, make_response
from flask.views import MethodView
from werkzeug.security import generate_password_hash
from .decorator import login_required
from ..models import User, BlackList

users_blueprint = Blueprint("users", __name__)


class RegistrationApiView(MethodView):
    """class that handles all authentications."""

    def post(self):
        """Register a user."""
        user_data = request.get_json()
        username = user_data.get('username')
        email = user_data.get('email')
        password = user_data.get('password')
        if username and email and password:
            if User.is_email_valid(email):
                if len(username.strip()) < 3:
                    message = {"error": "Invalid username.Try again!."}
                    return make_response(jsonify(message)), 400
                if re.match(
                        r'.*[\%\$\^\*\@\!\?\(\)\:\;\'\"\{\}\[\]].*', username):
                    message = {"error": "username has special characters."}
                    return jsonify(message), 400
                elif len(email) < 7:
                    message = {"message": "email too short."}
                    return make_response(jsonify(message)), 400
                elif len(password.strip()) < 7:
                    message = {"message": "Invalid password.Try Again !"}
                    return make_response(jsonify(message)), 400
                user = User.query.filter_by(email=email).first()
                if not user:
                    try:
                        user = User(username=username,
                                    email=email,
                                    password=password)
                        # saves user
                        user.save()
                        responseObject = {
                            'message': 'You were successfully registered'}
                        return jsonify(responseObject), 201
                    except Exception as e:
                        responseObject = {'message': 'user already exists'}
                        return jsonify(responseObject), 500
                responseObject = {
                    'error': 'User already exist please Log in.'}
                return jsonify(responseObject), 409
            return jsonify({"message": "Invalid username or email"}), 400
        response = {"message": "Input fields cannot be empty"}
        return jsonify(response), 400


class LoginAPI(MethodView):
    """class that handles User Login."""

    def post(self):
        """Log in user."""
        user_data = request.get_json()
        user = User.query.filter_by(email=user_data.get('email')).first()
        g.user = user
        if user and user.verify_password(user_data.get('password')):
            try:
                access_token = user.generate_token(user.id)
                if access_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'You are logged in!',
                        'access_token': access_token.decode()}
                    return jsonify(responseObject), 200
            except Exception as e:
                responseObject = {'status': 'fail', 'message': str(e)}
                return jsonify(responseObject), 400
        responseObject = {'message': 'Invalid credentials or not registered!'}
        return jsonify(responseObject), 401


class LogOutAPI(MethodView):
    """class that handles user logout."""

    def post(self):
        """Logout a user."""
        auth_token = request.headers.get('Authorization')
        if auth_token:
            resp = User.decode_token(auth_token)
            if not isinstance(resp, str):
                blacklist_token = BlackList(token=auth_token)
                try:
                    blacklist_token.save()
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged out'}
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    responseObject = {'message': e}
                    return make_response(jsonify(responseObject)), 200
            responseObject = {'status': 'fail', 'message': resp}
            return make_response(jsonify(responseObject)), 401
        responseObject = {
            'status': 'fail',
            'message': 'Please provide valid authentication token'}
        return make_response(jsonify(responseObject)), 403


class ResetPassword(MethodView):
    """class that handles resetting of password."""

    def post(self):
        """Functions that handles password resetting."""
        user_data = request.get_json()
        user = User.query.filter_by(email=user_data.get('email')).first()

        if user:
            new_password = uuid.uuid4().hex
            user.password = generate_password_hash(new_password)
            user.save()

            responseObject = {
                "message": "Password reset successful!",
                "New password": new_password}
            return make_response(jsonify(responseObject)), 200
        else:
            response = {"message": "Email does not exist"}
            return make_response(jsonify(response)), 401

# Instantiate ActivityAPI blueprint


registration_api_view = RegistrationApiView.as_view("registration_api_view")


login_view = LoginAPI.as_view("login_view")
logout_view = LogOutAPI.as_view("logout_view")
reset_password = ResetPassword.as_view("reset_password")


users_blueprint.add_url_rule('/auth/register/',
                             view_func=registration_api_view,
                             methods=['POST'])
users_blueprint.add_url_rule('/auth/login/',
                             view_func=login_view,
                             methods=['POST'])

users_blueprint.add_url_rule('/auth/logout/',
                             view_func=logout_view,
                             methods=['POST'])

users_blueprint.add_url_rule('/auth/reset-password/',
                             view_func=reset_password,
                             methods=['POST'])


# define add url rules
