from src.database.mongo import customers

class MongoCustomerRepository:
    def insert(self, customer, operation_id):
        customers.insert_one({
            "_id": str(customer["id"]), "name": customer["name"],
            "email": customer["email"], "version": 1,
            "operation_id": operation_id
        })

    def delete_if_owned_by_operation(self, customer_id, operation_id):
        customers.delete_one({"_id": customer_id, "operation_id": operation_id})

    def find(self, customer_id):
        return customers.find_one({"_id": customer_id}, {"_id": 0})
