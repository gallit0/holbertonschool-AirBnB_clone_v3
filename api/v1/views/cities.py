#!/usr/bin/python3
"""
    City
"""


from api.v1.views import app_views
from flask import request, jsonify
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False, methods=['GET'])
def cities_index(state_id):
    if storage.get(State, state_id) is None:
        return {"error": "Not found"}, 404

    cities = storage.get(State, state_id).cities
    cities_dict = []
    for city in cities:
        cities_dict.append(city.to_dict())
    return jsonify(cities_dict)


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['GET'])
def cities_get(city_id):
    if storage.get(City, city_id) is None:
        return {"error": "Not found"}, 404

    return jsonify(storage.get(City, city_id).to_dict())


@app_views.route("/cities/<city_id>",
                 strict_slashes=False, methods=['DELETE'])
def cities_delete(city_id):
    if storage.get(City, city_id) is None:
        return {"error": "Not found"}, 404

    storage.get(City, city_id).delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                 strict_slashes=False, methods=['POST'])
def cities_store(state_id):
    state = storage.get(State, state_id)

    if state is None:
        return {"error": "Not found"}, 404

    if not request.is_json:
        return {"error": "Not a Json"}, 400

    new_city = request.get_json()

    if "name" not in new_city:
        return {"error": "Missing name"}, 400

    new_city['state_id'] = state_id

    new_city = City(**new_city)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", strict_slashes=False, methods=['PUT'])
def cities_update(city_id):
    city = storage.get(City, city_id)
    data = request.get_json()

    if city is None:
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
        if key in City.__dict__:
            setattr(city, key, data[key])

    city.save()
    return jsonify(City.to_dict()), 200
