from flask import Blueprint, request, jsonify
from services.review_service import add_review, get_reviews

review_bp = Blueprint('review', __name__, url_prefix='/reviews')

@review_bp.route('/<product_id>', methods=['GET'])
def list_reviews(product_id):
    response = get_reviews(product_id)
    return jsonify(response)

@review_bp.route('/', methods=['POST'])
def add_review_route():
    data = request.json
    response = add_review(data)
    return jsonify(response)
