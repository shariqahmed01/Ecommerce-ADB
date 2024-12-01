from flask import Blueprint, request, jsonify, render_template, abort

from app.routes.review import list_reviews
from services.product_service import get_products, get_product_by_id

product_bp = Blueprint('product', __name__, url_prefix='/products')


@product_bp.route('/', methods=['GET'])
def list_products():
    """Display a list of products."""
    filters = request.args.to_dict()
    products = get_products(filters)

    # Convert ObjectId to string
    for product in products["products"]:
        product["_id"] = str(product["_id"])

    return render_template('products/product_list.html', products=products["products"])


from app.models.review import Review

@product_bp.route('/<product_id>', methods=['GET'])
def product_details(product_id):
    product = get_product_by_id(product_id)
    if not product["success"]:
        abort(404, description=product["message"])

    # Fetch reviews for the product
    reviews = Review.get_reviews_by_product_id(product_id)

    return render_template('products/product_detail.html', product=product["product"], reviews=reviews)



