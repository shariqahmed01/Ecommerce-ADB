from app.models.order import Order

def place_order(order_data):
    """Place a new order."""
    Order.create_order(order_data)
    return {"message": "Order placed successfully.", "success": True}

def get_orders(user_id):
    """Retrieve orders for a specific user."""
    orders = Order.get_orders_by_customer(user_id)
    return {"success": True, "orders": orders}
