import pytest
import os
import sys

# 1. 환경변수 설정 (app.db import 전)
# 실제 DB 연결을 시도하지 않도록 Dummy URL 설정
os.environ.setdefault("DATABASE_URL", "sqlite:///./test_dummy.db")

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 2. Base 및 모델 Import
from app.db import Base, get_db
# ★중요★: 테이블을 생성하려면 Base가 모델들을 알고 있어야 합니다. 
# 만약 에러가 계속된다면 아래처럼 모델들을 여기서 import 해주세요.
# from app.models.deals import Deal
# from app.models.docents import Docent

# ------------------------------------------------------------------
# [수정됨] MagicMock 제거 
# Base.metadata.create_all 메서드를 Mocking 해버리면, 
# 아래에서 create_all(bind=engine)을 호출해도 아무 일도 일어나지 않습니다.
# ------------------------------------------------------------------

from app.main import app

# 3. 테스트 DB 설정 (SQLite 사용)
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
# 메모리 DB를 원하면 "sqlite:///:memory:" 사용 가능

engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL, 
    connect_args={"check_same_thread": False} 
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 테스트 시작 전 테이블 생성
# MagicMock을 지웠으므로 이제 이 코드가 정상 작동하여 'deals', 'docents' 테이블을 만듭니다.
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    
    # (선택 사항) 테스트 할 때마다 DB를 깨끗하게 비우고 싶다면 
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    
    return TestClient(app)