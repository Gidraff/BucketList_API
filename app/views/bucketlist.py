from flask.views import MethodView
from flask import make_response, jsonify, request
from .decorator import login_required
from ..models import Bucketlist
from . import bucketlist_blueprint


class BucketListView(MethodView):
    """
    Class that handles bucketlist manipulation
    """

    @login_required
    def post(self, user_id):
        """Creates Bucketlist"""
        bucket_data = request.get_json()
        title = bucket_data.get("title", " ").strip()
        description = bucket_data.get("description", " ").strip()
        if title:
            existing_bucket = Bucketlist.query.filter_by(
                title=title,
                description=description,
                created_by=user_id).first()
            if existing_bucket:
                responseObject = {
                    "message": "Bucketlist already exists use"
                }
                return jsonify(responseObject), 409
            new_bucketlist = Bucketlist(title=bucket_data.get('title'),
                                        description=bucket_data.get(
                                            'description'),
                                        created_by=user_id
                                        )
            new_bucketlist.save()
            responseObject = {
                "id": new_bucketlist.id,
                "title": new_bucketlist.title,
                "description": new_bucketlist.description,
                "date_created": new_bucketlist.date_created,
                "created_by": new_bucketlist.created_by
            }
            return jsonify(responseObject), 201
        response = {
            "message": "Title cannot be blank"
        }
        return jsonify(response), 400

    @login_required
    def get(self, user_id, id=None):
        """return bucketlists"""
        if id is None:
            limit = request.args.get("limit", 20)
            page = request.args.get("page", 1)
            q = request.args.get("q")
            limit = 100 if int(limit) > 100 else int(limit)
            if q:
                bucketlists = Bucketlist.query.filter(
                    Bucketlist.title.ilike("%" + q + "%")).filter_by(
                        created_by=user_id)
            bucketlists = Bucketlist.query.filter_by(
                created_by=user_id
            )

            buckelists_pagination = bucketlists.paginate(int(page), int(limit))

            results = []
            for bucketlist in buckelists_pagination.items:
                response = {
                    "id": bucketlist.id,
                    "title": bucketlist.title,
                    "description": bucketlist.description,
                    "date_created": bucketlist.date_created,
                    "created_by": bucketlist.created_by
                }
                results.append(response)
            return jsonify(results), 200

        bucketlists = Bucketlist.query.filter_by(id=id, created_by=user_id)
        if not bucketlists:
            response = {"message": "Resource not found"}
            return jsonify(response), 404
        for bucketlist in bucketlists:

            bucketlist_detail = {
                "id": bucketlist.id,
                "title": bucketlist.title,
                "description": bucketlist.description,
                "date_created": bucketlist.date_created,
                "created_by": bucketlist.created_by
            }

            return make_response(jsonify(bucketlist_detail)), 200

    @login_required
    def put(self, id, user_id):
        """Edits bucketlist"""
        bucketlist = Bucketlist.query.filter_by(
            id=id, created_by=user_id).first()
        print(bucketlist.title)
        if not bucketlist:
            response = {
                "message": "No bucketlist by that id"
            }
            return jsonify(response), 404

        data = request.get_json()
        title = data.get("title")
        description = data.get("description")
        if title and description:
            bucketlist.title = title
            bucketlist.description = description

            bucketlist.save()
            responseObject = {
                "title": bucketlist.title,
                "description": bucketlist.description,
                "date_created": bucketlist.date_created,
                "date_modified": bucketlist.date_modified,
                "created_by": bucketlist.created_by
            }

            return make_response(jsonify(responseObject))
        response = {
            "message": "Enter a valid title and description"
        }
        return make_response(jsonify(response))

    @login_required
    def delete(self, user_id, id):
        """Deletes bucketlist"""
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            response = {
                "message": "No such bucketlist"
            }
            return make_response(jsonify(response)), 404
        if bucketlist.delete():
            response = {
                "message": "Bucketlist was deleted"
            }
            return make_response(jsonify(response)), 200
        return 'internal server error', 500


# Instantiate ItemAPI blueprint

bucketlist_view = BucketListView.as_view("bucketlist_view")


bucketlist_blueprint.add_url_rule('/bucketlists/', defaults={'user_id': None},
                                  view_func=bucketlist_view,
                                  methods=['POST'])
bucketlist_blueprint.add_url_rule(
    '/bucketlists/', view_func=bucketlist_view, methods=["GET"])
bucketlist_blueprint.add_url_rule('/bucketlists/<int:id>',
                                  view_func=bucketlist_view,
                                  methods=['GET', 'PUT', 'DELETE'])
