from datetime import datetime
from bson.objectid import ObjectId
from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from app.models.product import Product
from app.models.customer import Customer
from app.models.order import Order  # Assuming you have an Order model
from app.models.productvariant import ProductVariant  # Assuming you have a ProductVariant model

checkout_bp = Blueprint('checkout', __name__, url_prefix='/checkout')


@checkout_bp.route('/', methods=['GET'])
def checkout():
    """Render the checkout page."""
    # Get the current customer's cart
    customer_id = session.get('customer_id')

    if not customer_id:
        return redirect(url_for('auth.login'))  # Redirect to login if not logged in

    customer = Customer.get_customer_by_id(customer_id)
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

    # You can also fetch shipping info here (address, contact, etc.)
    return render_template('checkout/checkout.html', cart=cart_details)

@checkout_bp.route('/process_payment', methods=['POST'])
def process_payment():
    """Process payment and complete the order."""
    # Check if order has already been placed in the session
    if session.get('order_placed', False):
        return jsonify({"message": "Order already placed. Redirecting...", "success": False}), 400

    # Capture shipping information
    address = request.form.get('address')
    contact = request.form.get('contact')

    # Process the payment (this is just a placeholder for actual payment gateway integration)
    payment_successful = True  # Assume the payment was successful for now

    if payment_successful:
        # Get the current customer
        customer_id = session.get('customer_id')
        customer = Customer.get_customer_by_id(customer_id)

        if not customer:
            return jsonify({"message": "Customer not found.", "success": False}), 400

        # Get the cart from the customer's data
        cart = customer.get('cart', [])
        items = []

        # Prepare the order items
        total_amount = 0
        for item in cart:
            product = Product.get_product_by_id(item['productId'])
            variant = ProductVariant.get_variant_by_id(item.get('variant_id'))

            if product:
                # Calculate total price for the items
                total_amount += product['price'] * item['quantity']

                # Add item details
                items.append({
                    "productId": ObjectId(item['productId']),
                    "variantId": ObjectId(item['variant_id']) if variant else None,
                    "quantity": item['quantity'],
                    "price": product['price']
                })

        # Create the order
        order_data = {
            "customerId": ObjectId(customer_id),
            "orderDate": datetime.utcnow(),
            "items": items,
            "totalAmount": total_amount,
            "status": "pending",  # Status can be changed later to "completed", "shipped", etc.
            "shippingAddress": address,
            "contact": contact
        }

        # Insert the order into the database
        order_id = Order.create_order(order_data)

        # Mark that the order has been placed in the session to prevent duplicates
        session['order_placed'] = True

        # Clear the cart after successful order placement
        Customer.update_customer_cart(customer['_id'], [])

        return jsonify({
            "message": "Payment successful. Your order is being processed.",
            "order_id": str(order_id),
            "success": True
        })

    else:
        return jsonify({"message": "Payment failed. Please try again.", "success": False}), 500
