import json
import logging
import subprocess  # nosec
import time
from contextlib import contextmanager
from datetime import datetime, timedelta
from typing import Generator, Optional

from sqlalchemy import create_engine
from sqlalchemy.exc import DatabaseError, SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


class DBConfigSQLAlchemy:
    """Database configuration and management using SQLAlchemy with Azure Managed Identity authentication."""

    Base = declarative_base()

    def __init__(self, db_username: str, db_hostname: str, db_name: str, client_id: str) -> None:
        """
        Initializes the database configuration.

        Parameters
        ----------
        db_username : str
            The database username.
        db_hostname : str
            The database hostname.
        db_name : str
            The database name.
        client_id : str
            The Azure Managed Identity client ID.
        """
        self.engine: Optional[Engine] = None
        self.session_maker: Optional[sessionmaker] = None
        self.db_username: str = db_username
        self.db_hostname: str = db_hostname
        self.db_name: str = db_name
        self.client_id: str = client_id
        self.access_token: Optional[str] = None
        self.token_expiration_time: Optional[datetime] = None
        self.token_renewal_margin: timedelta = timedelta(minutes=5)
        self.retry_count: int = 3
        self.retry_delay: int = 5  # seconds between retries

    def _run_az_cli(self, command: list[str]) -> dict:
        """
        Runs an Azure CLI command and returns the output as a JSON object.

        Parameters
        ----------
        command : list[str]
            The Azure CLI command as a list of arguments.

        Returns
        -------
        dict
            The parsed JSON output from the command.

        Raises
        ------
        subprocess.CalledProcessError
            If the Azure CLI command fails.
        """
        try:
            result = subprocess.run(
                command, capture_output=True, check=True, text=True  # nosec
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.exception(f"Azure CLI command failed: {e}")
            raise

    def _get_db_access_token(self) -> None:
        """
        Retrieves and sets the database access token using Azure Managed Identity.

        Raises
        ------
        ValueError
            If the access token or expiration time cannot be retrieved.
        """
        self._run_az_cli(["az", "login", "--identity", "--client-id", self.client_id])

        token_info = self._run_az_cli(
            ["az", "account", "get-access-token", "--resource-type", "oss-rdbms"]
        )

        self.access_token = token_info.get("accessToken")
        expires_on_str = token_info.get("expiresOn")

        if not self.access_token or not expires_on_str:
            raise ValueError("Failed to retrieve access token from Azure CLI.")

        self.token_expiration_time = (
            datetime.fromisoformat(expires_on_str) - self.token_renewal_margin
        )
        logger.info("Database access token retrieved successfully.")

    def _get_db_connection_string(self) -> str:
        """
        Generates the PostgreSQL connection string with the current access token.

        Returns
        -------
        str
            The database connection string.
        """
        if not self.access_token or datetime.now() >= self.token_expiration_time:
            self._get_db_access_token()

        return f"postgresql+psycopg2://{self.db_username}:{self.access_token}@{self.db_hostname}/{self.db_name}"

    def create_connection(self) -> None:
        """
        Initializes the database connection and session maker.

        Raises
        ------
        SQLAlchemyError
            If an error occurs while creating the database engine.
        """
        try:
            db_url = self._get_db_connection_string()
            self.engine = create_engine(db_url, pool_pre_ping=True)
            self.session_maker = sessionmaker(
                bind=self.engine, autoflush=False, autocommit=False
            )
            logger.info("Successfully created database sessionmaker.")
        except SQLAlchemyError:
            logger.exception("Error creating database sessionmaker.")
            raise

    @contextmanager
    def managed_session(self) -> Generator[Session, None, None]:
        """
        Provides a database session with automatic rollback and retries.

        Yields
        ------
        Session
            A SQLAlchemy session.

        Raises
        ------
        DatabaseError
            If database connection issues persist after retries.
        SQLAlchemyError
            If a general SQLAlchemy error occurs.
        """
        for attempt in range(self.retry_count):
            self._validate_token_status()
            if not self.session_maker:
                raise RuntimeError("SessionMaker has not been created. Call create_connection() first.")

            session = self.session_maker()

            try:
                yield session
                session.commit()
                return  # Exit if successful
            except SQLAlchemyError:
                session.rollback()
                logger.exception("Database error encountered, rolling back changes.")
            except DatabaseError as e:
                logger.error(
                    f"Database connection error. Retrying in {self.retry_delay} seconds..."
                )
                time.sleep(self.retry_delay)
                if attempt == self.retry_count - 1:
                    raise e
            finally:
                session.close()

    def close_connection(self) -> None:
        """
        Closes the database engine connection.

        Raises
        ------
        SQLAlchemyError
            If an error occurs while disposing of the database engine.
        """
        if self.engine:
            try:
                self.engine.dispose()
                logger.info("Database connection successfully closed.")
            except SQLAlchemyError:
                logger.exception("Error disposing the database engine.")
                raise

    def _validate_token_status(self) -> None:
        """
        Checks and renews the access token if needed.
        """
        if not self.token_expiration_time or datetime.now() >= self.token_expiration_time:
            self._get_db_access_token()
            logger.info("Database access token renewed.")
