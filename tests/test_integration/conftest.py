import pytest
from sqlalchemy.orm import Session

from models.database import engine


@pytest.fixture
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind = connection)
    yield session
    # test logic
    session.close()
    transaction.rollback()
    connection.close()
