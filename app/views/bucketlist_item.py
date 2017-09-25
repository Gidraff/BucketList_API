"""Module that handles bucketlits items manipulation."""
import re
from flask.views import MethodView
from flask import Blueprint, make_response, jsonify, abort, request
from .decorator import login_required
from ..models import Bucketlist, Item


item_blueprint = Blueprint("item", __name__)


class ItemAPI(MethodView):
    """class that handle Item manipulation."""

    @login_required
    def post(self, id, user_id):
        """Create that bucketlist Item."""
        bucketlist = Bucketlist.query.filter_by(
            id=id, created_by=user_id).first()
        if not bucketlist:
            return jsonify({"message": "No such buckeltlist"}), 404
        item_data = request.get_json()
        item_name = item_data.get("item")
        done_status = item_data.get("done")

        if "item" not in item_data:
            return jsonify({'error': "Item field is empty!"}), 400
        if item_name and item_name.strip() or done_status:
            if done_status and not isinstance(done_status, bool):
                return jsonify({"error": "It either True of False"}), 400
            # cut from here
            existing_item = Item.query.filter_by(
                item=item_name,
                bucketlist_id=id).first()
            if existing_item:
                return jsonify({"message": "item already exists"}), 409
            if re.match(
                    r'.*[\%\$\^\*\@\!\?\(\)\:\;\'\"\{\}\[\]].*', item_name):
                return jsonify({
                    "error": "Input contains special characters"}), 400
            if len(item_name.strip()) > 70:
                return jsonify({
                    "error": "Invalid lenght. max is 70 characters"}), 400
            item = Item(item=item_name, done=done_status, bucketlist_id=id)

            item.save()
            item_detail = {
                "id": item.id,
                "bucketlist_id": item.bucketlist_id,
                "item": item.item,
                "date_created": item.date_created,
                "date_modified": item.date_modified,
                "done": item.done
            }
            return make_response(jsonify(item_detail)), 201
        return jsonify({"error": "Invalid Inputs.Try again!"}), 400

    @login_required
    def get(self, id, user_id, item_id=None):
        """Return all items or specified item."""
        if item_id is None:
            try:
                limit = request.args.get("limit", default=20, type=int)
                page = request.args.get("page", default=1, type=int)
            except TypeError as e:
                return jsonify({
                    "error": "Something happened.Please check page or limit"}
                    ), 400
            q = request.args.get("q", type=str)
            limit = 5 if int(limit) > 5 else int(limit)
            if q:
                bucketlist = Bucketlist.query.filter_by(
                    id=id, created_by=user_id).first()
                if not bucketlist:
                    return jsonify(
                        {"message": "No bucketlist available"}), 404
                items = Item.query.filter(
                    Item.item.ilike("%" + q + "%")).filter_by(
                        bucketlist_id=id)
                if items:
                    search_items = [{
                        "bucketlist_id": item.bucketlist_id,
                        "id": item.id,
                        "item_name": item.item,
                        "date_created": item.date_created,
                        "done": item.done
                    } for item in items]
                    return jsonify(search_items), 200
                return jsonify({"error": "No match found"}), 404
            bucketlist = Bucketlist.query.filter_by(
                id=id, created_by=user_id).first()
            if not bucketlist:
                return jsonify({"message": "No bucketlist available"}), 404
            items = Item.query.filter_by(
                bucketlist_id=id).paginate(int(page), int(limit))

            next_page = ''
            prev_page = ''
            pages = items.pages
            if items.has_next:
                next_page = 'http://localhost:5000' +\
                    '/bucketlists/{}/items/?=limit'.format(id) +\
                    str(limit) +\
                    '&page=' + str(page - 1)
            if items.has_prev:
                prev_page = 'http://localhost:5000' +\
                    '/bucketlists/{}/items/?=limit'.format(id) +\
                    str(limit) +\
                    '&page=' + str(page - 1)

            results = [{
                "bucketlist_id": item.bucketlist_id,
                "id": item.id,
                "item_name": item.item,
                "done": item.done,
                "date_created": item.date_created,
                "date_modified": item.date_modified
            } for item in items.items]
            return jsonify(
                        items=results,
                        next_page=next_page,
                        prev_page=prev_page,
                        pages=pages), 200
        elif item_id:
            bucketlist = Bucketlist.query.filter_by(
                created_by=user_id, id=id).first()

            if not bucketlist:
                return jsonify({
                    "error": "bucketlist not available available"}), 404
            item = Item.query.filter_by(id=item_id).first()
            if not item:
                return jsonify({"error": "No Item matching that id"}), 404
            return jsonify({
                "item": item.item,
                "date_created": item.date_created,
                "bucketlist_id": item.bucketlist_id,
                "done": item.done,
                "id": item.id
            }), 200

    @login_required
    def put(self, id, item_id, user_id):
        """Edit bucketlist item specified."""
        if not item_id:
            return jsonify({"error": "Item id missing"}), 400
        if Bucketlist.query.filter_by(
                id=id, created_by=user_id).first():
            item_data = request.get_json()
            item_name = None
            item_status = None

            if "item" in item_data:
                item_name = item_data.get("item")
            if "done" in item_data:
                item_status = item_data.get("done")

            if not Item.exists(item_id):
                return jsonify({"error": "No item matching that Id"}), 400
            item = Item.query.filter_by(
                id=item_id, bucketlist_id=id).first()

            if item_name and not item_name.strip() and\
                    not isinstance(item_name, str):
                return jsonify({"error": "Invalid item name"}), 404
            elif item_name and re.match(
                    r'.*[\%\$\^\*\@\!\?\(\)\:\;\'\"\{\}\[\]].*', item_name):
                return jsonify({
                    "error": "Invalid item name has special characters"}), 400
            elif item.item == item_name:
                return jsonify({
                    "error": "Item with that name already exists"}), 404
            elif item_name and len(item_name.strip()) > 70:
                return jsonify({
                    "error": "Invalid lenght.Max 70 characters"}), 400
            elif item_name:
                item.item = item_name
            if item_status and not isinstance(item_status, bool):
                message = {"error": "Invalid.Either True of False"}
                return jsonify(message), 404
            elif isinstance(item_status, bool):
                item.done = item_status
            item.save()
            return jsonify({
                "item": item.item,
                "done": item.done,
                "message": "item Updated !"
            }), 200
        return jsonify({"error": "Bucketlist requested don't exist"}), 404

    @login_required
    def delete(self, id, item_id, user_id):
        """Delete bucketlist item specified."""
        if not item_id:
            return jsonify({"message": "Not allowed"}), 400
        bucketlist = Bucketlist.query.filter_by(
            id=id, created_by=user_id).first()
        if bucketlist:
            item = Item.query.filter_by(
                bucketlist_id=id, id=item_id).first()
            if item:
                item.delete()
                return jsonify({
                    "message": "Item was successfully deleted!"}), 200
            return jsonify({"error": "No item matching that id"}), 404
        return jsonify({"error": "No item for this bucketlist!"}), 404


item_view = ItemAPI.as_view('item_view')
item_blueprint.add_url_rule('/bucketlists/<id>/items/',
                            view_func=item_view,
                            methods=['POST'])

item_blueprint.add_url_rule('/bucketlists/<id>/items/',
                            view_func=item_view,
                            methods=['GET'])

item_blueprint.add_url_rule('/bucketlists/<int:id>/items/<int:item_id>/',
                            view_func=item_view,
                            methods=['GET', 'PUT', 'DELETE'])
