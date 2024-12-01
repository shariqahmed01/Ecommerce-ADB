from flask import Blueprint, request, jsonify
from services.order_service import place_order, get_orders

order_bp = Blueprint('order', __name__, url_prefix='/orders')

@order_bp.route('/', methods=['POST'])
def create_order():
    data = request.json
    response = place_order(data)
    return jsonify(response)

@order_bp.route('/', methods=['GET'])
def list_orders():
    user_id = request.headers.get('user_id')  # Example header to identify the user
    response = get_orders(user_id)
    return jsonify(response)
