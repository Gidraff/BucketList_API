from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimeJSONWebSignatureSerializer as Serializer
from marshmallow import Schema, fields
from passlib.apps import custom_app_context as pwd_context
from app import db

class User(db.Model):
    """creates a table for the user"""

    __tablename__ = 'users'
    id =db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=False)
    email = db.Column(db.String(30), unique=True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        """Method to encrypt password"""
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        """Method to verify password"""
        return pwd_context.verify(password, self.password_hash)

    def authentication_token(self):
        """Generate authentication token"""
        pass

class Bucketlist(db.Model):
    """Create a table for bucketlist"""
    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False)
    description = db.Column(db.String(120), unique=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    created_by = db.relationship(
        'User', backref=db.backref("users.username", lazy="dynamic"))
    activities = db.relationship("Activity", backref=db.backref("bucketlists")


    def __repr__(self):
        return "<Bucketlsi(created_by=%s)>" % (self.created_by)




class Activity(db.Model):
    """Creates a table for activities"""

    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(150), unique=True)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp())
    done = db.Column(db.Boolean, default=False)


class UserSchema(Schema):
    """User schema for serialization"""
    id = fields.int(dump_only=True)
    username = fields.str()
    email = fields.Email()


class ActivitySchema(Schema):
    """Activity schema for serialization"""
    id = fields.int(dump_only=True)
    activity = fields.str(dump_only=True)
    date_created = fields.DateTime()
    date_modified = fields.DateTime()
    done = fields.Boolean()


class BucketlistSchema(Schema):
    """Bucketlist schema for serialization"""
    id = fields.int(dump_only=True)
    title = fields.str(dump_only=True)
    description = fields.str(dump_only=True)
    date_created = fields.DateTime(dump_only=True)
    date_modified = fields.DateTime(dump_only=True)
    created_by = fields.Nested(UserSchema, only=('username'))
    activities = field.Nested(ActivitySchema, many=True)


user_schema = UserSchema()
users_schema = UserSchema(many=True)
bucketlist_schema = BucketlistSchema()
bucketlists_schema =BucketlistSchema(many=True)
activity = ActivitySchema()
activities =ActivitySchema(many=True) 


