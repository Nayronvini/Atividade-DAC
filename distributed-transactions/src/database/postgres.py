from sqlalchemy import create_engine, text
from src.core.config import settings

engine = create_engine(settings.postgres_url, pool_pre_ping=True, future=True)

def initialize_postgres():
    with engine.begin() as connection:
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS customers (
                id UUID PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                email VARCHAR(200) NOT NULL,
                version BIGINT NOT NULL DEFAULT 1,
                operation_id UUID NOT NULL,
                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
            )
        """))
        connection.execute(text("""
            CREATE INDEX IF NOT EXISTS ix_customers_operation_id
            ON customers(operation_id)
        """))
