from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    postgres_url: str
    mongo_url: str
    mongo_database: str = "distributed"
    sqlite_journal_path: str = "./data/transaction-journal.db"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
