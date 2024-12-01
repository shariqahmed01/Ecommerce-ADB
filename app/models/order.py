from . import mongo

class Order:
    @staticmethod
    def create_order(order_data):
        return mongo.db.Order.insert_one(order_data)

    @staticmethod
    def get_orders_by_customer(customer_id):
        return list(mongo.db.Order.find({"customerId": customer_id}))

    @staticmethod
    def get_order_by_id(order_id):
        return mongo.db.Order.find_one({"_id": order_id})

    @staticmethod
    def update_order_status(order_id, status):
        return mongo.db.Order.update_one({"_id": order_id}, {"$set": {"status": status}})
