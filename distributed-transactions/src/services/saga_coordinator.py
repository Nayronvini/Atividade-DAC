from uuid import uuid4
from src.database import journal

class SagaCoordinator:
    def start(self, entity_id, operation):
        transaction_id = str(uuid4())
        journal.create_transaction(transaction_id, entity_id, operation)
        return transaction_id

    def step_completed(self, transaction_id, step):
        journal.update_transaction(transaction_id, f"{step}_APPLIED", step)

    def committed(self, transaction_id):
        journal.update_transaction(transaction_id, "COMMITTED")

    def compensating(self, transaction_id, error):
        journal.update_transaction(transaction_id, "COMPENSATING", error_message=error)

    def compensated(self, transaction_id):
        journal.update_transaction(transaction_id, "COMPENSATED")

    def compensation_failed(self, transaction_id, error):
        journal.update_transaction(transaction_id, "COMPENSATION_REQUIRED",
                                   error_message=error)
