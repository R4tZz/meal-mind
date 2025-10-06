"""
Pytest configuration and fixtures
"""

import os
import sys
from pathlib import Path
import pytest
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine.url import make_url
from alembic.config import Config
from alembic import command

# Add parent directory to Python path
api_dir = Path(__file__).parent.parent
sys.path.insert(0, str(api_dir))

# Load .env file from api directory
env_path = api_dir / ".env"
load_dotenv(dotenv_path=env_path)

# Get DATABASE_URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL environment variable must be set for tests.")

# Parse DATABASE_URL to extract connection components
db_url = make_url(DATABASE_URL)
POSTGRES_USER = db_url.username or "postgres"
POSTGRES_PASSWORD = db_url.password or "postgres"
POSTGRES_HOST = db_url.host or "localhost"
POSTGRES_PORT = str(db_url.port or 54322)

# Test database configuration
TEST_DB_NAME = os.getenv("TEST_DB_NAME", "mealmind_test")

# Connection strings
ADMIN_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/postgres"
TEST_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{TEST_DB_NAME}"


def _database_exists(engine, db_name: str) -> bool:
    """Check if a database exists."""
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT 1 FROM pg_database WHERE datname=:name"),
            {"name": db_name},
        )
        return result.fetchone() is not None


def _create_database(admin_engine, db_name: str) -> None:
    """Create a new database."""
    with admin_engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        conn.execute(text(f'CREATE DATABASE "{db_name}"'))
        print(f"Created test database '{db_name}'.")


def _run_migrations(database_url: str) -> None:
    """Run Alembic migrations on the specified database."""
    alembic_ini_path = api_dir / "alembic.ini"
    alembic_cfg = Config(str(alembic_ini_path))
    alembic_cfg.set_main_option("sqlalchemy.url", database_url)
    command.upgrade(alembic_cfg, "head")
    print("Alembic migrations applied.")


@pytest.fixture(scope="session")
def setup_test_database():
    """
    Session-scoped fixture to ensure test database exists and is migrated.

    This runs ONCE per test session (not per test).
    - Loads configuration from .env file
    - Checks if mealmind_test database exists
    - Creates it if missing
    - Runs Alembic migrations to set up schema

    The autouse=True means it runs automatically before any tests.
    """
    print("\n🔧 Setting up test database...")
    print(f"Database server: {POSTGRES_HOST}:{POSTGRES_PORT}")

    # Connect to PostgreSQL server (not a specific database)
    admin_engine = create_engine(ADMIN_DATABASE_URL, isolation_level="AUTOCOMMIT")

    # Check if test database exists
    if not _database_exists(admin_engine, TEST_DB_NAME):
        print(f"Test database '{TEST_DB_NAME}' does not exist, creating...")
        _create_database(admin_engine, TEST_DB_NAME)
    else:
        print(f"Test database '{TEST_DB_NAME}' already exists")

    # Run migrations to ensure schema is up to date
    print(f"Running Alembic migrations on '{TEST_DB_NAME}'...")
    _run_migrations(TEST_DATABASE_URL)

    admin_engine.dispose()
    print("Test database ready!\n")


@pytest.fixture(scope="function")
def db_session(setup_test_database):
    """
    Provide a database session with automatic transaction rollback.

    Each test gets a fresh session within a transaction.
    After the test completes (pass or fail), the transaction is rolled back,
    ensuring the database is clean for the next test.

    This pattern is MUCH faster than recreating the database between tests
    while maintaining perfect test isolation.

    Usage:
        def test_create_recipe(db_session):
            recipe = Recipe(name="Pasta")
            db_session.add(recipe)
            db_session.commit()
            # After test: automatic rollback, recipe disappears
    """
    # Create engine for test database
    engine = create_engine(TEST_DATABASE_URL)

    # Create a connection
    connection = engine.connect()

    # Begin a transaction
    transaction = connection.begin()

    # Create a session bound to this connection and transaction
    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()

    # Provide the session to the test
    yield session

    # After test completes, cleanup:
    session.close()  # Close the session

    # Only rollback if transaction is still active
    if transaction.is_active:
        transaction.rollback()  # Rollback all changes

    connection.close()  # Close the connection
    engine.dispose()  # Dispose the engine
