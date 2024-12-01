from flask import Flask
from config import get_config
from app.models import init_app as init_models
from app.routes import register_blueprints
import os

def create_app(env="development"):
    """
    Application factory to create and configure the Flask app.
    """
    app = Flask(__name__,template_folder='C:/Users/shari/Desktop/SujithADB/templates')
    app.secret_key = "your_secret_key"
    # Load configuration based on the environment
    app.config.from_object(get_config(env))

    # Initialize models (database connection)
    init_models(app)

    # Register all blueprints
    register_blueprints(app)

    return app
