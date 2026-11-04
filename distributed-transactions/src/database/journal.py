import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from src.core.config import settings

def _connect():
    path = Path(settings.sqlite_journal_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path, timeout=10)
    connection.row_factory = sqlite3.Row
    return connection

def initialize_journal():
    with _connect() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS saga_transactions (
                id TEXT PRIMARY KEY, entity_id TEXT NOT NULL,
                operation TEXT NOT NULL, status TEXT NOT NULL,
                completed_step TEXT, error_message TEXT,
                created_at TEXT NOT NULL, updated_at TEXT NOT NULL
            )
        """)

def create_transaction(transaction_id, entity_id, operation):
    now = datetime.now(timezone.utc).isoformat()
    with _connect() as connection:
        connection.execute("""
            INSERT INTO saga_transactions
            (id, entity_id, operation, status, created_at, updated_at)
            VALUES (?, ?, ?, 'STARTED', ?, ?)
        """, (transaction_id, entity_id, operation, now, now))

def update_transaction(transaction_id, status, completed_step=None, error_message=None):
    now = datetime.now(timezone.utc).isoformat()
    with _connect() as connection:
        connection.execute("""
            UPDATE saga_transactions
            SET status=?, completed_step=COALESCE(?, completed_step),
                error_message=?, updated_at=? WHERE id=?
        """, (status, completed_step, error_message, now, transaction_id))

def get_transaction(transaction_id):
    with _connect() as connection:
        row = connection.execute(
            "SELECT * FROM saga_transactions WHERE id=?", (transaction_id,)
        ).fetchone()
        return dict(row) if row else None

def list_incomplete():
    with _connect() as connection:
        rows = connection.execute("""
            SELECT * FROM saga_transactions
            WHERE status NOT IN ('COMMITTED', 'COMPENSATED')
            ORDER BY created_at
        """).fetchall()
        return [dict(row) for row in rows]
