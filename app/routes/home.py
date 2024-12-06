from flask import Blueprint, render_template
from app.models.product import Product

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def index():
    # Fetch featured products from the database
    trending_products = Product.get_trending_products(limit=4)
    return render_template('index.html', trending_products=trending_products)
