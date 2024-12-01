from flask import Blueprint, request, jsonify, abort, session
from app.models.product import Product

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/', methods=['GET'])
def view_cart():
    """View all items in the cart."""
    cart = session.get('cart', [])
    cart_details = []

    for item in cart:
        product = Product.get_product_by_id(item['product_id'])
        if product:
            variant = next((v for v in product.get('variants', []) if v['id'] == item.get('variant_id')), None)
            cart_details.append({
                "product_id": item['product_id'],
                "name": product['name'],
                "price": product['price'],
                "quantity": item['quantity'],
                "variant": variant,  # Include variant details
                "total": product['price'] * item['quantity']
            })

    return jsonify({"cart": cart_details})


@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    """Add an item to the cart."""
    product_id = None
    quantity = 1
    variant_id = None

    # Check for JSON data in the request
    if request.is_json:
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        variant_id = data.get('variant_id')
    else:
        # Fallback to query parameters
        product_id = request.args.get('product_id')
        quantity = request.args.get('quantity', 1, type=int)
        variant_id = request.args.get('variant_id')

    # Validate the product_id
    if not product_id:
        return jsonify({"message": "Product ID is required.", "success": False}), 400

    # Validate the variant_id (optional)
    product = Product.get_product_by_id(product_id)
    if not product:
        return jsonify({"message": "Invalid product ID.", "success": False}), 400
    if variant_id and variant_id not in [v['id'] for v in product.get('variants', [])]:
        return jsonify({"message": "Invalid variant ID.", "success": False}), 400

    # Initialize cart in session if not present
    if 'cart' not in session:
        session['cart'] = []

    # Add or update product in cart
    for item in session['cart']:
        if item['product_id'] == product_id and item.get('variant_id') == variant_id:
            item['quantity'] += quantity
            session.modified = True
            return jsonify({"message": "Product quantity updated in cart.", "success": True})

    # Add new product to the cart
    session['cart'].append({
        "product_id": product_id,
        "quantity": quantity,
        "variant_id": variant_id  # Include variant ID
    })
    session.modified = True

    return jsonify({"message": "Product added to cart.", "success": True})


@cart_bp.route('/remove', methods=['POST'])
def remove_from_cart():
    """Remove an item from the cart."""
    product_id = request.json.get('product_id')
    variant_id = request.json.get('variant_id')
    cart = session.get('cart', [])

    # Remove product from cart
    session['cart'] = [item for item in cart if not (item['product_id'] == product_id and item.get('variant_id') == variant_id)]
    session.modified = True

    return jsonify({"message": "Product removed from cart.", "success": True})


@cart_bp.route('/clear', methods=['POST'])
def clear_cart():
    """Clear the cart."""
    session.pop('cart', None)
    return jsonify({"message": "Cart cleared.", "success": True})
