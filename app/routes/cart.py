from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash

from app.models.cart import Cart
from app.models.customer import Customer
from app.models.product import Product
from bson.objectid import ObjectId

from app.models.productvariant import ProductVariant

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

def get_customer():
    """Fetch the current logged-in customer."""
    customer_id = session.get('customer_id')
    if not customer_id:
        return None
    return Customer.get_customer_by_id(customer_id)


@cart_bp.route('/view', methods=['GET'])
def view_cart_page():
    customer_id = session.get('customer_id')
    if not customer_id:
        return redirect(url_for('auth.login'))

    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        return redirect(url_for('auth.login'))

    cart = customer.get('cart', [])
    cart_details = []

    subtotal = 0
    for item in cart:
        # Skip items without required keys
        if not all(key in item for key in ['product_id', 'variant_id', 'quantity']):
            continue

        product_id = item['product_id']
        variant_id = item['variant_id']
        quantity = item['quantity']

        product = Product.get_product_by_id(product_id)
        variant = ProductVariant.get_variant_by_id(variant_id)

        if product and variant:
            item_total = variant['price'] * quantity
            subtotal += item_total

            cart_details.append({
                "product_id": product_id,
                "variant_id": variant_id,
                "name": product['name'],
                "image": product['imageUrls'][0] if product.get('imageUrls') else None,
                "variant_details": {
                    "size": variant['size'],
                    "color": variant['color'],
                    "material": variant['material']
                },
                "price": variant['price'],
                "quantity": quantity,
                "total": item_total
            })

    tax = round(subtotal * 0.1, 2)
    shipping = 5.0
    grand_total = round(subtotal + tax + shipping, 2)

    return render_template(
        'cart/view_cart.html',
        cart=cart_details,
        subtotal=subtotal,
        tax=tax,
        shipping=shipping,
        grand_total=grand_total
    )




@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    """Add an item to the cart."""
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided.", "success": False}), 400

    product_id = data.get('product_id')
    variant_id = data.get('variant_id')
    quantity = data.get('quantity', 1)

    # Validate product_id and variant_id
    if not product_id or not variant_id:
        return jsonify({"message": "Product ID and Variant ID are required.", "success": False}), 400

    try:
        product_id = ObjectId(product_id)
        variant_id = ObjectId(variant_id)
    except Exception:
        return jsonify({"message": "Invalid ID format.", "success": False}), 400

    # Fetch customer
    customer_id = session.get('customer_id')
    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        return jsonify({"message": "Please log in to add items to your cart.", "success": False}), 401

    # Ensure cart exists and is properly structured
    cart = customer.get('cart', [])
    for item in cart:
        if not all(key in item for key in ['product_id', 'variant_id', 'quantity']):
            continue  # Skip invalid items

        if item['product_id'] == str(product_id) and item['variant_id'] == str(variant_id):
            item['quantity'] += quantity
            Customer.update_customer_cart(customer_id, cart)
            return jsonify({"message": "Cart updated successfully.", "success": True})

    # Add new item to cart
    cart.append({
        "product_id": str(product_id),
        "variant_id": str(variant_id),
        "quantity": quantity
    })
    Customer.update_customer_cart(customer_id, cart)

    return jsonify({"message": "Item added to cart.", "success": True})



@cart_bp.route('/remove', methods=['POST'])
def remove_from_cart():
    """Remove an item from the cart."""
    data = request.get_json()

    product_id = data.get('product_id')
    variant_id = data.get('variant_id')

    if not product_id or not variant_id:
        return jsonify({"message": "Product ID and Variant ID are required.", "success": False}), 400

    try:
        customer_id = session.get('customer_id')
        if not customer_id:
            return jsonify({"message": "User not logged in.", "success": False}), 401

        # Fetch customer data
        customer = Customer.get_customer_by_id(customer_id)
        if not customer:
            return jsonify({"message": "Customer not found.", "success": False}), 404

        # Remove item from the cart
        cart = customer.get('cart', [])
        cart = [item for item in cart if not (
            item['product_id'] == product_id and item['variant_id'] == variant_id
        )]

        # Update the cart
        Customer.update_customer_cart(customer_id, cart)
        return jsonify({"message": "Item removed successfully.", "success": True}), 200

    except Exception as e:
        return jsonify({"message": f"An error occurred: {str(e)}", "success": False}), 500






@cart_bp.route('/update', methods=['POST'])
def update_cart_quantity():
    """Update the quantity of an item in the cart."""
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided.", "success": False}), 400

    product_id = data.get('product_id')
    variant_id = data.get('variant_id')
    quantity = int(data.get('quantity', 1))

    # Validate input
    if not product_id or not variant_id:
        return jsonify({"message": "Product ID and Variant ID are required.", "success": False}), 400

    try:
        product_id = ObjectId(product_id)
        variant_id = ObjectId(variant_id)
    except Exception:
        return jsonify({"message": "Invalid ID format.", "success": False}), 400

    # Fetch customer
    customer = Customer.get_customer_by_id(session.get('customer_id'))
    if not customer:
        return jsonify({"message": "Please log in to update your cart.", "success": False}), 401

    # Update the cart
    cart = customer.get('cart', [])
    for item in cart:
        if item['product_id'] == str(product_id) and item['variant_id'] == str(variant_id):
            item['quantity'] = quantity
            Customer.update_customer_cart(customer['_id'], cart)

            # Recalculate totals
            subtotal = sum(i['price'] * i['quantity'] for i in cart)
            tax = subtotal * 0.1  # Example tax rate: 10%
            shipping = 10.00 if cart else 0.00  # Example shipping rate
            grand_total = subtotal + tax + shipping

            return jsonify({
                "message": "Cart updated successfully.",
                "success": True,
                "item_total": item['price'] * item['quantity'],
                "subtotal": subtotal,
                "tax": tax,
                "shipping": shipping,
                "grand_total": grand_total
            })

    return jsonify({"message": "Item not found in cart.", "success": False}), 404





@cart_bp.route('/clear', methods=['POST'])
def clear_cart():
    """Clear the cart."""
    customer = get_customer()
    if not customer:
        return jsonify({"message": "Please log in to clear your cart.", "success": False}), 401

    Customer.update_customer_cart(customer['_id'], [])
    return jsonify({"message": "Cart cleared.", "success": True})


def validate_cart(cart):
    """Validate cart items for required fields."""
    for item in cart:
        if 'price' not in item or 'quantity' not in item:
            raise ValueError(f"Invalid cart item: {item}")

