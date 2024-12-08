from datetime import datetime
from bson.objectid import ObjectId
from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from app.models.product import Product
from app.models.customer import Customer
from app.models.order import Order  # Assuming you have an Order model
from app.models.productvariant import ProductVariant  # Assuming you have a ProductVariant model

checkout_bp = Blueprint('checkout', __name__, url_prefix='/checkout')


@checkout_bp.route('/', methods=['GET'])
def checkout():
    """Display the checkout page."""
    customer_id = session.get('customer_id')
    if not customer_id:
        flash("Please log in to proceed to checkout.", "danger")
        return redirect(url_for('auth.login'))

    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        flash("Customer not found.", "danger")
        return redirect(url_for('auth.login'))

    cart = customer.get('cart', [])
    cart_details = []
    subtotal = 0

    for item in cart:
        product_id = item.get('productId') or item.get('product_id')
        variant_id = item.get('variantId') or item.get('variant_id')

        # Ensure both product and variant IDs exist
        if not product_id or not variant_id:
            continue

        product = Product.get_product_by_id(product_id)
        variant = ProductVariant.get_variant_by_id(variant_id)

        if product and variant:
            item_total = variant['price'] * item['quantity']
            subtotal += item_total
            cart_details.append({
                "name": product['name'],
                "image": product['imageUrls'][0] if product.get('imageUrls') else None,
                "price": variant['price'],
                "quantity": item['quantity'],
                "variant_details": {
                    "size": variant['size'],
                    "color": variant['color'],
                    "material": variant['material']
                },
                "total": round(item_total, 2)
            })

    # Calculate totals
    tax = round(subtotal * 0.1, 2)  # 10% tax
    shipping = 5.0  # Fixed shipping charge
    grand_total = round(subtotal + tax + shipping, 2)

    return render_template(
        'checkout/checkout.html',
        cart=cart_details,
        subtotal=round(subtotal, 2),
        tax=tax,
        shipping=shipping,
        grand_total=grand_total
    )



@checkout_bp.route('/process_payment', methods=['POST'])
def process_payment():
    """Process payment and create an order."""
    address = request.form.get('address')
    contact = request.form.get('contact')
    payment_method = request.form.get('payment_method')

    customer_id = session.get('customer_id')
    customer = Customer.get_customer_by_id(customer_id)
    if not customer:
        flash("Please log in to complete the checkout.", "danger")
        return redirect(url_for('auth.login'))

    cart = customer.get('cart', [])
    if not cart:
        flash("Your cart is empty.", "warning")
        return redirect(url_for('cart.view_cart_page'))

    total_amount = 0
    processed_cart = []  # Prepare cart items with details for the order

    for item in cart:
        product_id = item.get('productId') or item.get('product_id')
        variant_id = item.get('variantId') or item.get('variant_id')
        quantity = item.get('quantity', 0)

        if not product_id or not variant_id:
            continue

        product = Product.get_product_by_id(product_id)
        variant = ProductVariant.get_variant_by_id(variant_id)

        if product and variant:
            item_total = variant['price'] * quantity
            total_amount += item_total
            processed_cart.append({
                "product_id": str(product_id),
                "variant_id": str(variant_id),
                "quantity": quantity,
                "price": variant['price'],  # Include price to avoid recalculating later
                "total": round(item_total, 2)
            })

    if not processed_cart:
        flash("Unable to process your cart. Please check the items.", "danger")
        return redirect(url_for('cart.view_cart_page'))

    # Prepare order data
    order_data = {
        "customerId": ObjectId(customer_id),
        "orderDate": datetime.now(),
        "items": processed_cart,
        "totalAmount": round(total_amount, 2),
        "status": "pending",
        "shippingAddress": address,
        "contact": contact,
        "paymentMethod": payment_method
    }

    # Insert order into the database
    order_id = Order.create_order(order_data)

    # Clear customer's cart
    Customer.update_customer_cart(customer['_id'], [])


    flash(f"Payment successful! Order #{str(order_id)} is being processed.", "success")
    return redirect(url_for('home.index'))


@checkout_bp.route('/success/<order_id>', methods=['GET'])
def success_page(order_id):
    """Display the success page after payment."""
    return render_template('checkout/success.html', order_id=order_id)

