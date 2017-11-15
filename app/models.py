"""Module that contains all models."""
import jwt
import re
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask import current_app, jsonify

db = SQLAlchemy()


class User(db.Model):
    """create a table for the user."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(300), unique=True)
    password = db.Column(db.String(300))
    email = db.Column(db.String(300), unique=True)
    bucketlists = db.relationship(
        "Bucketlist", backref="users",
        lazy="dynamic", order_by="Bucketlist.id", cascade='all, delete-orphan')

    def __init__(self, username, email, password):
        """Initialize a user by username, password and email."""
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        """Validate user password."""
        return check_password_hash(self.password, password)

    def generate_token(self, user_id):
        """Generate authentication token."""
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=60),
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
    def is_email_valid(email):
        """Validate email and return a boolean value."""
        return bool(re.match(r"[\w\.-]+@([\w\.-]+)(\.[\w\.]+$)", email))

    @staticmethod
    def decode_token(token):
        """Decode the access token from the authorization."""
        try:
            payload = jwt.decode(token, current_app.config['SECRET'])
            is_blacklisted = BlackList.check_token(token)
            if is_blacklisted:
                return "Login to access this service!"
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return "Not Authorized please login!"
        except jwt.InvalidTokenError:
            return "Not Authorized.Please Register or Login"

    def save(self):
        """Save an instance of user."""
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        """Return a formatted object."""
        return "<User: {}>".format(self.username)


class Bucketlist(db.Model):
    """Create a table for bucketlist."""

    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(300))
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
        """Initialize Bucketlist by title, description, created_by."""
        self.title = title
        self.description = description
        self.created_by = created_by

    def save(self):
        """Save new bucketlist or edited bucketlist."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete bucketlist."""
        db.session.delete(self)
        db.session.commit()
        return jsonify({
            "message": "{} deleted successfully".format(self.title)})

    @staticmethod
    def exists(user_id, title):
        """Check bucketlist existence."""
        bucket = Bucketlist.query.filter_by(created_by=user_id,
                                            title=title).first()
        if bucket:
            return True
        else:
            return False

    @staticmethod
    def get_all(user_id):
        """Return all of user's Bucketlist."""
        return Bucketlist.query.filter_by(created_by=user_id).all()

    def __repr__(self):
        """Return formatted object."""
        return "<Bucketlist: {}>".format(self.title)


class Item(db.Model):
    """Create a table for items."""

    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    item = db.Column(db.String(150), unique=True)
    bucketlist_id = db.Column(
        db.Integer, db.ForeignKey(Bucketlist.id))
    date_created = db.Column(
        db.DateTime, default=datetime.now)
    date_modified = db.Column(
        db.DateTime, default=datetime.now)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, item, done, bucketlist_id):
        """Initialize bucketlist object."""
        self.item = item
        self.done = done
        self.bucketlist_id = bucketlist_id

    def save(self):
        """Save new item or edited bucketlist."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete specified item in from bucketlist."""
        db.session.delete(self)
        db.session.commit()
        return True

    @staticmethod
    def exists(item_id):
        """Check if an item exists."""
        unique_item = Item.query.filter_by(
            id=item_id).first()
        return True if unique_item else False

    @staticmethod
    def get_all(bucketlist_id):
        """Return all items."""
        return Item.query.filter_by(bucketlist_id=bucketlist_id).all()

    def __repr__(self):
        """Return formatted Item Object."""
        return "<Item: {}>".format(self.item)


class BlackList(db.Model):
    """Creates table to handle token blacklist."""

    __tablename__ = "blacklist"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, default=datetime.now,
                               nullable=False)

    def __init__(self, token):
        """Initialize blacklist by token."""
        self.token = token
        self.blacklisted_on = datetime.now()

    def save(self):
        """Save token in the blacklist table."""
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def check_token(auth_token):
        """Verify token existence."""
        response = BlackList.query.filter_by(token=str(auth_token)).first()

        if response:
            return True
        else:
            return False

    def __repr__(self):
        """Return formatted of blacklist object."""
        return '<id: token: {}'.format(self.token)
