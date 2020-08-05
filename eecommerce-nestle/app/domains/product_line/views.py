from typing import Tuple, Any

from flask import Blueprint, jsonify, request

from app.domains.product_line.actions import \
    get as get_product_line, \
    create as create_product_line, \
    update as update_product_line, \
    get_by_id as get_product_line_by_id, \
    delete as delete_product_line

app_product_line = Blueprint('app.product_line', __name__)


@app_product_line.route('/product_lines', methods=['POST'])
def post() -> Tuple[Any, int]:
    payload = request.get_json()
    product_line = create_product_line(payload)
    return jsonify(product_line.serialize()), 201


@app_product_line.route('/product_lines/<id>', methods=['PUT'])
def put(id: str) -> Tuple[Any, int]:
    payload = request.get_json()
    product_line = update_product_line(id, payload)
    return jsonify(product_line.serialize()), 200


@app_product_line.route('/product_lines', methods=['GET'])
def get() -> Tuple[Any, int]:
    filters = request.args
    return jsonify([product_line.serialize() for product_line in get_product_line(filters)]), 200


@app_product_line.route('/product_lines/<id>', methods=['GET'])
def get_by_id(id: str) -> Tuple[Any, int]:
    product_line = get_product_line_by_id(id)
    return jsonify(product_line.serialize()), 200


@app_product_line.route('/product_lines/<id>', methods=['DELETE'])
def delete(id: str) -> Tuple[Any, int]:
    delete_product_line(id)
    return jsonify(''), 204
