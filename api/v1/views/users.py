#!/usr/bin/python3
"""
    User
"""


from api.v1.views import app_views
from flask import request, jsonify
from models import storage
from models.user import User


@app_views.route("/users/", strict_slashes=False, methods=['GET'])
def users_index():
    users = storage.all(User)
    users_dict = []
    for user in users:
        users_dict.append(users[user].to_dict())
    return jsonify(users_dict)


@app_views.route("/users/<user_id>", strict_slashes=False, methods=['GET'])
def users_get(user_id):
    if storage.get(User, user_id) is None:
        return {"error": "Not found"}, 404

    return jsonify(storage.get(User, user_id).to_dict())


@app_views.route("/users/<user_id>",
                 strict_slashes=False, methods=['DELETE'])
def users_delete(user_id):
    if storage.get(User, user_id) is None:
        return {"error": "Not found"}, 404

    storage.get(User, user_id).delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", strict_slashes=False, methods=['POST'])
def users_store():
    if not request.is_json:
        return {"error": "Not a Json"}, 400

    new_user = request.get_json()

    if "email" not in new_user:
        return {"error": "Missing name"}, 400

    if "password" not in new_user:
        return {"error": "Missing name"}, 400

    new_user = User(**new_user)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", strict_slashes=False, methods=['PUT'])
def users_update(user_id):
    user = storage.get(User, user_id)
    data = request.get_json()

    if user is None:
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
        if key == 'email':
            continue
        if key in User.__dict__:
            setattr(user, key, data[key])

    user.save()
    return jsonify(user.to_dict()), 200
