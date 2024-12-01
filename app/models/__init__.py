from flask_pymongo import PyMongo

# Initialize PyMongo instance
mongo = PyMongo()

def init_app(app):
    # Bind the Flask app to PyMongo
    mongo.init_app(app)


def cart():
    from flask_pymongo import PyMongo

    # Initialize PyMongo instance
    mongo = PyMongo()

    def init_app(app):
        """
        Initialize the models by associating the Flask app with the database.
        This should be called in the main app setup.
        """
        mongo.init_app(app)
