
#!/usr/bin/python3
"""
places module that handles all default RESTful API
actions.
"""

from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, make_response, abort
from models import storage


def place_all(city_id=None):
    """Returns all places"""
    if city_id:
        city = storage.get(City, city_id)
        if city is not None:
            place_list = [place.to_dict() for place in city.places]
            return jsonify(place_list)
        return abort(404)


@app_views.route("/places/<place_id>", methods=['GET'],
                 strict_slashes=False)
def place_by_id(place_id=None):
    """returns a place by a specific ID"""
    if place_id:
        place = storage.get(Place, place_id)
        if place is not None:
            return jsonify(place.to_dict())
        return abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id):
    """deletes a place"""
    place = storage.get(Place, place_id)
    if place is not None:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """add place using POST"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.get_json():
        if 'user_id' in request.get_json():
            if 'name' in request.get_json():
                places = request.get_json()
                user = storage.get(User, places['user_id'])
                if user is None:
                    abort(404)
                places['city_id'] = city_id
                place = Place(**places)
                place.save()
                return make_response(jsonify(place.to_dict()), 201)
            return make_response(jsonify({"error": "Missing name"}), 400)
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    return make_response(jsonify({"error": "Not a JSON"}), 400)


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """update an place with PUT"""
    place = storage.get(Place, place_id)
    if place is None:
        return abort(404)
    request_dict = request.get_json()
    if request_dict is not None:
        for key, val in request_dict.items():
            if key not in ['id', 'created_at', 'updated_at', 'city_id', 'user_id']:
                setattr(place, key, val)
        storage.save()
        return make_response(jsonify(place.to_dict()), 200)
    return make_response(jsonify({"error": "Not a JSON"}), 400)