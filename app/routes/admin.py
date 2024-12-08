from flask import Blueprint, request, jsonify, flash, session, redirect, url_for, render_template

from app.models import mongo
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


@admin_bp.route('/products', methods=['GET'])
def manage_products():
    """Admin view for managing products."""
    products = Product.get_all_products()
    categories = Category.get_all_categories()  # Fetch all categories
    subcategories = Subcategory.get_all_subcategories()  # Fetch all subcategories
    return render_template(
        'admin/manage_products.html',
        products=products,
        categories=categories,
        subcategories=subcategories
    )

@admin_bp.route('/products/add', methods=['POST'])
def add_product():
    try:
        # Extract and validate mandatory fields
        name = request.form.get('name')
        description = request.form.get('description')
        category_id = request.form.get('categoryId')
        subcategory_id = request.form.get('subcategoryId')

        if not all([name, description, category_id, subcategory_id]):
            flash("All mandatory fields must be filled.", "danger")
            return redirect(url_for('admin.manage_products'))

        # Validate that subcategory belongs to the selected category
        valid_subcategories = Subcategory.get_subcategories_by_category_id(category_id)
        if not any(sub['_id'] == subcategory_id for sub in valid_subcategories):
            flash("Invalid subcategory for the selected category.", "danger")
            return redirect(url_for('admin.manage_products'))

        # Process image URLs
        image_urls = request.form.get('imageUrls', '').split(',')
        image_urls = [url.strip() for url in image_urls if url.strip()]

        # Parse variants from the form
        variants = []
        for key, value in request.form.items():
            if key.startswith('variants['):
                index, field = key.split('[')[1].split(']')[0], key.split('][')[1].split(']')[0]
                while len(variants) <= int(index):
                    variants.append({})
                variants[int(index)][field] = value

        # Ensure no duplicate variants
        seen_variants = set()
        for variant in variants:
            key = (variant.get('size'), variant.get('color'), variant.get('material'))
            if key in seen_variants:
                flash("Duplicate variants are not allowed.", "danger")
                return redirect(url_for('admin.manage_products'))
            seen_variants.add(key)

        # Save product variants in ProductVariant collection
        variant_ids = []
        for variant in variants:
            variant_data = {
                "size": variant.get("size"),
                "color": variant.get("color"),
                "material": variant.get("material"),
                "stockQuantity": int(variant.get("stockQuantity", 0)),
                "price": float(variant.get("price", 0.0))
            }
            variant_result = mongo.db.ProductVariant.insert_one(variant_data)
            variant_ids.append(str(variant_result.inserted_id))  # Store variant IDs as strings

        # Construct and save product data in Product collection
        product_data = {
            "name": name,
            "description": description,
            "categoryId": str(category_id),  # Save categoryId as string
            "subcategoryId": str(subcategory_id),  # Save subcategoryId as string
            "imageUrls": image_urls,
            "isTrending": request.form.get('isTrending') == 'on',
            "productVariantIds": variant_ids  # Save variant IDs as strings
        }
        mongo.db.Product.insert_one(product_data)

        flash("Product created successfully!", "success")
        return redirect(url_for('admin.manage_products'))

    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
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

@admin_bp.route('/orders', methods=['GET'])
def manage_orders():
    """Admin view for managing orders."""
    # Fetch all orders from the database
    orders = Order.get_all_orders()

    # Enrich orders with customer usernames
    for order in orders:
        customer = Customer.get_customer_by_id(order['customerId'])
        order['customerName'] = customer.get('username', 'Unknown Customer') if customer else 'Unknown Customer'

    return render_template('admin/manage_orders.html', orders=orders)



