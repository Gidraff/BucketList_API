from flask.views import MethodView
from flask import jsonify, request
from ..models import db, User, Bucketlist, Activity
from . import auth_blueprint


class RegistrationApiView(MethodView):
    """
        class that handles all authentications
    """

    def post(self):
        """function that registers the user"""

        user_data = request.get_json()
        print("r  ", user_data)
        user = User.query.filter_by(email=user_data.get('email')).first()
        if not user:
            try:
                user = User(username=user_data.get('username'),
                            email=user_data.get('email'),
                            password=user_data.get('password'))
            user = user
                # saves user
                user.save()
                responseObject= {
                    'status': 'success',
                    'message': 'You were successfully registered',
                }
                return jsonify(responseObject), 201
            except Exception as e:
                responseObject = {
                    'message': str(e) 
                }
                return jsonify(responseObject), 500
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exist please Log in.'
            }
            return jsonify(responseObject), 409

class LoginAPI(MethodView):
    """
        class that handles User Login
    """
    
    def post(self):
        """Function that handles user login"""
        
        user_data = request.get_json()
        user = User.query.filter_by(email=user_data.get('email')).first()
        g.user
        if user and user.verify_password(user_data.get('password')):
            try:
                access_token = user.generate_token(user.id)
                if access_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'You are logged in!',
                        'access_token': access_token.decode()
                    }
                    return jsonify(responseObject), 200

            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': str(e)
                }
                return jsonify(responseObject),  400
        else:
            responseObject = {
                'message': 'Invalid credentials or not register'
            }
            return jsonify(responseObject), 409


class LogOutAPI(MethodView):
    """
        class that handles user logout
    """

    def post(self):
        """Function that handles user logout"""
    pass

class ResetPassword(MethodView):
    """
        class that handles resetting of password
    """
    
    def post(self):
        """Functions that handles password resetting"""
        pass

#Instantiate ActivityAPI blueprint

registration_api_view = RegistrationApiView.as_view("registration_api_view")
login_view = LoginAPI.as_view("login_view")
logout_view = LogOutAPI.as_view("logout_view")
reset_password = ResetPassword.as_view("reset_password")


auth_blueprint.add_url_rule('/auth/register/', 
                            view_func=registration_api_view,
                            methods=['POST'])

auth_blueprint.add_url_rule('/auth/login/',
                            view_func=login_view,
                            methods=['POST'])

auth_blueprint.add_url_rule('/auth/logout/',
                            view_func=logout_view,
                            methods=['POST'])

auth_blueprint.add_url_rule('/auth/reset-password',
                            view_func=reset_password,
                            methods=['POST'])


#define add url rules