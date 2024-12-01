from app.models.product import Product
from bson.objectid import ObjectId, InvalidId

def get_products(filters=None):
    """Fetch products with optional filters."""
    try:
        products = Product.get_all_products(filters)
        return {"success": True, "products": products}
    except Exception as e:
        return {"success": False, "message": f"Failed to fetch products: {str(e)}"}

def get_product_by_id(product_id):
    """Fetch a single product by ID."""
    try:
        # Ensure product_id is a valid ObjectId
        product_id = ObjectId(product_id)
    except InvalidId:
        return {"success": False, "message": "Invalid product ID format."}

    product = Product.get_product_by_id(product_id)
    if not product:
        return {"success": False, "message": "Product not found."}

    return {"success": True, "product": product}
