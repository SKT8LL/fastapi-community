from dotenv import load_dotenv

# .env 로드 (로컬 개발 편의성)
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import db
from app.routers import places, events, deals, docents

# DB 초기화 (주의: 로컬 실행 시 AZURE_SQL_CONNECTIONSTRING 환경변수 필수)

# DB 초기화
# db.py에서 에러가 안 났다면 엔진 생성됨
db.Base.metadata.create_all(bind=db.engine)

# FastAPI 앱
app = FastAPI(
    title="UNMUTE API",
    description="Z세대를 위한 Indie Culture OS Backend",
    version="1.0.0"
)

# CORS (배포 시에는 더 제한적으로)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(places.router)
app.include_router(events.router)
app.include_router(deals.router)
app.include_router(docents.router)

# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}
