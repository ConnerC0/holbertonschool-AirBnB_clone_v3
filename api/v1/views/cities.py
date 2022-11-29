#!/usr/bin/python3
"""
city module that handles all default RESTful API
actions.
"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request, make_response


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'],
                 strict_slashes=False
                 )
def list_cities(state_id):
    """List all `State` objects"""
    states = storage.get(State, state_id)
    result = []
    if states is None:
        abort(404)
    for cities in states.cities:
        result.append(cities.to_dict())
    return jsonify(result)


@app_views.route('/cities/<city_id>',
                 methods=['GET'],
                 strict_slashes=False
                 )
def get_city_id(city_id):
    """Retrieves a `State` object."""
    city = storage.get(City, city_id)
    if city is not None:
        return make_response(jsonify(city.to_dict()))
    abort(404)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'],
                 )
def delete_city(city_id):
    """Deletes a `State` object."""
    city = storage.get(City, city_id)
    if city is not None:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities/',
                 methods=['POST'],
                 strict_slashes=False
                 )
def create_city_post(state_id):
    """Creates a `State` object."""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing Name"}), 400)
    state = storage.get(State, state_id)
    if state is None:
        return abort(404)
    request_dict = request.get_json()
    request_dict['state_id'] = state_id
    city = City(**request_dict)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>',
                 methods=['PUT'],
                 strict_slashes=False
                 )
def update_city(city_id):
    """Updates a `State` object."""
    if request.get_json():
        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        request_dict = request.get_json()
        for key, val in request_dict.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, val)
        storage.save()
        return make_response(jsonify(city.to_dict()), 200)
    return make_response(jsonify({"error": "Not a JSON"}), 400)
