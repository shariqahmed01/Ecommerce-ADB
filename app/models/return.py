from . import mongo

class Return:
    @staticmethod
    def create_return(return_data):
        return mongo.db.Return.insert_one(return_data)

    @staticmethod
    def get_returns_by_order(order_id):
        return list(mongo.db.Return.find({"orderId": order_id}))

    @staticmethod
    def update_return_status(return_id, status):
        return mongo.db.Return.update_one({"_id": return_id}, {"$set": {"status": status}})
