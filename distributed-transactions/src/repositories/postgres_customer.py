from sqlalchemy import text
from src.database.postgres import engine

class PostgresCustomerRepository:
    def insert(self, customer, operation_id):
        with engine.begin() as connection:
            connection.execute(text("""
                INSERT INTO customers (id, name, email, version, operation_id)
                VALUES (:id, :name, :email, 1, :operation_id)
            """), {
                "id": str(customer["id"]), "name": customer["name"],
                "email": customer["email"], "operation_id": operation_id
            })

    def delete_if_owned_by_operation(self, customer_id, operation_id):
        with engine.begin() as connection:
            connection.execute(text("""
                DELETE FROM customers WHERE id=:id AND operation_id=:operation_id
            """), {"id": customer_id, "operation_id": operation_id})

    def find(self, customer_id):
        with engine.connect() as connection:
            row = connection.execute(text("""
                SELECT id, name, email, version, operation_id
                FROM customers WHERE id=:id
            """), {"id": customer_id}).mappings().first()
            return dict(row) if row else None
