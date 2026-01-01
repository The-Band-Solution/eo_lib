from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session, scoped_session
from eo_lib.config import Config
from eo_lib.domain.base import Base


class PostgresClient:
    """
    Singleton Database Client for PostgreSQL.

    Manages the SQLAlchemy Engine and SessionFactory (SessionLocal) to provide
    thread-safe database access throughout the application.
    """

    _instance = None
    _engine = None
    _SessionLocal = None

    def __new__(cls):
        """
        Ensures only one instance of PostgresClient exists.

        Returns:
            PostgresClient: The singleton instance.
        """
        if cls._instance is None:
            cls._instance = super(PostgresClient, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        """
        Initializes the SQLAlchemy engine and session factory.
        Uses configuration from the Config class.
        """
        db_url = Config.get_database_url()
        self._engine = create_engine(db_url, echo=False)
        self._SessionLocal = scoped_session(sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine, expire_on_commit=False
        ))

    def get_session(self) -> Session:
        """
        Creates and returns a new SQLAlchemy Session.

        Returns:
            Session: A new database session instance.
        """
        if not self._SessionLocal:
            self._initialize()
        assert self._SessionLocal is not None
        return self._SessionLocal()

    def create_tables(self):
        """
        Utility method to create all database tables defined in the ORM models.
        Useful for development and testing environments.
        """
        # Import models here to ensure they are registered with Base
        # We need to define the ORM model for User before calling this
        pass
