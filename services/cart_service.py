from app.models.customer import Customer

def get_cart(user_id):
    """Retrieve the user's shopping cart."""
    user = Customer.get_customer_by_email(user_id)
    if not user or "cart" not in user:
        return {"success": True, "cart": []}
    return {"success": True, "cart": user['cart']}

def add_to_cart(data):
    """Add an item to the user's cart."""
    user = Customer.get_customer_by_email(data['user_id'])
    if not user:
        return {"message": "User not found.", "success": False}

    item = {
        "product_id": data['product_id'],
        "quantity": data['quantity'],
    }
    user['cart'].append(item)
    Customer.update_customer(user['_id'], {"cart": user['cart']})
    return {"message": "Item added to cart.", "success": True}

def remove_from_cart(data):
    """Remove an item from the user's cart."""
    user = Customer.get_customer_by_email(data['user_id'])
    if not user:
        return {"message": "User not found.", "success": False}

    user['cart'] = [
        item for item in user['cart']
        if item['product_id'] != data['product_id']
    ]
    Customer.update_customer(user['_id'], {"cart": user['cart']})
    return {"message": "Item removed from cart.", "success": True}
