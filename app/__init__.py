"""Module that handle app creation."""
from flask import jsonify
from flask_api import FlaskAPI
from instance.config import app_config
from .views.users import users_blueprint
from .views.bucketlist import bucketlist_blueprint
from .views.bucketlist_item import item_blueprint
from .views.errors import bad_request, page_not_found
# from .views.errors import internal_server_error
from .models import db


def create_app(config_name):
    """Create flask api App."""
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(users_blueprint)
    app.register_blueprint(bucketlist_blueprint)
    app.register_blueprint(item_blueprint)
    app.register_error_handler(400, bad_request)
    app.register_error_handler(404, page_not_found)
    # app.register_error_handler(Exception, internal_server_error)
    db.init_app(app)
    return app
