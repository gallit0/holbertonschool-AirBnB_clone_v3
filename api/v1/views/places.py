#!/usr/bin/python3
"""
    Place
"""


from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.city import City
from models.user import User
from models.place import Place


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False, methods=['GET'])
def places_index(city_id):
    if storage.get(City, city_id) is None:
        return {"error": "Not found"}, 404

    places = storage.get(City, city_id).places
    places_dict = []
    for place in places:
        places_dict.append(place.to_dict())
    return jsonify(places_dict)


@app_views.route("/places/<place_id>", strict_slashes=False, methods=['GET'])
def places_get(place_id):
    if storage.get(Place, place_id) is None:
        return {"error": "Not found"}, 404

    return jsonify(storage.get(Place, place_id).to_dict())


@app_views.route("/places/<place_id>",
                 strict_slashes=False, methods=['DELETE'])
def places_delete(place_id):
    if storage.get(Place, place_id) is None:
        return {"error": "Not found"}, 404

    storage.get(Place, place_id).delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 strict_slashes=False, methods=['POST'])
def places_store(city_id):
    city = storage.get(City, city_id)

    if city is None:
        return {"error": "Not found"}, 404

    if not request.is_json:
        return {"error": "Not a Json"}, 400

    new_place = request.get_json()

    if "name" not in new_place:
        return {"error": "Missing name"}, 400

    if "user_id" not in new_place:
        return {"error": "Missing user_id"}, 400

    if storage.get(User, new_place['user_id']) is None:
        return {"error": "Not found"}, 404

    new_place['city_id'] = city_id

    new_place = Place(**new_place)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False, methods=['PUT'])
def places_update(place_id):
    place = storage.get(Place, place_id)
    data = request.get_json()

    if place is None:
        return {"error": "Not found"}, 404

    if not request.is_json:
        return {"error": "Not a Json"}, 400

    for key in data:
        if key == 'id':
            continue
        if key == 'created_at':
            continue
        if key == 'updated_at':
            continue
        if key == 'city_id':
            continue
        if key in Place.__dict__:
            setattr(place, key, data[key])

    place.save()
    return jsonify(place.to_dict()), 200
