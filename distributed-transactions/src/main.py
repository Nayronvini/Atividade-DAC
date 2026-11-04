from fastapi import FastAPI
from src.api.routes.customers import router
from src.database.postgres import initialize_postgres
from src.database.mongo import initialize_mongo
from src.database.journal import initialize_journal

app = FastAPI(
    title="Distributed Transactions Lab",
    description="Laboratório de comparação entre 2PC, Saga e compensações",
    version="0.1.0"
)

@app.on_event("startup")
def startup():
    initialize_journal()
    initialize_postgres()
    initialize_mongo()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(router, prefix="/api")
