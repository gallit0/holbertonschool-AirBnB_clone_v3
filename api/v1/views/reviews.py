#!/usr/bin/python3
"""
    Review
"""


from api.v1.views import app_views
from flask import request, jsonify, abort
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False, methods=['GET'])
def reviews_index(place_id):
    if storage.get(Place, place_id) is None:
        return {"error": "Not found"}, 404

    reviews = storage.get(Place, place_id).reviews
    reviews_dict = []
    for review in reviews:
        reviews_dict.append(review.to_dict())
    return jsonify(reviews_dict)


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=['GET'])
def reviews_get(review_id):
    if storage.get(Review, review_id) is None:
        return {"error": "Not found"}, 404

    return jsonify(storage.get(Review, review_id).to_dict())


@app_views.route("/reviews/<review_id>",
                 strict_slashes=False, methods=['DELETE'])
def reviews_delete(review_id):
    if storage.get(Review, review_id) is None:
        return {"error": "Not found"}, 404

    storage.get(Review, review_id).delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 strict_slashes=False, methods=['POST'])
def reviews_store(place_id):
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if not request.is_json:
        return {"error": "Not a Json"}, 400

    new_review = request.get_json()

    if "text" not in new_review:
        return {"error": "Missing text"}, 400

    if "user_id" not in new_review:
        return {"error": "Missing user_id"}, 400

    if storage.get(User, new_review['user_id']) is None:
        abort(404)

    new_review['place_id'] = place_id

    new_review = Review(**new_review)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=['PUT'])
def reviews_update(review_id):
    review = storage.get(Review, review_id)
    data = request.get_json()

    if review is None:
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
        if key == 'place_id':
            continue
        if key in Review.__dict__:
            setattr(review, key, data[key])

    review.save()
    return jsonify(review.to_dict()), 200
