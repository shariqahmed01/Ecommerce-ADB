from . import mongo

class Delivery:
    @staticmethod
    def create_delivery(delivery_data):
        return mongo.db.Delivery.insert_one(delivery_data)

    @staticmethod
    def get_delivery_by_tracking(tracking_number):
        return mongo.db.Delivery.find_one({"trackingNumber": tracking_number})

    @staticmethod
    def update_delivery_status(tracking_number, status):
        return mongo.db.Delivery.update_one({"trackingNumber": tracking_number}, {"$set": {"status": status}})
