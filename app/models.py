from flask_sqlalchemy import SQLAlchemy
import jwt

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

from flask import current_app

db = SQLAlchemy()


class User(db.Model):
    """creates a table for the user"""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(300), unique=True)
    password = db.Column(db.String(300))
    email = db.Column(db.String(300), unique=True)
    bucketlists = db.relationship(
        "Bucketlist", backref="users",
        lazy="dynamic", order_by="Bucketlist.id", cascade='all, delete-orphan')

    def __init__(self, username, email, password):
        """Initialize a table by"""
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        """Verifies password against its harsh to validate
        user's password
        """
        return check_password_hash(self.password, password)

    def generate_token(self, user_id):
        """generates authentication token"""
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=20),
                'iat': datetime.utcnow(),
                'sub': user_id
            }

            # create byte string token using payload and secret key
            jwt_string = jwt.encode(
                payload,
                current_app.config['SECRET'],
                algorithm='HS256'
            )
            return jwt_string
        except Exception as e:
            # returns an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decode the access token from the authorization """
        try:
            payload = jwt.decode(token, current_app.config['SECRET'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Expired token please login to get a new one"
        except jwt.InvalidTokenError:
            return "Invalid token.Please Register or Login"

    def save(self):
        # saves a new user or edited user
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        # return formatted data
        return "<User: {}>".format(self.username)


class Bucketlist(db.Model):
    """Create a table for bucketlist"""
    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(300), unique=False)
    description = db.Column(db.String(300), unique=False)
    date_created = db.Column(
        db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    items = db.relationship(
        "Item", order_by="Item.bucketlist_id", cascade="delete",
        backref="bucketlists", lazy="dynamic")

    def __init__(self, title, description, created_by):
        """
            Initializes Bucketlist by title, description, created_by
        """
        self.title = title
        self.description = description
        self.created_by = created_by

    def save(self):
        """saves new bucketlist or edited bucketlist"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """deletes bucketlist"""
        db.session.delete(self)
        db.session.commit()
        return True

    @staticmethod
    def get_all(user_id):
        """returns all of users bucketlist"""
        return Bucketlist.query.filter_by(created_by=user_id)

    def __repr__(self):
        # return formatted onject
        return "<Bucketlist: {}>".format(self.title)


class Item(db.Model):
    """Creates a table for items"""
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item = db.Column(db.String(150), unique=True, nullable=False)
    bucketlist_id = db.Column(
        db.Integer, db.ForeignKey(Bucketlist.id))
    date_created = db.Column(
        db.DateTime, default=datetime.now, nullable=False)
    date_modified = db.Column(
        db.DateTime, default=datetime.now, nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, item, bucketlist_id):
        self.item = item
        self.bucketlist_id = bucketlist_id

    def save(self):
        """saves new item or edited bucketlist"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """deletes a given item in bucketlist"""
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all(bucketlist_id):
        """get all itemt"""
        return Item.query.filter_by(bucketlist_id=bucketlist_id).all()

    def __repr__(self):
        return "<Item: {}>".format(self.item)


class BlackList(db.Model):
    """creates a table to handle token blacklist logout"""
    __tablename__ = "blacklist"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, default=datetime.now,
                               nullable=False)

    def __init__(self, token):
        """Initialize blacklist by token"""
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def save(self):
        """saves token in the blacklist table"""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        """returns spring representation of blacklits object"""
        return '<id: token: {}'.format(self.token)
