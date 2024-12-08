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
    """Display a list of products with price ranges."""
    filters = request.args.to_dict()
    products = Product.get_all_products(filters)

    return render_template('products/product_list.html', products=products)




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
    """Filter products based on category, subcategory, and product variants."""
    filters = {}
    variant_filters = {}

    # Collect filter criteria
    category_id = request.args.get('categoryId')
    subcategory_id = request.args.get('subcategoryId')
    size = request.args.get('size')
    color = request.args.get('color')
    material = request.args.get('material')
    min_price = request.args.get('minPrice', type=float)
    max_price = request.args.get('maxPrice', type=float)

    # Apply category and subcategory filters
    if category_id:
        try:
            filters["categoryId"] = ObjectId(category_id)
        except Exception:
            return jsonify({"error": "Invalid category ID"}), 400

    if subcategory_id:
        try:
            filters["subcategoryId"] = ObjectId(subcategory_id)
        except Exception:
            return jsonify({"error": "Invalid subcategory ID"}), 400

    # Apply variant filters
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

    # Fetch products and categories/subcategories
    products = Product.get_filtered_products(filters, variant_filters)
    categories = Category.get_all_categories()
    subcategories = Subcategory.get_all_subcategories()

    return render_template(
        'products/product_list.html',
        products=products,
        categories=categories,
        subcategories=subcategories,
        selected_category=category_id,
        selected_subcategory=subcategory_id
    )


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
        product = mongo.db.Product.find_one({"_id": ObjectId(product_id)})
        if not product:
            return None

        product["_id"] = str(product["_id"])
        product["categoryId"] = str(product["categoryId"])
        product["subcategoryId"] = str(product["subcategoryId"])

        # Fetch associated variants
        variant_ids = [ObjectId(variant_id) for variant_id in product.get("productVariantIds", [])]
        variants = list(mongo.db.ProductVariant.find({"_id": {"$in": variant_ids}}))

        # Add variants and default variant
        product["variants"] = variants
        if variants:
            product["defaultVariant"] = variants[0]  # Use the first variant as the default
        else:
            product["defaultVariant"] = None

        return product
    except Exception as e:
        raise Exception(f"Error fetching product details: {e}")




@product_bp.route('/create', methods=['POST'])
def create_product():
    try:
        # Extract data from the request
        data = request.get_json()

        # Insert product variants and collect their IDs
        variants = data.get("variants", [])
        variant_ids = []
        for variant in variants:
            variant_data = {
                "size": variant.get("size"),
                "color": variant.get("color"),
                "material": variant.get("material"),
                "stockQuantity": int(variant.get("stockQuantity", 0)),
                "price": float(variant.get("price", 0.0)),
            }
            variant_result = mongo.db.ProductVariant.insert_one(variant_data)
            variant_ids.append(str(variant_result.inserted_id))  # Convert variantId to string

        # Prepare product data with correct format
        product_data = {
            "name": data.get("name"),
            "description": data.get("description"),
            "categoryId": str(data.get("categoryId")),  # Save categoryId as string
            "subcategoryId": str(data.get("subcategoryId")),  # Save subcategoryId as string
            "imageUrls": data.get("imageUrls", []),
            "isTrending": data.get("isTrending", False),
            "productVariantIds": variant_ids  # Save variant IDs as strings
        }

        # Insert product into the database
        product_result = mongo.db.Product.insert_one(product_data)
        product_id = product_result.inserted_id

        # Response
        return jsonify({
            "message": "Product and variants created successfully.",
            "productId": str(product_id),
            "productVariantIds": variant_ids
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@product_bp.route('/api/subcategories', methods=['GET'])
def get_subcategories():
    category_id = request.args.get('categoryId')
    if not category_id:
        print("No categoryId provided")
        return jsonify([])

    try:
        print(f"Fetching subcategories for categoryId: {category_id}")
        subcategories = Subcategory.get_subcategories_by_category_id(category_id)
        print(f"Subcategories fetched: {subcategories}")
        return jsonify([{"_id": str(sub["_id"]), "name": sub["name"]} for sub in subcategories])
    except Exception as e:
        print(f"Error fetching subcategories: {e}")
        return jsonify({"error": str(e)}), 500



