from fastapi import APIRouter, HTTPException, Query
from uuid import UUID
from src.domain.schemas import CustomerCreate, CustomerResult
from src.services.customer_service import CustomerService
from src.database import journal
from src.repositories.postgres_customer import PostgresCustomerRepository
from src.repositories.mongo_customer import MongoCustomerRepository

router = APIRouter(prefix="/customers", tags=["customers"])
service = CustomerService()

@router.post("/postgres-then-mongo", response_model=CustomerResult)
def create_postgres_then_mongo(
    payload: CustomerCreate,
    fail_at: str | None = Query(default=None, description="Use mongo para simular falha")
):
    if fail_at not in (None, "mongo"):
        raise HTTPException(400, "fail_at deve ser mongo")
    try:
        tx_id = service.create_postgres_then_mongo(payload.model_dump(mode="json"), fail_at)
        return CustomerResult(transaction_id=tx_id, customer_id=payload.id,
                              status="COMMITTED", message="Persistido nos dois bancos")
    except Exception as exc:
        raise HTTPException(500, str(exc)) from exc

@router.post("/mongo-then-postgres", response_model=CustomerResult)
def create_mongo_then_postgres(
    payload: CustomerCreate,
    fail_at: str | None = Query(default=None, description="Use postgres para simular falha")
):
    if fail_at not in (None, "postgres"):
        raise HTTPException(400, "fail_at deve ser postgres")
    try:
        tx_id = service.create_mongo_then_postgres(payload.model_dump(mode="json"), fail_at)
        return CustomerResult(transaction_id=tx_id, customer_id=payload.id,
                              status="COMMITTED", message="Persistido nos dois bancos")
    except Exception as exc:
        raise HTTPException(500, str(exc)) from exc

@router.get("/transactions/{transaction_id}")
def transaction_status(transaction_id: UUID):
    result = journal.get_transaction(str(transaction_id))
    if not result:
        raise HTTPException(404, "Transação não encontrada")
    return result

@router.get("/{customer_id}/debug")
def debug_customer(customer_id: UUID):
    return {
        "postgres": PostgresCustomerRepository().find(str(customer_id)),
        "mongo": MongoCustomerRepository().find(str(customer_id))
    }
