import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application Configuration."""
    # Defaul to sqlite for ease of demo if not provided, but spec says postgres.
    # We will assume user provides a connection string or we warn.
    # Storage Config
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/eo_lib_db")
    STORAGE_TYPE = os.getenv("STORAGE_TYPE", "db") # Options: db, memory, json
    JSON_DATA_DIR = os.getenv("JSON_DATA_DIR", "/tmp/eo_lib_data")

    @classmethod
    def get_database_url(cls) -> str:
        return cls.DATABASE_URL
        
    @classmethod
    def get_storage_type(cls) -> str:
        return cls.STORAGE_TYPE

    @classmethod
    def get_json_dir(cls) -> str:
        return cls.JSON_DATA_DIR
