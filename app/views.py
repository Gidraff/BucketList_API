"""Module that contains all endpoints"""
#modules and packages for import
from flask import jsonify, request, render_template
from
from app import db, create_app

from app.models import User, Bucketlist, Activity

#Intializes app

app = app.create_app('development')

@app.route('/index', methods=['GET'])
def index():
    """This is index page"""
    return render_template('index.html')

@app.route('/auth/register', methods=['POST'])
def user_registration():
    """function that registers the user"""
    user_data = request.get_json()
    user = User.query.filter_by(email=user_data.get('email')).first
    if not user:
        try:
            user = User(
                username=user_data.get('username'),
                email=user_data.get('email')
                password=user_data('password')
            )
            # inserts user
            db.session.add(user)
            db.session.commit()

            #generate token
            token = g.user.generate_auth_token()
            responseObject= {
                'status': 'success',
                'message': 'You were successfully registered',
                'token': token
            }
            return jsonify(responseObject), 201
        except Exception as e:
            responseObject = {
                'status': 'fail',
                'message': 'please try again!'
            }
            return jsonify(responseObject), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'User already exist please Log in.'
        }
        return jsonify(responseObject), 202

@app.route('/auth/login', methods=['POST'])
def user_login():
    """Function that handles user login"""
    pass

@app.route('/auth/logout', methods=['POST'])
def user_logout():
    """Function that handles user logout"""
    pass

@app.route('/auth/reset-password', methods=['POST'])
def reset_password():
    """Functions that handles password resetting"""
    pass

@app.route('/bucketlists/', methods=['POST'])
def create_bucketlist():
    """Function that handles bucketlist creation"""
    pass

@app.route('/bucketlists/', methods=['GET'])
def view_bucketlists():
    """Function that handles viewing bucketlists"""
    pass

@app.route('/bucketlists/<id>', methods=['GET'])
def view_bucketlist(id):
    """Function returns bucketlist by id passed"""
    pass

@app.route('/bucketlists/<id>', methods=['PUT'])
def edit_bucketlist(id):
    """
    Function that handles editting of a bucketlist
    """
    pass

@app.route('/bucketlists/<id>', methods=['DELETE'])
def delete_bucketlist(id):
    """Function that handles bucketlist deletion"""
    pass

@app.route('/bucketlists/<id>/activities/', methods=['POST'])
def create_activity(id):
    """Function that handles activity creation"""
    pass

@app.route('/bucketlists/<id>/activities/<activity_id>', methods='PUT')
def edit_activity(id, activity_id):
    pass

@app.route('/bucketlists/<id>/activities/<activity_id>', methods=['DELETE'])
def delete_activity(id, activity_id):
    """
    Function that handles deletion of a bucketlist
    activities
    """
    pass
