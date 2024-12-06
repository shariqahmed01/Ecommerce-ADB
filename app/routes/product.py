from bson import ObjectId
from flask import Blueprint, request, jsonify, render_template, abort, flash, redirect, url_for

from app.models import mongo
from app.models.category import Subcategory, Category
from app.models.product import Product
from app.models.productvariant import ProductVariant
from app.routes.review import list_reviews
from services.product_service import get_products, get_product_by_id

product_bp = Blueprint('product', __name__, url_prefix='/products')


@product_bp.route('/', methods=['GET'])
def list_products():
    """Display a list of products."""
    filters = request.args.to_dict()
    products = get_products(filters)

    # Convert ObjectId to string
    for product in products["products"]:
        product["_id"] = str(product["_id"])

    return render_template('products/product_list.html', products=products["products"])


from app.models.review import Review

@product_bp.route('/details/<product_id>', methods=['GET'])
def product_details(product_id):
    """
    Display product details including variants and reviews.
    """
    try:
        # Fetch product details
        product = Product.get_product_details(product_id)
        if not product:
            flash("Product not found.", "danger")
            return redirect(url_for('product.list_products'))

        # Get the default variant and all variants for the product
        default_variant = product.get("defaultVariant")
        variants = product.get("variants", [])
        if not default_variant and variants:
            default_variant = variants[0]  # Assign the first variant as the default

        # Fetch reviews for the product
        reviews = Review.get_reviews_by_product_id(product_id)

        # Render the product details page
        return render_template(
            'products/product_detail.html',
            product=product,
            variant=default_variant,
            reviews=reviews
        )
    except Exception as e:
        # Log the error and redirect with a flash message
        flash(f"An error occurred while loading product details: {str(e)}", "danger")
        return redirect(url_for('product.list_products'))


@product_bp.route('/filter', methods=['GET'])
def filter_products():
    filters = {}
    category = request.args.get('category')
    subcategory = request.args.get('subcategory')
    size = request.args.get('size')
    color = request.args.get('color')
    material = request.args.get('material')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort = request.args.get('sort')

    if category:
        filters['category'] = category
    if subcategory:
        filters['subcategory'] = subcategory
    if size:
        filters['size'] = size
    if color:
        filters['color'] = color
    if material:
        filters['material'] = material
    if min_price is not None:
        filters


@product_bp.route('/', methods=['GET'])
def product_list():
    """Display a filtered list of products."""
    filters = {}
    variant_filters = {}

    # Collect filters from query parameters
    category_id = request.args.get('categoryId')
    subcategory_id = request.args.get('subcategoryId')
    size = request.args.get('size')
    color = request.args.get('color')
    material = request.args.get('material')
    min_price = request.args.get('minPrice', type=float)
    max_price = request.args.get('maxPrice', type=float)

    # Build filters
    if category_id:
        filters["categoryId"] = ObjectId(category_id)
    if subcategory_id:
        filters["subcategoryId"] = ObjectId(subcategory_id)
    if size:
        variant_filters["size"] = size
    if color:
        variant_filters["color"] = color
    if material:
        variant_filters["material"] = material
    if min_price is not None:
        variant_filters["price"] = {"$gte": min_price}
    if max_price is not None:
        if "price" in variant_filters:
            variant_filters["price"]["$lte"] = max_price
        else:
            variant_filters["price"] = {"$lte": max_price}

    # Fetch products and related categories/subcategories
    products = Product.get_filtered_products(filters, variant_filters)
    categories = Category.get_all_categories()
    subcategories = Subcategory.get_all_subcategories()

    return render_template(
        'products/product_list.html',
        products=products,
        categories=categories,
        subcategories=subcategories
    )

@staticmethod
def get_product_details(product_id):
    """Fetch detailed information for a product, including variants."""
    try:
        product_id = ObjectId(product_id)
    except Exception:
        return None

    # Fetch the product
    product = mongo.db.Product.find_one({"_id": product_id})
    if not product:
        return None

    # Fetch associated variants
    variants = list(mongo.db.ProductVariant.find({"productId": product["_id"]}))
    for variant in variants:
        variant["_id"] = str(variant["_id"])  # Convert ObjectId to string

    product["_id"] = str(product["_id"])
    product["variants"] = variants if variants else []  # Ensure `variants` is always a list
    return product

