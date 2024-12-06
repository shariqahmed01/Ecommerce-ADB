from . import mongo
from bson.objectid import ObjectId

from .productvariant import ProductVariant


class Product:

    @staticmethod
    def get_product_by_id(product_id):
        return mongo.db.Product.find_one({"_id": ObjectId(product_id)})

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

    @staticmethod
    def get_product_by_id(product_id):
        """Fetch a product by its ID."""
        try:
            product_id = ObjectId(product_id)
        except Exception:
            return None
        return mongo.db.Product.find_one({"_id": product_id})

    @staticmethod
    def add_review(review_data):
        """Add a review to a product."""
        product_id = review_data.get("productId")
        if not product_id:
            raise ValueError("Product ID is required to add a review.")

        try:
            product_id = ObjectId(product_id)
        except Exception as e:
            raise ValueError(f"Invalid Product ID: {e}")

        review = {
            "customerId": review_data.get("customerId"),
            "rating": review_data.get("rating"),
            "comment": review_data.get("comment"),
            "reviewDate": review_data.get("reviewDate"),
        }

        return mongo.db.Product.update_one(
            {"_id": product_id},
            {"$push": {"reviews": review}}
        )

    @staticmethod
    def get_products_by_subcategory(subcategory_id):
        try:
            subcategory_id = ObjectId(subcategory_id)
        except Exception:
            return []
        return list(mongo.db.Product.find({"subcategoryId": subcategory_id}))

    @staticmethod
    def get_product_details(product_id):
        """Fetch detailed information for a product, including variants."""
        product = mongo.db.Product.find_one({"_id": ObjectId(product_id)})
        if not product:
            return None

        # Fetch associated variants using the `productVariantIds`
        variant_ids = [ObjectId(variant_id) for variant_id in product["productVariantIds"]]
        variants = list(mongo.db.ProductVariant.find({"_id": {"$in": variant_ids}}))

        # Convert ObjectId to string for compatibility
        for variant in variants:
            variant["_id"] = str(variant["_id"])

        product["_id"] = str(product["_id"])
        product["variants"] = variants
        product["defaultVariant"] = variants[0] if variants else None
        return product

    @staticmethod
    def get_all_products(query=None):
        """Fetch all products matching the given query."""
        if query is None:
            query = {}

        products = list(mongo.db.Product.find(query))
        for product in products:
            product["_id"] = str(product["_id"])

            # Fetch the cheapest variant price for display
            variants = list(mongo.db.ProductVariant.find({"productId": ObjectId(product["_id"])}))
            if variants:
                product["price"] = min(variant["price"] for variant in variants)
            else:
                product["price"] = "N/A"
        return products

    @staticmethod
    def get_filtered_products(filters, variant_filters):
        """Fetch products and optionally filter by variants."""
        products = list(mongo.db.Product.find(filters))
        for product in products:
            product["_id"] = str(product["_id"])
            # Attach variants filtered by variant_filters
            variants = list(mongo.db.ProductVariant.find({"productId": product["_id"], **variant_filters}))
            for variant in variants:
                variant["_id"] = str(variant["_id"])
            product["variants"] = variants
        return products


