from . import mongo
from bson.objectid import ObjectId

class Customer:
    @staticmethod
    def get_customer_by_email(email):
        """Fetch a customer by email."""
        return mongo.db.Customer.find_one({"email": email})

    @staticmethod
    def create_customer(customer_data):
        """Insert a new customer into the database."""
        return mongo.db.Customer.insert_one(customer_data)

    @staticmethod
    def get_customer_by_id(customer_id):
        """Fetch a customer by their ID."""
        try:
            customer_id = ObjectId(customer_id)
        except Exception:
            return None
        return mongo.db.Customer.find_one({"_id": customer_id})

    @staticmethod
    def update_customer_by_id(customer_id, updated_data):
        """Update a customer's data by ID."""
        try:
            customer_id = ObjectId(customer_id)
        except Exception:
            return None
        mongo.db.Customer.update_one({"_id": customer_id}, {"$set": updated_data})

    @staticmethod
    def update_customer_cart(customer_id, cart):
        """Update the cart for a specific customer."""
        try:
            customer_id = ObjectId(customer_id)
        except Exception:
            return None
        return mongo.db.Customer.update_one({"_id": customer_id}, {"$set": {"cart": cart}})
