from flask import Blueprint
from .auth import auth_bp
from .contact import contact_bp
from .product import product_bp
from .cart import cart_bp
from .order import order_bp
from .review import review_bp
from .delivery import delivery_bp
from .admin import admin_bp
from .home import home_bp  # Import the home blueprint

def register_blueprints(app):
    """Register all blueprints with the Flask app."""
    app.register_blueprint(home_bp)  # Register the home blueprint
    app.register_blueprint(auth_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(delivery_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(contact_bp)
