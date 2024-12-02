from . import mongo
from bson.objectid import ObjectId


class Product:
    @staticmethod
    def get_all_products(filters=None):
        """Fetch all products with optional filters."""
        query = filters if isinstance(filters, dict) else {}
        return list(mongo.db.Product.find(query))

    @staticmethod
    def get_product_by_id(product_id):
        """Fetch a single product by its ID."""
        try:
            product_id = ObjectId(product_id)
        except Exception:
            return None  # Return None if the ID is invalid
        return mongo.db.Product.find_one({"_id": product_id})

    @staticmethod
    def create_product(product_data):
        """Insert a new product."""
        result = mongo.db.Product.insert_one(product_data)
        return result.inserted_id  # Return the inserted ID

    @staticmethod
    def update_product(product_id, updated_data):
        """Update an existing product by its ID."""
        try:
            product_id = ObjectId(product_id)
        except Exception:
            return None  # Return None if the ID is invalid
        return mongo.db.Product.update_one({"_id": product_id}, {"$set": updated_data})

    @staticmethod
    def delete_product(product_id):
        """Delete a product by its ID."""
        try:
            product_id = ObjectId(product_id)
        except Exception:
            return None  # Return None if the ID is invalid
        return mongo.db.Product.delete_one({"_id": product_id})

    @staticmethod
    def get_featured_products():
        """Fetch featured products from the database."""
        products = mongo.db.Product.find({"isFeatured": True})  # Example filter
        # Convert ObjectId to string and format data
        return [
            {**product, "_id": str(product["_id"])} for product in products
        ]


