from . import mongo

class Employee:
    @staticmethod
    def create_employee(employee_data):
        return mongo.db.Employee.insert_one(employee_data)

    @staticmethod
    def get_employee_by_username(username):
        return mongo.db.Employee.find_one({"username": username})

    @staticmethod
    def update_employee(employee_id, updated_data):
        return mongo.db.Employee.update_one({"_id": employee_id}, {"$set": updated_data})
