from . import mongo
from bson.objectid import ObjectId

class User:
    @staticmethod
    def get_user_by_email(email):
        """Fetch a user by email."""
        return mongo.db.User.find_one({"email": email})

    @staticmethod
    def create_user(user_data):
        """Insert a new user into the database."""
        return mongo.db.User.insert_one(user_data)

    @staticmethod
    def get_user_by_id(user_id):
        """Fetch a user by ID."""
        try:
            user_id = ObjectId(user_id)
        except Exception:
            return None
        return mongo.db.User.find_one({"_id": user_id})
