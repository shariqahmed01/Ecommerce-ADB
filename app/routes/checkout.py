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
    customer_id = session.get('customer_id')

    if not customer_id:
        return redirect(url_for('auth.login'))

    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        return redirect(url_for('auth.login'))

    cart = customer.get('cart', [])
    subtotal = sum(item['quantity'] * Product.get_product_by_id(item['productId'])['price'] for item in cart)
    tax = round(subtotal * 0.1, 2)  # 10% tax
    shipping = 5.0  # Fixed shipping charge
    grand_total = round(subtotal + tax + shipping, 2)

    cart_details = []
    for item in cart:
        product = Product.get_product_by_id(item['productId'])
        if product:
            cart_details.append({
                "name": product['name'],
                "price": product['price'],
                "quantity": item['quantity'],
                "total": round(product['price'] * item['quantity'], 2)
            })

    return render_template(
        'checkout/checkout.html',
        cart=cart_details,
        subtotal=subtotal,
        tax=tax,
        shipping=shipping,
        grand_total=grand_total
    )


@checkout_bp.route('/process_payment', methods=['POST'])
def process_payment():
    if session.get('order_placed', False):
        return jsonify({"message": "Order already placed.", "success": False}), 400

    address = request.form.get('address')
    contact = request.form.get('contact')
    payment_method = request.form.get('payment_method')

    customer_id = session.get('customer_id')
    customer = Customer.get_customer_by_id(customer_id)

    if not customer:
        return jsonify({"message": "Customer not found.", "success": False}), 400

    cart = customer.get('cart', [])
    total_amount = sum(item['quantity'] * Product.get_product_by_id(item['productId'])['price'] for item in cart)

    # Create the order
    order_data = {
        "customerId": ObjectId(customer_id),
        "orderDate": datetime.utcnow(),
        "items": cart,
        "totalAmount": total_amount,
        "status": "pending",
        "shippingAddress": address,
        "contact": contact,
        "paymentMethod": payment_method
    }

    order_id = Order.create_order(order_data)

    session['order_placed'] = True
    Customer.update_customer_cart(customer['_id'], [])

    return jsonify({
        "message": "Payment successful. Order is being processed.",
        "order_id": str(order_id),
        "success": True
    })

