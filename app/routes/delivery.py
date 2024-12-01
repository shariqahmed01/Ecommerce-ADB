from flask import Blueprint, jsonify
from services.delivery_service import track_delivery

delivery_bp = Blueprint('delivery', __name__, url_prefix='/delivery')

@delivery_bp.route('/<tracking_number>', methods=['GET'])
def track_order(tracking_number):
    response = track_delivery(tracking_number)
    return jsonify(response)
