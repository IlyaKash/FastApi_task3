import pytest
from sqlalchemy.orm import sessionmaker
from models.good import Base
from public.db import engine_s

@pytest.fixture(scope="session")
def test_db():
    engine = engine_s
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def session(test_db):
    Session = sessionmaker(bind=test_db)
    session = Session()
    try:
        yield session
    finally:
        session.close()