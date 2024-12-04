from . import mongo

class Admin:
    @staticmethod
    def create_admin(admin_data):
        return mongo.db.Admin.insert_one(admin_data)

    @staticmethod
    def get_admin_by_username(username):
        return mongo.db.Admin.find_one({"username": username})

    @staticmethod
    def get_admin_by_email(email):
        """Fetch an admin user by their email."""
        return mongo.db.Admin.find_one({"email": email})


