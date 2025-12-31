from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from eo_lib.config import Config
from eo_lib.domain.base import Base

class PostgresClient:
    """
    Singleton Database Client.
    Manages the SQLAlchemy Engine and SessionFactory.
    """
    _instance = None
    _engine = None
    _SessionLocal = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PostgresClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        db_url = Config.get_database_url()
        self._engine = create_engine(db_url, echo=False)
        self._SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self._engine, expire_on_commit=False)

    def get_session(self) -> Session:
        """Factory method to get a new DB session."""
        if not self._SessionLocal:
            self._initialize()
        return self._SessionLocal()

    def create_tables(self):
        """Helper to init tables (useful for dev/test)."""
        # Import models here to ensure they are registered with Base
        # We need to define the ORM model for User before calling this
        pass 
