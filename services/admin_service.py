from app.models.product import Product

def add_product(product_data):
    """Add a new product."""
    Product.create_product(product_data)
    return {"message": "Product added successfully.", "success": True}

def update_product(product_id, updated_data):
    """Update an existing product."""
    Product.update_product(product_id, updated_data)
    return {"message": "Product updated successfully.", "success": True}

def delete_product(product_id):
    """Delete a product."""
    Product.delete_product(product_id)
    return {"message": "Product deleted successfully.", "success": True}
