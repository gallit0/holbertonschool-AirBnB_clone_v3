#!/usr/bin/python3
"""
    State
"""


from api.v1.views import app_views
from flask import request, jsonify
from models import storage
from models.state import State


@app_views.route("/states/", strict_slashes=False, methods=['GET'])
def index():
    states = storage.all(State)
    states_dict = []
    for state in states:
        states_dict.append(states[state].to_dict())
    return jsonify(states_dict)


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['GET'])
def get(state_id):
    if storage.get(State, state_id) is None:
        return {"error": "Not found"}, 404

    return jsonify(storage.get(State, state_id).to_dict())


@app_views.route("/states/<state_id>",
                 strict_slashes=False, methods=['DELETE'])
def delete(state_id):
    if storage.get(State, state_id) is None:
        return {"error": "Not found"}, 404

    storage.get(State, state_id).delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", strict_slashes=False, methods=['POST'])
def store():
    if not request.is_json:
        return {"error": "Not a Json"}, 400

    new_state = request.get_json()

    if "name" not in new_state:
        return {"error": "Missing name"}, 400

    new_state = State(**new_state)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>", strict_slashes=False, methods=['PUT'])
def update(state_id):
    state = storage.get(State, state_id)
    data = request.get_json()

    if state is None:
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
        if key in State.__dict__:
            setattr(state, key, data[key])

    state.save()
    return jsonify(state.to_dict()), 200
