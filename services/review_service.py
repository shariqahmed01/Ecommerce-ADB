from app.models.review import Review

def get_reviews(product_id):
    """Retrieve reviews for a product."""
    reviews = Review.get_reviews_by_product(product_id)
    return {"success": True, "reviews": reviews}

def add_review(review_data):
    """Add a new review."""
    Review.create_review(review_data)
    return {"message": "Review added successfully.", "success": True}
