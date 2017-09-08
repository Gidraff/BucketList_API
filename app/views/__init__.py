from flask import Blueprint

# Instantiate Blueprint for auth blueprint
auth_blueprint = Blueprint("auth", __name__)
from . import auth


# Instantiate Blueprint for bucketlist blueprint
bucketlist_blueprint = Blueprint("bucketlist", __name__)
from . import bucketlist


# Instantiate Blueprint for bucketlist blueprint
activity_blueprint = Blueprint("activity", __name__)
from . import bucketlist_activity




