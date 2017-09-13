from flask import Blueprint

# Instantiate Blueprint for users blueprint
users_blueprint = Blueprint("users", __name__)
from . import users


# Instantiate Blueprint for bucketlist blueprint
bucketlist_blueprint = Blueprint("bucketlist", __name__)
from . import bucketlist


# Instantiate Blueprint for bucketlist blueprint
item_blueprint = Blueprint("item", __name__)
from . import bucketlist_item
