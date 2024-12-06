from flask import Blueprint, request, jsonify, flash, session, redirect, url_for, render_template

from app.models.category import Category, Subcategory
from app.models.customer import Customer
from app.models.order import Order
from app.models.product import Product
from services.admin_service import add_product, update_product, delete_product

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/product', methods=['POST'])
def add_product_route():
    data = request.json
    response = add_product(data)
    return jsonify(response)

@admin_bp.route('/product/<product_id>', methods=['PUT'])
def update_product_route(product_id):
    data = request.json
    response = update_product(product_id, data)
    return jsonify(response)

@admin_bp.route('/product/<product_id>', methods=['DELETE'])
def delete_product_route(product_id):
    response = delete_product(product_id)
    return jsonify(response)


@admin_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """Admin dashboard page."""
    if not session.get('is_admin'):
        flash("Unauthorized access.", "danger")
        return redirect(url_for('auth.login'))
    return render_template('admin/dashboard.html')


# View all products
@admin_bp.route('/products', methods=['GET'])
def manage_products():
    """Admin view for managing products."""
    products = Product.get_all_products()
    return render_template('admin/manage_products.html', products=products)

# Add a new product
@admin_bp.route('/products/add', methods=['POST'])
def add_product():
    """Admin action to add a new product."""
    product_data = {
        "name": request.form.get('name'),
        "description": request.form.get('description'),
        "price": float(request.form.get('price')),
        "countInStock": int(request.form.get('countInStock')),
        "imageUrls": [request.form.get('imageUrl')],
        "isFeatured": request.form.get('isFeatured') == 'on',
        "isTrending": request.form.get('isTrending') == 'on'
    }
    Product.create_product(product_data)
    flash("Product added successfully!", "success")
    return redirect(url_for('admin.manage_products'))

# Edit an existing product
@admin_bp.route('/products/edit/<product_id>', methods=['POST'])
def edit_product(product_id):
    """Admin action to edit an existing product."""
    updated_data = {
        "name": request.form.get('name'),
        "description": request.form.get('description'),
        "price": float(request.form.get('price')),
        "countInStock": int(request.form.get('countInStock')),
        "imageUrls": [request.form.get('imageUrl')],
        "isFeatured": request.form.get('isFeatured') == 'on',
        "isTrending": request.form.get('isTrending') == 'on'
    }
    Product.update_product(product_id, updated_data)
    flash("Product updated successfully!", "success")
    return redirect(url_for('admin.manage_products'))

# Remove a product
@admin_bp.route('/products/remove/<product_id>', methods=['POST'])
def remove_product(product_id):
    """Admin action to remove a product."""
    Product.delete_product(product_id)
    flash("Product removed successfully!", "success")
    return redirect(url_for('admin.manage_products'))

# View all orders



# Update the status of an order
@admin_bp.route('/orders/update/<order_id>', methods=['POST'])
def update_order_status(order_id):
    """Admin action to update the status of an order."""
    new_status = request.form.get('status')
    Order.update_order_status(order_id, new_status)
    flash("Order status updated successfully!", "success")
    return redirect(url_for('admin.manage_orders'))

