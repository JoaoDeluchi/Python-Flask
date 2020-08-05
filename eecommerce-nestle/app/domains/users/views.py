from typing import Tuple, Any

from flask import Blueprint, jsonify, request


from app.domains.users.actions import \
    get as get_users, \
    create as create_user, \
    update as update_user, \
    get_by_id as get_user_by_id,\
    delete as delete_users

app_users = Blueprint('app.users', __name__)


@app_users.route('/users', methods=['POST'])
def post() -> Tuple[Any, int]:
    payload = request.get_json()
    user = create_user(payload)
    return jsonify(user.serialize()), 201


@app_users.route('/users/<id>', methods=['PUT'])
def put(id: str) -> Tuple[Any, int]:
    payload = request.get_json()
    user = update_user(id, payload)
    return jsonify(user.serialize()), 200


@app_users.route('/users', methods=['GET'])
def get() -> Tuple[Any, int]:
    return jsonify([user.serialize() for user in get_users()]), 200


@app_users.route('/users/<id>', methods=['GET'])
def get_by_id(id: str) -> Tuple[Any, int]:
    user = get_user_by_id(id)
    return jsonify(user.serialize()), 200


@app_users.route('/users/<id>', methods=['DELETE'])
def delete(id: str) -> Tuple[Any, int]:
    delete_users(id)
    return jsonify(''), 204
