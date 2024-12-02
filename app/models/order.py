from . import mongo
from bson.objectid import ObjectId
from datetime import datetime

class Order:
    @staticmethod
    def create_order(order_data):
        """Create a new order and insert it into the database."""
        order_data["orderDate"] = datetime.utcnow()  # Ensure the order date is set to now
        result = mongo.db.Order.insert_one(order_data)
        return result.inserted_id

    @staticmethod
    def get_order_by_id(order_id):
        """Fetch an order by its ID."""
        try:
            order_id = ObjectId(order_id)
        except Exception:
            return None
        return mongo.db.Order.find_one({"_id": order_id})

    @staticmethod
    def update_order_status(order_id, status):
        """Update the status of an order."""
        try:
            order_id = ObjectId(order_id)
        except Exception:
            return None
        return mongo.db.Order.update_one({"_id": order_id}, {"$set": {"status": status}})
