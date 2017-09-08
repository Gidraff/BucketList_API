from flask.views import MethodView

from ..models import db, Bucketlist, Activity
from . import activity_blueprint


class ActivityAPI(MethodView):
    """
    class that handle activity manipulation
    """
    def post(self):
        """Function that handles activity creation"""
        pass

    def put(self):
        """function that handles activity editing"""
        pass

    def delete(self):
        """
        Function that handles deletion of a bucketlist
        activities
        """
        pass

#Instantiate ActivityAPI blueprint
activity_view = ActivityAPI.as_view('activity_views')

activity_blueprint.add_url_rule('/bucketlists/<id>/activities', 
                                view_func=activity_view, 
                                methods=['POST'])




#define add url rules

