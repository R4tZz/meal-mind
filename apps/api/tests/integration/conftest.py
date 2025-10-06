import pytest
from sqlalchemy import inspect


@pytest.fixture
def db_inspector(db_session):
    """Provide database inspector for integration tests."""
    return inspect(db_session.bind)
