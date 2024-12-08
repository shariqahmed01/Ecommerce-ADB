from bson import ObjectId

from . import mongo

class Category:
    @staticmethod
    def get_all_categories():
        """Fetch all categories from the database."""
        categories = list(mongo.db.Category.find())
        for category in categories:
            category['_id'] = str(category['_id'])  # Convert ObjectId to string
        return categories

    @staticmethod
    def get_category_by_id(category_id):
        try:
            category_id = ObjectId(category_id)
        except Exception:
            return None
        return mongo.db.Category.find_one({"_id": category_id})


class Subcategory:
    @staticmethod
    def get_subcategories_by_category(category_id):
        try:
            category_id = ObjectId(category_id)
        except Exception:
            return []
        return list(mongo.db.Subcategory.find({"categoryId": category_id}))


    @staticmethod
    def create_subcategory(subcategory_data):
        return mongo.db.Subcategory.insert_one(subcategory_data)

    @staticmethod
    def get_all_subcategories():
        """Fetch all subcategories from the database."""
        subcategories = list(mongo.db.Subcategory.find())
        print(subcategories)
        for subcategory in subcategories:
            subcategory['_id'] = str(subcategory['_id'])  # Convert ObjectId to string
            subcategory['categoryId'] = str(subcategory['categoryId'])  # Convert ObjectId to string
        return subcategories

    @staticmethod
    def get_subcategories_by_category_id(category_id):
        """Fetch subcategories for a specific category."""
        try:
            category_id = ObjectId(category_id)  # Convert category ID to ObjectId
        except Exception:
            return []

        subcategories = list(mongo.db.Subcategory.find({"categoryId": category_id}))
        print(subcategories)
        return [
            {**subcategory, "_id": str(subcategory["_id"]), "categoryId": str(subcategory["categoryId"])}
            for subcategory in subcategories
        ]


