import pytest
import os

# app.db import 전에 환경변수 설정 (ImportError 방지)
os.environ.setdefault("AZURE_SQL_CONNECTIONSTRING", "Driver={ODBC Driver 17 for SQL Server};Server=tcp:test.database.windows.net,1433;Database=testdb;Uid=test;Pwd=test;")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base, get_db

# Mock creation of tables in production DB (since we don't have ODBC driver in test env)
from unittest.mock import MagicMock
Base.metadata.create_all = MagicMock()

from app.main import app

# 테스트 DB (in-memory SQLite, 또는 별도 테스트 Azure SQL)
# 로컬 개발 환경에서 빠르게 돌리기 위해 SQLite 사용
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    return TestClient(app)
