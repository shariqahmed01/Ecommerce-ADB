from bson import ObjectId

from . import mongo

class Category:
    @staticmethod
    def get_all_categories():
        return list(mongo.db.Category.find())

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
        """Fetch all subcategories."""
        subcategories = list(mongo.db.Subcategory.find())
        for subcategory in subcategories:
            subcategory["_id"] = str(subcategory["_id"])
            subcategory["categoryId"] = str(subcategory["categoryId"])
        return subcategories
