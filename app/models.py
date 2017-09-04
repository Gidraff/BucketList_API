from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


from app import db, create_app

class User(db.Model):
    """creates a table for the user"""

    __tablename__ = 'users'
    id =db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=False)
    password_hash = db.Column(db.String(64))
    email = db.Column(db.String(120), unique=True)
    bucketlists = db.relationship(
        "Bucketlist", backref="users", lazy="dynamic")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def generate_auth_token(self, expiration=600):
        """generates authentication token"""
        s = Serializer(
            app.config['SECRET'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(
            app.config['SECRET'], expires_in=expiration)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None
        except  BadSignature:
            return None

        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        #return formatted data
        return "<User: {}>".format(self.username)

class Bucketlist(db.Model):
    """Create a table for bucketlist"""
    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False)
    description = db.Column(db.String(120), unique=False)
    date_created = db.Column(
        db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    created_by = db.relationship(
        'User', backref="users.username", lazy="dynamic")
    activities = db.relationship(
        "Activity", cascade="delete", 
        backref="bucketlists", lazy="dynamic")

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self):
        #return formatted onject
        return "<Bucketlist: {}>".format(self.title)

class Activity(db.Model):
    """Creates a table for activities"""
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(150), unique=True)
    bucketlist_id = db.Column(
        db.Integer, db.ForeignKey('bucketlists.id'))
    date_created = db.Column(
        db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp())
    done = db.Column(db.Boolean, default=False)

    def __init__(self, activity):
        self.activity = activity

    def __repr__(self):
        return "<Activity: {}>".format(self.activity)
