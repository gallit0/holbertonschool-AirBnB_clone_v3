#!/usr/bin/python3
"""
    Places Amenities
"""


from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.place import Place
from models.user import User
from models.amenity import Amenity


@app_views.route("/places/<place_id>/amenities",
                 strict_slashes=False, methods=['GET'])
def places_amenities_index(place_id):
    if storage.get(Place, place_id) is None:
        abort(404)

    amenities = storage.get(Place, place_id).amenities
    places_amenities_dict = []
    for amenity in amenities:
        places_amenities_dict.append(amenity.to_dict())
    return jsonify(places_amenities_dict)


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=['DELETE'])
def places_amenities_delete(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if place is None:
        abort(404)
    if amenity not in place.amenities:
        abort(404)

    del place.amenities[place.amenities.index(amenity)]
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/amenities/<amenity_id>",
                 strict_slashes=False, methods=['POST'])
def places_amenities_link(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if amenity is None:
        abort(404)
    if place is None:
        abort(404)
    if amenity in place.amenities:
        abort(200)

    place.amenities.append(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201
