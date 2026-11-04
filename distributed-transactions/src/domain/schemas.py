from pydantic import BaseModel, Field
from uuid import UUID

class CustomerCreate(BaseModel):
    id: UUID
    name: str = Field(min_length=1, max_length=150)
    email: str = Field(min_length=3, max_length=200)

class CustomerResult(BaseModel):
    transaction_id: UUID
    customer_id: UUID
    status: str
    message: str
