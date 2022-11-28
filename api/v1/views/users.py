#!/usr/bin/python3
"""
users module that handles all default RESTful API
actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def users(user_id):
    if user_id is not None:
        user_list = storage.get(User, user_id)
        if user_list is not None:
            return jsonify(user_list.to_dict())
        abort(404)
    users = storage.all(User)
    user_list = []
    for user in users.values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route("/users/<user_id>", methods=['DELETE'],
                strict_slashes=False)
def user_delete(user_id):
    """deletes a user by ID"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users/", methods=['POST'], strict_slashes=False)
def post_user():
    """POST function for user"""
    if request.get_json():
        if "email" in request.get_json():
            if "password" in request.get_json():
                user = User(**request.get_json())
                user.save()
                return make_response(jsonify(user.to_dict()), 201)
            return make_response(jsonify({"error:" "Missing password"}), 400)
        return make_response(jsonify({"error": "Missing email"}), 400)
    return make_response(jsonify({"error": "Not a JSON"}), 400)


@app_views.route("/users/<user_id>", methods=['PUT'],
                 strict_slashes=False)
def user_put(user_id):
    """update user with PUT"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({"error:" "Not a JSON"}), 400)
    request_dict = request.get_json()
    for key, val in request_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, val)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)