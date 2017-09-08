from flask_api import FlaskAPI
from functools import wraps
from flask import jsonify
from instance.config import app_config
from .models import db
#initialize sqlalchemy

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    #registers authentication blueprint
    from .views import auth_blueprint
    app.register_blueprint(auth_blueprint)

    #registers buckelits blueprint
    from .views import bucketlist_blueprint
    app.register_blueprint(bucketlist_blueprint)

    #register activity blueprint
    from .views import activity_blueprint
    app.register_blueprint(activity_blueprint)


    return app   