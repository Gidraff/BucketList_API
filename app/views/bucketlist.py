"""Module that handles bucketlist functionalities."""
import re
from flask.views import MethodView
from flask import Blueprint, make_response, jsonify, request
from .decorator import login_required
from ..models import Bucketlist

bucketlist_blueprint = Blueprint("bucketlist", __name__)


class BucketListView(MethodView):
    """Class that handles bucketlist manipulation."""

    @login_required
    def post(self, user_id):
        """Create Bucketlist."""
        bucket_data = request.get_json()
        title = bucket_data.get("title")
        description = bucket_data.get("description")
        if isinstance(title, int):
            return jsonify({"error": "Title cannot be a integer"}), 400
        if title.strip():
            if Bucketlist.exists(user_id, title.strip(" ")):
                return jsonify({"error": "Bucketlist already exists."}), 409
            if re.match(r'.*[\%\$\^\*\@\!\?\(\)\:\;\'\"\{\}\[\]].*', title):
                return jsonify({
                        "error": "Invalid, remove  special characters"}), 400
            if len(title.strip()) > 70:
                return jsonify({"error": "Invalid clength for title"}), 400
            if re.match(
                    r'.*[\%\$\^\*\@\!\?\(\)\:\;\'\"\{\}\[\]].*', description):
                return jsonify({"error": "Title has special characters"}), 400
            elif len(description.strip()) > 300:
                return jsonify({"error": "description too long.Max 300"}), 400
            new_bucketlist = Bucketlist(title=title,
                                        description=description,
                                        created_by=user_id)
            new_bucketlist.save()
            responseObject = {
                "id": new_bucketlist.id,
                "title": new_bucketlist.title,
                "description": new_bucketlist.description,
                "date_created": new_bucketlist.date_created,
                "created_by": new_bucketlist.created_by}
            return jsonify(responseObject), 201
        return jsonify({"message": "Title cannot be blank"}), 400

    @login_required
    def get(self, user_id, id=None):
        """Return bucketlists."""
        if id is None:
            try:
                limit = int(request.args.get("limit", default=20, type=int))
                page = int(request.args.get("page", default=1, type=int))
            except TypeError as e:
                return jsonify({"error": "limit and page must be int"}), 400
            q = request.args.get("q", type=str)
            limit = 5 if int(limit) > 5 else int(limit)
            if q:
                bucketlists = Bucketlist.query.filter(
                    Bucketlist.title.ilike("%" + q + "%")).filter_by(
                        created_by=user_id)
                bucketlist_search = [{
                    "id": bucketlist.id,
                    "title": bucketlist.title,
                    "description": bucketlist.description,
                    "date_created": bucketlist.date_created,
                    "created_by": bucketlist.created_by
                } for bucketlist in bucketlists]
                return jsonify(bucketlist_search)

            bucketlists = Bucketlist.query.filter_by(
                created_by=user_id
            ).paginate(int(page), int(limit))

            next_page = ''
            prev_page = ''
            pages = bucketlists.pages
            if bucketlists.has_next:
                next_page = 'http://localhost:5000' +\
                    '/bucketlists/?limit=' + str(limit) +\
                    '&page=' + str(page + 1)

            if bucketlists.has_prev:
                prev_page = 'http://localhost:5000' +\
                    '/bucketlists/?limit=' + str(limit) +\
                    '&page=' + str(page - 1)

            results = []
            for bucketlist in bucketlists.items:
                response = {
                    "id": bucketlist.id,
                    "title": bucketlist.title,
                    "description": bucketlist.description,
                    "date_created": bucketlist.date_created,
                    "created_by": bucketlist.created_by}
                results.append(response)
            if len(results) == 0:
                return jsonify({"message": "No bucketlists available"}), 400
            return make_response(jsonify(
                                        buckets=results,
                                        next_page=next_page,
                                        prev_page=prev_page,
                                        pages=pages)), 200

        bucketlists = Bucketlist.query.filter_by(
            id=id, created_by=user_id).first()
        if not bucketlists:
            return jsonify({"message": "Resource not found"}), 404
        bucketlist_detail = {
            "id": bucketlists.id,
            "title": bucketlists.title,
            "description": bucketlists.description,
            "date_created": bucketlists.date_created,
            "created_by": bucketlists.created_by}
        return make_response(jsonify(bucketlist_detail)), 200

    @login_required
    def put(self, id, user_id):
        """Edits bucketlist."""
        bucketlist = Bucketlist.query.filter_by(
            id=id, created_by=user_id).first()
        if not bucketlist:
            return jsonify({"error": "No bucketlist matching id passed"}), 404

        data = request.get_json()
        title = data.get("title")
        description = data.get("description")

        if not title.strip() or type(title) == int:
            return jsonify({"message": "Invalid title"})
        if title.strip():
            if not Bucketlist.exists(user_id, title):
                bucketlist.title = title
        if re.match(r'.*[\%\$\^\*\@\!\?\(\)\:\;\'\"\{\}\[\]].*', title):
                message = {"error": "special characters not allowed"}
                return jsonify(message), 400
        if len(title.strip()) < 1 or len(title.strip()) > 70:
            return jsonify({"Error": "Invalid length for title"}), 400
        if description.strip() and\
                type(description) is int:
                bucketlist.description = bucketlist.description
        if re.match(r'.*[\%\$\^\*\@\!\?\(\)\:\;\'\"\{\}\[\]].*', description):
                return jsonify({
                    "error": "special characters not allowed"}), 400
        if len(description.strip()) > 300:
            return jsonify({"error": "Invalid length for description"}), 400
        elif isinstance(description, str) and\
                description.strip():
            bucketlist.description = description
        bucketlist.save()
        responseObject = {
            "title": bucketlist.title,
            "description": bucketlist.description,
            "date_created": bucketlist.date_created,
            "date_modified": bucketlist.date_modified,
            "created_by": bucketlist.created_by
        }
        return make_response(jsonify(responseObject)), 200
        return make_response(jsonify({
            "error": "Enter a valid title and description"})), 400

    @login_required
    def delete(self, user_id, id):
        """Delete bucketlist specified."""
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            return jsonify({"error": "No bucketlist matching that id"}), 404
        if bucketlist.delete():
            return jsonify({"message": "Bucketlist was deleted"}), 200
        return 'internal server error', 500


# Instantiate ItemAPI blueprint


bucketlist_view = BucketListView.as_view("bucketlist_view")


bucketlist_blueprint.add_url_rule('/bucketlists/', defaults={'user_id': None},
                                  view_func=bucketlist_view,
                                  methods=['POST'])

bucketlist_blueprint.add_url_rule(
    '/bucketlists/', view_func=bucketlist_view, methods=["GET"])
bucketlist_blueprint.add_url_rule('/bucketlists/<int:id>/',
                                  view_func=bucketlist_view,
                                  methods=['GET', 'PUT', 'DELETE'])
