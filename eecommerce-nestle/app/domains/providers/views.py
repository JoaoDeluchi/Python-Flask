from flask import Blueprint, jsonify, request
from typing import Tuple, Any, List
from app.domains.providers.models import provider_category
from app.domains import category
from app.domains.providers.actions import \
    get as get_provider, \
    create as create_provider, \
    update as update_provider, \
    get_by_id as get_provider_by_id, \
    delete as delete_provider, \
    populate_table_provider_category_association as create_association,\
    get_categories_from_provider as get_association

app_providers = Blueprint('app.providers', __name__)


@app_providers.route('/providers', methods=['POST'])
def post() -> Tuple[Any, int]:
    payload = request.get_json()
    provider = create_provider(payload)
    return jsonify(provider.serialize()), 201


@app_providers.route('/providers/<id>', methods=['PUT'])
def put(id: str) -> Tuple[Any, int]:
    payload = request.get_json()
    provider = update_provider(id, payload)
    return jsonify(provider.serialize()), 200


@app_providers.route('/providers', methods=['GET'])
def get() -> Tuple[Any, int]:
    filters = request.args
    return jsonify([provider.minimum_serialize() for provider in get_provider(filters)]), 200


@app_providers.route('/providers/<id>', methods=['GET'])
def get_by_id(id: str) -> Tuple[Any, int]:
    provider = get_provider_by_id(id)
    return jsonify(provider.serialize()), 200


@app_providers.route('/providers/<id>', methods=['DELETE'])
def delete(id: str) -> Tuple[Any, int]:
    delete_provider(id)
    return jsonify(''), 204


@app_providers.route('/providers/categories', methods=['POST'])
def create_association_provider_category() -> Tuple[Any, int]:
    payload = request.get_json()
    association = create_association(payload)
    return jsonify(association.serialize()), 201


@app_providers.route('/providers/categories/<id>', methods=['GET'])
def get_associations_provider_Category(id: str) -> Tuple[List, int]:
    provider_categories = get_association(id)
    return jsonify(provider_categories), 200

