import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Application-wide configuration management.
    
    Loads settings from environment variables and provides a centralized
    access point for database URLs, storage strategies, and file paths.
    """
    # Default to sqlite for ease of demo if not provided, but spec says postgres.
    # We will assume user provides a connection string or we warn.
    # Storage Config
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost:5432/eo_lib_db")
    STORAGE_TYPE = os.getenv("STORAGE_TYPE", "db") # Options: db, memory, json
    JSON_DATA_DIR = os.getenv("JSON_DATA_DIR", "/tmp/eo_lib_data")

    @classmethod
    def get_database_url(cls) -> str:
        """
        Returns the configured PostgreSQL database URL.
        
        Returns:
            str: Connection string.
        """
        return cls.DATABASE_URL
        
    @classmethod
    def get_storage_type(cls) -> str:
        """
        Returns the configured storage strategy (db, memory, json).
        
        Returns:
            str: The storage type identifier.
        """
        return cls.STORAGE_TYPE

    @classmethod
    def get_json_dir(cls) -> str:
        """
        Returns the directory path for JSON storage.
        
        Returns:
            str: Path to the JSON data directory.
        """
        return cls.JSON_DATA_DIR
