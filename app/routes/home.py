from flask import Blueprint, render_template
from app.models.product import Product

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    # Fetch featured products from the database
    featured_products = Product.get_featured_products()
    return render_template('index.html', featured_products=featured_products)
