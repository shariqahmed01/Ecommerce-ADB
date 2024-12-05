from flask import Blueprint, render_template, session, redirect, url_for, request, flash, jsonify
from app.models.customer import Customer
from app.models.order import Order
from app.models.product import Product
from bson.objectid import ObjectId
from datetime import datetime

from app.models.review import Review
from services.order_service import place_order, get_orders

order_bp = Blueprint('order', __name__, url_prefix='/orders')

@order_bp.route('/', methods=['POST'])
def create_order():
    data = request.json
    response = place_order(data)
    return jsonify(response)


@order_bp.route('/', methods=['GET'])
def list_orders():
    """Fetch and return all orders for the logged-in customer."""
    customer_id = session.get('customer_id')
    if not customer_id:
        return jsonify({"message": "Please log in to view your orders.", "success": False}), 401

    # Fetch orders
    orders = Order.get_orders_by_customer_id(customer_id)

    # Serialize ObjectId and datetime fields
    formatted_orders = []
    for order in orders:
        formatted_order = {
            "_id": str(order["_id"]),
            "customerId": str(order["customerId"]),
            "orderDate": order["orderDate"].isoformat() if isinstance(order["orderDate"], datetime) else order[
                "orderDate"],
            "items": [
                {
                    "productId": str(item["productId"]),
                    "variantId": str(item.get("variantId")) if item.get("variantId") else None,
                    "quantity": item.get("quantity", 0),  # Default quantity to 0 if missing
                    "price": item.get("price", 0.0)  # Default price to 0.0 if missing
                }
                for item in order["items"]
            ],
            "totalAmount": order.get("totalAmount", 0.0),  # Default totalAmount to 0.0 if missing
            "status": order.get("status", "unknown"),  # Default status to "unknown" if missing
            "shippingAddress": order.get("shippingAddress", ""),
            "contact": order.get("contact", ""),
            "paymentMethod": order.get("paymentMethod", "")
        }
        formatted_orders.append(formatted_order)

    return jsonify({"success": True, "orders": formatted_orders})


@order_bp.route('/view', methods=['GET'])
def view_orders():
    """Display the customer's orders."""
    customer_id = session.get('customer_id')
    if not customer_id:
        flash("Please log in to view your orders.", "danger")
        return redirect(url_for('auth.login'))

    orders = Order.get_orders_by_customer_id(customer_id)
    formatted_orders = []

    for order in orders:
        items = []
        for item in order['items']:
            product = Product.get_product_by_id(item['productId'])
            if product:
                items.append({
                    "product_id": str(item['productId']),
                    "name": product['name'],
                    "image": product['imageUrls'][0] if product.get('imageUrls') else url_for('static', filename='images/default-product.jpg'),
                    "price": item.get('price', 0.0),
                    "quantity": item.get('quantity', 0),
                    "total": item.get('price', 0.0) * item.get('quantity', 0)
                })
        formatted_orders.append({
            "order_id": str(order['_id']),
            "order_date": order['orderDate'].strftime("%Y-%m-%d %H:%M:%S"),
            "status": order.get('status', 'unknown'),
            "items": items,
            "total_amount": order.get('totalAmount', 0.0)
        })

    return render_template('orders/view_orders.html', orders=formatted_orders)



@order_bp.route('/review/<product_id>', methods=['POST'])
def submit_review(product_id):
    """Submit a review for a delivered product."""
    customer_id = session.get('customer_id')
    if not customer_id:
        flash("Please log in to submit a review.", "danger")
        return redirect(url_for('auth.login'))

    review_data = {
        "customerId": ObjectId(customer_id),
        "productId": ObjectId(product_id),
        "rating": int(request.form.get('rating')),
        "comment": request.form.get('comment'),
        "reviewDate": datetime.utcnow()
    }

    # Add review to the product
    Product.add_review(review_data)

    flash("Review submitted successfully.", "success")
    return redirect(url_for('order.view_orders'))

@order_bp.route('/review/<product_id>', methods=['POST'], endpoint="submit_product_review")
def submit_review(product_id):
    """Submit a review for a delivered product."""
    customer_id = session.get('customer_id')
    if not customer_id:
        flash("Please log in to submit a review.", "danger")
        return redirect(url_for('auth.login'))

    # Collect review data from form
    review_data = {
        "customerId": ObjectId(customer_id),
        "productId": ObjectId(product_id),
        "rating": int(request.form.get('rating')),
        "comment": request.form.get('comment'),
        "reviewDate": datetime.utcnow()
    }

    try:
        # Save review to the Review model
        Review.create_review(review_data)
        flash("Review submitted successfully.", "success")
    except Exception as e:
        flash(f"Error submitting review: {str(e)}", "danger")

    return redirect(url_for('order.view_orders'))