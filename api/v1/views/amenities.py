#!/usr/bin/python3
"""
    Amenity
"""


from api.v1.views import app_views
from flask import request, jsonify
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities/", strict_slashes=False, methods=['GET'])
def amenities_index():
    amenities = storage.all(Amenity)
    amenities_dict = []
    for amenity in amenities:
        amenities_dict.append(amenities[amenity].to_dict())
    return jsonify(amenities_dict)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False, methods=['GET'])
def amenities_get(amenity_id):
    if storage.get(Amenity, amenity_id) is None:
        return {"error": "Not found"}, 404

    return jsonify(storage.get(Amenity, amenity_id).to_dict())


@app_views.route("/amenities/<amenity_id>",
                 strict_slashes=False, methods=['DELETE'])
def amenities_delete(amenity_id):
    if storage.get(Amenity, amenity_id) is None:
        return {"error": "Not found"}, 404

    storage.get(Amenity, amenity_id).delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", strict_slashes=False, methods=['POST'])
def amenities_store():
    if not request.is_json:
        return {"error": "Not a Json"}, 400

    new_amenity = request.get_json()

    if "name" not in new_amenity:
        return {"error": "Missing name"}, 400

    new_amenity = Amenity(**new_amenity)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", strict_slashes=False, methods=['PUT'])
def amenities_update(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    data = request.get_json()

    if amenity is None:
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
        if key in Amenity.__dict__:
            setattr(amenity, key, data[key])

    amenity.save()
    return jsonify(amenity.to_dict()), 200
