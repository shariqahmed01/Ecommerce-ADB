from . import mongo
from bson.objectid import ObjectId

class Review:
    @staticmethod
    def get_reviews_by_product_id(product_id):
        """Fetch all reviews for a specific product."""
        try:
            product_id = ObjectId(product_id)  # Ensure productId is an ObjectId
        except Exception as e:
            return []

        reviews = mongo.db.Review.find({"productId": product_id})
        # Convert ObjectId to string for template compatibility
        return [
            {
                **review,
                "_id": str(review["_id"]),
                "productId": str(review["productId"]),
                "customerId": str(review["customerId"]),
                "reviewDate": review["reviewDate"].strftime("%Y-%m-%d")
            }
            for review in reviews
        ]
