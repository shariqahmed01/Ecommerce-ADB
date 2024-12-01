from . import mongo
from bson.objectid import ObjectId


class Cart:
    @staticmethod
    def get_cart(customer_id):
        """Retrieve the cart for a specific customer."""
        try:
            customer_id = ObjectId(customer_id)  # Ensure customerId is an ObjectId
        except Exception:
            return None

        cart = mongo.db.Cart.find_one({"customerId": customer_id})
        if not cart:
            # If no cart exists, create an empty one
            cart = {
                "customerId": customer_id,
                "items": []  # Each item will be a dict with productId, quantity, etc.
            }
            mongo.db.Cart.insert_one(cart)
        return cart

    @staticmethod
    def add_item(customer_id, product_id, quantity=1):
        """Add an item to the cart."""
        try:
            customer_id = ObjectId(customer_id)
            product_id = ObjectId(product_id)
        except Exception:
            return False

        cart = Cart.get_cart(customer_id)

        # Check if the product already exists in the cart
        for item in cart["items"]:
            if item["productId"] == product_id:
                # If the product exists, update the quantity
                item["quantity"] += quantity
                break
        else:
            # If the product does not exist, add a new item
            cart["items"].append({"productId": product_id, "quantity": quantity})

        # Update the cart in the database
        mongo.db.Cart.update_one(
            {"customerId": customer_id},
            {"$set": {"items": cart["items"]}}
        )
        return True

    @staticmethod
    def remove_item(customer_id, product_id):
        """Remove an item from the cart."""
        try:
            customer_id = ObjectId(customer_id)
            product_id = ObjectId(product_id)
        except Exception:
            return False

        cart = Cart.get_cart(customer_id)
        cart["items"] = [item for item in cart["items"] if item["productId"] != product_id]

        # Update the cart in the database
        mongo.db.Cart.update_one(
            {"customerId": customer_id},
            {"$set": {"items": cart["items"]}}
        )
        return True

    @staticmethod
    def clear_cart(customer_id):
        """Clear all items from the cart."""
        try:
            customer_id = ObjectId(customer_id)
        except Exception:
            return False

        mongo.db.Cart.update_one(
            {"customerId": customer_id},
            {"$set": {"items": []}}
        )
        return True

    @staticmethod
    def get_cart_total(customer_id):
        """Calculate the total price of items in the cart."""
        try:
            customer_id = ObjectId(customer_id)
        except Exception:
            return 0.0

        cart = Cart.get_cart(customer_id)
        total = 0.0

        # Fetch product details to calculate the total
        for item in cart["items"]:
            product = mongo.db.Product.find_one({"_id": item["productId"]})

