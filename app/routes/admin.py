from flask import Blueprint, request, jsonify
from services.admin_service import add_product, update_product, delete_product

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/product', methods=['POST'])
def add_product_route():
    data = request.json
    response = add_product(data)
    return jsonify(response)

@admin_bp.route('/product/<product_id>', methods=['PUT'])
def update_product_route(product_id):
    data = request.json
    response = update_product(product_id, data)
    return jsonify(response)

@admin_bp.route('/product/<product_id>', methods=['DELETE'])
def delete_product_route(product_id):
    response = delete_product(product_id)
    return jsonify(response)
