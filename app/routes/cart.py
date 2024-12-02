from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from app.models.customer import Customer
from app.models.product import Product
from bson.objectid import ObjectId

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

def get_customer():
    """Fetch the current logged-in customer."""
    customer_id = session.get('customer_id')
    if not customer_id:
        return None
    return Customer.get_customer_by_id(customer_id)

@cart_bp.route('/view', methods=['GET'])
def view_cart_page():
    """Render the cart page."""
    customer = Customer.get_customer_by_id(session.get('customer_id'))
    if not customer:
        return redirect(url_for('auth.login'))

    cart = customer.get('cart', [])
    cart_details = []

    for item in cart:
        product = Product.get_product_by_id(item['productId'])
        if product:
            cart_details.append({
                "product_id": str(item['productId']),
                "name": product['name'],
                "price": product['price'],
                "quantity": item['quantity'],
                "total": product['price'] * item['quantity']
            })

    return render_template('cart/view_cart.html', cart=cart_details)



@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    """Add an item to the cart."""
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided.", "success": False}), 400

    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    variant_id = data.get('variant_id', None)

    # Validate product_id
    if not product_id:
        return jsonify({"message": "Product ID is required.", "success": False}), 400

    try:
        product_id = ObjectId(product_id)
    except Exception:
        return jsonify({"message": "Invalid Product ID format.", "success": False}), 400

    # Fetch customer
    customer = Customer.get_customer_by_id(session.get('customer_id'))
    if not customer:
        return jsonify({"message": "Please log in to add items to your cart.", "success": False}), 401

    # Fetch product
    product = Product.get_product_by_id(product_id)
    if not product:
        return jsonify({"message": "Product not found.", "success": False}), 404

    # Update customer's cart
    cart = customer.get('cart', [])
    for item in cart:
        if item['productId'] == product_id and item.get('variant_id') == variant_id:
            item['quantity'] += quantity
            Customer.update_customer_cart(customer['_id'], cart)
            return jsonify({"message": "Product quantity updated in cart.", "success": True})

    # Add new item to cart
    cart.append({"productId": product_id, "quantity": quantity, "variant_id": variant_id})
    Customer.update_customer_cart(customer['_id'], cart)
    return jsonify({"message": "Product added to cart.", "success": True})



@cart_bp.route('/remove', methods=['POST'])
def remove_from_cart():
    """Remove an item from the cart."""
    data = request.get_json() if request.is_json else request.form
    product_id = data.get('product_id')

    if not product_id:
        return jsonify({"message": "Product ID is required.", "success": False}), 400

    customer = Customer.get_customer_by_id(session.get('customer_id'))
    if not customer:
        return jsonify({"message": "Please log in to remove items from your cart.", "success": False}), 401

    cart = customer.get('cart', [])
    updated_cart = [item for item in cart if str(item['productId']) != product_id]
    Customer.update_customer_cart(customer['_id'], updated_cart)

    return jsonify({"message": "Product removed from cart.", "success": True})


@cart_bp.route('/update', methods=['POST'])
def update_cart_quantity():
    """Update the quantity of an item in the cart."""
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    if not product_id or not quantity:
        return jsonify({"message": "Product ID and quantity are required.", "success": False}), 400

    customer = Customer.get_customer_by_id(session.get('customer_id'))
    if not customer:
        return jsonify({"message": "Please log in to update your cart.", "success": False}), 401

    cart = customer.get('cart', [])
    for item in cart:
        if str(item['productId']) == product_id:
            item['quantity'] = quantity
            Customer.update_customer_cart(customer['_id'], cart)
            return jsonify({"message": "Cart updated successfully.", "success": True})

    return jsonify({"message": "Product not found in cart.", "success": False}), 404




@cart_bp.route('/clear', methods=['POST'])
def clear_cart():
    """Clear the cart."""
    customer = get_customer()
    if not customer:
        return jsonify({"message": "Please log in to clear your cart.", "success": False}), 401

    Customer.update_customer_cart(customer['_id'], [])
    return jsonify({"message": "Cart cleared.", "success": True})
