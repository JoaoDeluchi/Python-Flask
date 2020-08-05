from typing import Tuple, Any

from flask import Blueprint, jsonify, request, send_file
from app.domains.products.actions import \
    get as get_product, \
    create as create_product, \
    update as update_product, \
    get_by_id as get_product_by_id, \
    delete as delete_product, \
    export_product,\
    upload_file as upload_product

app_products = Blueprint('app.products', __name__)


@app_products.route('/products', methods=['POST'])
def post() -> Tuple[Any, int]:
    payload = request.get_json()
    product = create_product(payload)
    return jsonify(product.serialize()), 201


@app_products.route('/products/<id>', methods=['PUT'])
def put(id: str) -> Tuple[Any, int]:
    payload = request.get_json()
    product = update_product(id, payload)
    return jsonify(product.serialize()), 200


@app_products.route('/products', methods=['GET'])
def get() -> Tuple[Any, int]:
    filters = request.args
    return jsonify([product.serialize() for product in get_product(filters)]), 200


@app_products.route('/products/<id>', methods=['GET'])
def get_by_id(id: str) -> Tuple[Any, int]:
    product = get_product_by_id(id)
    return jsonify(product.serialize()), 200


@app_products.route('/products/<id>', methods=['DELETE'])
def delete(id: str) -> Tuple[Any, int]:
    delete_product(id)
    return jsonify(''), 204


@app_products.route('/products:batchGet', methods=['GET'])
def batchGet() -> Tuple[Any, int]:
    return send_file(export_product(), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', True), 200


@app_products.route('/products:import', methods=['POST'])
def upload_file() -> Tuple[Any, int]:
    file = request.files['file']
    products_imported = upload_product(file)
    return jsonify([product.serialize() for product in products_imported]), 201
