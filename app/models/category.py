from . import mongo

class Category:
    @staticmethod
    def get_all_categories():
        return list(mongo.db.Category.find())

    @staticmethod
    def create_category(category_data):
        return mongo.db.Category.insert_one(category_data)


class Subcategory:
    @staticmethod
    def get_subcategories_by_category(category_id):
        return list(mongo.db.Subcategory.find({"categoryId": category_id}))

    @staticmethod
    def create_subcategory(subcategory_data):
        return mongo.db.Subcategory.insert_one(subcategory_data)
