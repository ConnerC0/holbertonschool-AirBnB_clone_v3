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
def users(user_id=None):
    """Returns all users or an user by specific ID"""
    if user_id:
        users = storage.get(User, user_id)
        if users is not None:
            return jsonify(users.to_dict())
        return abort(404)
    users = storage.all(User)
    userlist = []
    for user in users.values():
        userlist.append(user.to_dict())
    return jsonify(userlist)


@app_views.route("/users/<user_id>", methods=['DELETE'],
                 strict_slashes=False)
def user_delete(user_id):
    """deletes a user by ID"""
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users/", methods=['POST'], strict_slashes=False)
def post_user():
    """add user using POST"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "email" not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if "password" not in request.get_json():
        return make_response(jsonify({"error": "Missing password"}), 400)
    user = User(**request.get_json())
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['PUT'],
                 strict_slashes=False)
def user_put(user_id):
    """update user with PUT"""
    user = storage.get(User, user_id)
    if user is None:
        return abort(404)
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    request_dict = request.get_json()
    for key, val in request_dict.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, val)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
