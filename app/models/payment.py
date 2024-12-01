from . import mongo

class Payment:
    @staticmethod
    def create_payment(payment_data):
        return mongo.db.Payment.insert_one(payment_data)

    @staticmethod
    def get_payment_by_order(order_id):
        return mongo.db.Payment.find_one({"orderId": order_id})

    @staticmethod
    def update_payment_status(payment_id, status):
        return mongo.db.Payment.update_one({"_id": payment_id}, {"$set": {"status": status}})
