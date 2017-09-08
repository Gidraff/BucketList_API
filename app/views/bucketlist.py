from flask.views import MethodView
from flask import jsonify, request
from decorator import login_required
from ..models import db, Bucketlist
from . import bucketlist_blueprint


class BucketListView(MethodView):
    """
    Class that handles bucketlist manipulation
    """

    def post(self, user_id):
        """Creates Bucketlist"""
        decorators = [login_required]

        bucket_data = request.get_json()
        title = bucket_data.get("title", " ").strip()
        description = bucket_data.get("description", " ").strip()
        created_by = bucket_data.get("created_by", "").strip()
        if title:
            
            existing_bucket = Bucketlist.query.filter_by(title=title,
                                                         description=description,
                                                         created_by=created_by
                                                         ).first()
            if existing_bucket:
                responseObject = {
                    "message": "Bucketlist already exists use"
                }
                return jsonify(responseObject), 409
            else:
                new_bucketlist = Bucketlist(title=bucket_data.get('title'),
                                            description=bucket_data.get('description'),
                                            created_by =bucket_data.get('created_by')
                                            )
                new_bucketlist.save()
                responseObject = {
                    "id": new_bucketlist.id,
                    "title": new_bucketlist.title,
                    "description": new_bucketlist.description,
                    "date_created": new_bucketlist.date_created
                }
                return jsonify(responseObject), 201
        else:
            
            response = {
                "message": "Title cannot be blank"
            }
            return jsonify(response), 400


    def get(self):
        """return bucketlists"""
        
        pass


    def put(self):
        """Edits bucketlist"""

        pass

    def get(self):
        """returns bucketlist by id"""
        pass

    def delete(self):
        """Deletes bucketlist"""
        pass


#Instantiate ActivityAPI blueprint

bucketlist_view = BucketListView.as_view("bucketlist_view")


bucketlist_blueprint.add_url_rule('/bucketlists/', defaults={'user_id': None}, 
                                    view_func=bucketlist_view, 
                                    methods=['POST',])
bucketlist_blueprint.add_url_rule('/bucketlists/', view_func=bucketlist_view, methods=['GET', ])
bucketlist_blueprint.add_url_rule('/bucketlists/<int:id>', view_func=bucketlist_view, 
                                    methods=['GET', 'PUT', 'DELETE'])
