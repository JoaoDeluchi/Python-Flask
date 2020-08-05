from typing import Tuple, Any, List

from flask import Blueprint, jsonify, request, send_file

from app.domains.category.actions import \
    get as get_category, \
    create as create_category, \
    update as update_category, \
    get_by_id as get_category_by_id, \
    delete as delete_category, \
    upload_file, \
    export_file, \
    get_providers_from_category as get_association

app_categories = Blueprint('app.categories', __name__)


@app_categories.route('/categories', methods=['POST'])
def post() -> Tuple[Any, int]:
    payload = request.get_json()
    category = create_category(payload)
    return jsonify(category.serialize()), 201


@app_categories.route('/categories:import', methods=['POST'])
def upload() -> Tuple[Any, int]:
    file = request.files['file']
    return jsonify([category.serialize() for category in upload_file(file)]), 201


@app_categories.route('/categories:batchGet', methods=['GET'])
def batchGet() -> Tuple[Any, int]:
    return send_file(export_file(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', True), 200


@app_categories.route('/categories/<id>', methods=['PUT'])
def put(id: str) -> Tuple[Any, int]:
    payload = request.get_json()
    category = update_category(id, payload)
    return jsonify(category.serialize()), 200


@app_categories.route('/categories', methods=['GET'])
def get() -> Tuple[Any, int]:
    filters = request.args
    return jsonify([category.serialize() for category in get_category(filters)]), 200


@app_categories.route('/categories/<id>', methods=['GET'])
def get_by_id(id: str) -> Tuple[Any, int]:
    category = get_category_by_id(id)
    return jsonify(category.serialize()), 200


@app_categories.route('/categories/<id>', methods=['DELETE'])
def delete(id: str) -> Tuple[Any, int]:
    delete_category(id)
    return jsonify(''), 204

@app_categories.route('/categories/providers/<id>', methods=['GET'])
def get_associations_provider_Category(id: str) -> Tuple[List, int]:
    categories_providers = get_association(id)
    return jsonify(categories_providers), 200