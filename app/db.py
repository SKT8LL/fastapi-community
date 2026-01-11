from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from typing import Generator

# DATABASE_URL 환경변수 사용 (Azure App Service Bicep 배포 시 DATABASE_URL로 주입됨)
# 또는 로컬에서 AZURE_SQL_CONNECTIONSTRING 대신 DATABASE_URL 사용 권장
database_url = os.getenv("DATABASE_URL")

if not database_url:
    # 하위 호환성: 기존 AZURE_SQL_CONNECTIONSTRING이 있으면 시도 (단, 포맷이 다를 수 있음)
    # Bicep 배포 후에는 DATABASE_URL을 사용하므로, 여기서는 DATABASE_URL을 우선으로 함.
    odbc_str = os.getenv("AZURE_SQL_CONNECTIONSTRING")
    if odbc_str:
        # 기존 MSSQL/ODBC 로직 유지 (혹시 모를 롤백 대비) 또는 에러 발생
        # 여기서는 PostgreSQL로 전환하므로 DATABASE_URL 없으면 에러 혹은 SQLite(개발용) Fallback 고려
        # 하지만 프롬프트 원칙상 환경변수 필수.
        raise ValueError("DATABASE_URL (or AZURE_SQL_CONNECTIONSTRING) environment variable not set")
    raise ValueError("DATABASE_URL environment variable not set")

# PostgreSQL 연결 (DATABASE_URL이 postgresql:// 형태로 들어온다고 가정)
connection_string = database_url
engine = create_engine(connection_string, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator:
    """FastAPI 의존성: DB 세션 반환"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
