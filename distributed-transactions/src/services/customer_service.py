from src.repositories.postgres_customer import PostgresCustomerRepository
from src.repositories.mongo_customer import MongoCustomerRepository
from src.services.saga_coordinator import SagaCoordinator

class CustomerService:
    def __init__(self):
        self.pg = PostgresCustomerRepository()
        self.mongo = MongoCustomerRepository()
        self.coordinator = SagaCoordinator()

    def create_postgres_then_mongo(self, customer, fail_at=None):
        customer_id = str(customer["id"])
        tx_id = self.coordinator.start(customer_id, "CREATE_PG_THEN_MONGO")
        pg_inserted = False
        try:
            self.pg.insert(customer, tx_id)
            pg_inserted = True
            self.coordinator.step_completed(tx_id, "POSTGRES")
            if fail_at == "mongo":
                raise RuntimeError("Falha simulada antes da escrita no MongoDB")
            self.mongo.insert(customer, tx_id)
            self.coordinator.step_completed(tx_id, "MONGO")
            self.coordinator.committed(tx_id)
            return tx_id
        except Exception as exc:
            self.coordinator.compensating(tx_id, str(exc))
            try:
                if pg_inserted:
                    self.pg.delete_if_owned_by_operation(customer_id, tx_id)
                self.coordinator.compensated(tx_id)
            except Exception as compensation_error:
                self.coordinator.compensation_failed(tx_id, str(compensation_error))
                raise RuntimeError(
                    f"Falha: {exc}; compensação pendente: {compensation_error}; tx={tx_id}"
                ) from compensation_error
            raise RuntimeError(
                f"Operação compensada: {exc}; transaction_id={tx_id}"
            ) from exc

    def create_mongo_then_postgres(self, customer, fail_at=None):
        customer_id = str(customer["id"])
        tx_id = self.coordinator.start(customer_id, "CREATE_MONGO_THEN_PG")
        mongo_inserted = False
        try:
            self.mongo.insert(customer, tx_id)
            mongo_inserted = True
            self.coordinator.step_completed(tx_id, "MONGO")
            if fail_at == "postgres":
                raise RuntimeError("Falha simulada antes da escrita no PostgreSQL")
            self.pg.insert(customer, tx_id)
            self.coordinator.step_completed(tx_id, "POSTGRES")
            self.coordinator.committed(tx_id)
            return tx_id
        except Exception as exc:
            self.coordinator.compensating(tx_id, str(exc))
            try:
                if mongo_inserted:
                    self.mongo.delete_if_owned_by_operation(customer_id, tx_id)
                self.coordinator.compensated(tx_id)
            except Exception as compensation_error:
                self.coordinator.compensation_failed(tx_id, str(compensation_error))
                raise RuntimeError(
                    f"Falha: {exc}; compensação pendente: {compensation_error}; tx={tx_id}"
                ) from compensation_error
            raise RuntimeError(
                f"Operação compensada: {exc}; transaction_id={tx_id}"
            ) from exc
