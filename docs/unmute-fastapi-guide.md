# UNMUTE FastAPI 기본 구조

## 1. 프로젝트 디렉토리 구조
```
unmute-api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 앱
│   ├── config.py            # 설정 (환경변수)
│   ├── database.py          # PostgreSQL 연결
│   ├── models.py            # Pydantic 모델
│   ├── routers/
│   │   ├── search.py        # GET /api/v1/search (하이브리드 검색)
│   │   ├── ingest.py        # POST /api/v1/ingest/* (Blob 업로드)
│   │   ├── order.py         # POST /api/v1/orders (주문 관리)
│   │   └── health.py        # GET /health
│   ├── services/
│   │   ├── search_service.py    # Azure AI Search
│   │   ├── rag_service.py       # OpenAI RAG
│   │   ├── ingest_service.py    # Blob 업로드
│   │   └── order_service.py     # 주문/재고
│   └── utils/
│       ├── logging.py       # App Insights 로깅
│       └── errors.py        # 커스텀 예외
├── requirements.txt         # 의존성
├── .env.example            # 환경변수 예제
├── Dockerfile
└── docker-compose.yml
```

## 2. 필수 라이브러리 (requirements.txt)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
pydantic==2.5.0
pydantic-settings==2.1.0
azure-search-documents==11.4.0
azure-storage-blob==12.19.0
openai==1.6.1
python-dotenv==1.0.0
aiohttp==3.9.1
```

## 3. 환경변수 (.env)
```
ENVIRONMENT=development
DATABASE_URL=postgresql+psycopg2://unmute_admin:PASSWORD@HOST:5432/unmute_db
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointProtocol=...
SEARCH_SERVICE_ENDPOINT=https://unmute-search-dev-xxx.search.windows.net
SEARCH_SERVICE_ADMIN_KEY=YOUR_SEARCH_KEY
OPENAI_API_KEY=sk-YOUR_KEY
APPINSIGHTS_INSTRUMENTATIONKEY=YOUR_KEY
```

## 4. app/main.py - FastAPI 앱
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import search, ingest, order, health

app = FastAPI(title="UNMUTE API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(search.router, prefix="/api/v1")
app.include_router(ingest.router, prefix="/api/v1")
app.include_router(order.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 5. app/config.py - 설정
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DATABASE_URL: str
    SEARCH_SERVICE_ENDPOINT: str
    SEARCH_SERVICE_ADMIN_KEY: str
    AZURE_STORAGE_CONNECTION_STRING: str
    OPENAI_API_KEY: str
    APPINSIGHTS_INSTRUMENTATIONKEY: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## 6. app/routers/search.py - 검색 (하이브리드)
```python
from fastapi import APIRouter, Query
from app.services.search_service import HybridSearchService

router = APIRouter()
search_svc = HybridSearchService()

@router.get("/search")
async def search(
    q: str = Query(..., description="검색어"),
    lat: float = Query(None),
    lng: float = Query(None),
    radius: float = Query(5),
    limit: int = Query(10),
):
    """
    하이브리드 검색: 키워드 + 벡터 (Azure AI Search)
    + 거리 필터
    """
    results = await search_svc.hybrid_search(
        query=q,
        lat=lat,
        lng=lng,
        radius=radius,
        limit=limit
    )
    return {"results": results, "count": len(results)}

@router.post("/rag/docent")
async def generate_docent(place_id: int):
    """
    RAG로 감성적 설명(도슨트) 생성
    """
    from app.services.rag_service import RagService
    rag_svc = RagService()
    docent = await rag_svc.generate_docent(place_id)
    return {"docent": docent}
```

## 7. app/routers/ingest.py - 업로드
```python
from fastapi import APIRouter, File, UploadFile, Form
from app.services.ingest_service import IngestService

router = APIRouter()
ingest_svc = IngestService()

@router.post("/ingest/poster")
async def upload_poster(
    file: UploadFile = File(...),
    place_id: int = Form(None),
    event_id: int = Form(None),
):
    """
    포스터 이미지 업로드 → Blob → AI Search 인덱싱(OCR)
    """
    result = await ingest_svc.upload_poster(
        file=file,
        place_id=place_id,
        event_id=event_id
    )
    return result

@router.post("/ingest/text")
async def upload_description(
    place_id: int = Form(...),
    text: str = Form(...),
):
    """
    운영자 설명 텍스트 업로드
    """
    result = await ingest_svc.upload_text(place_id, text)
    return result
```

## 8. app/routers/order.py - 주문/재고
```python
from fastapi import APIRouter
from app.services.order_service import OrderService

router = APIRouter()
order_svc = OrderService()

@router.post("/orders")
async def create_order(event_id: int, quantity: int, user_id: int):
    """
    주문 생성 (재고 수량 기반)
    """
    result = await order_svc.create_order(event_id, quantity, user_id)
    return result

@router.get("/orders/{order_id}")
async def get_order(order_id: int):
    """주문 조회"""
    return await order_svc.get_order(order_id)

@router.delete("/orders/{order_id}")
async def cancel_order(order_id: int):
    """주문 취소"""
    await order_svc.cancel_order(order_id)
    return {"status": "cancelled"}
```

## 9. app/services/search_service.py - Azure AI Search
```python
from azure.search.documents import SearchClient
from app.config import settings

class HybridSearchService:
    def __init__(self):
        self.client = SearchClient(
            endpoint=settings.SEARCH_SERVICE_ENDPOINT,
            index_name="unmute-index",
            credential=settings.SEARCH_SERVICE_ADMIN_KEY
        )
    
    async def hybrid_search(self, query, lat=None, lng=None, radius=5, limit=10):
        """
        1. 키워드 검색 (BM25)
        2. 벡터 검색 (임베딩)
        3. 결과 병합
        4. 거리 필터링
        """
        # Azure AI Search 쿼리
        results = self.client.search(
            search_text=query,
            top=limit,
            select=["id", "title", "description", "location", "tags"]
        )
        
        # 거리 필터링 (위도/경도가 있을 경우)
        if lat and lng:
            results = [r for r in results 
                      if self._calculate_distance(lat, lng, r) <= radius]
        
        return list(results)
    
    def _calculate_distance(self, lat1, lng1, result):
        """두 지점 사이 거리 계산 (하버사인 공식)"""
        # 간단한 근사값 계산
        import math
        lat2, lng2 = result.get('location', [0, 0])
        
        R = 6371  # 지구 반지름 (km)
        dlat = math.radians(lat2 - lat1)
        dlng = math.radians(lng2 - lng1)
        
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * \
            math.cos(math.radians(lat2)) * math.sin(dlng/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        
        return R * c
```

## 10. app/services/rag_service.py - OpenAI RAG
```python
from openai import OpenAI
from app.config import settings

class RagService:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_docent(self, place_id):
        """
        검색 결과를 바탕으로 도슨트(감성적 설명) 생성
        """
        # 1. Place 정보 조회 (DB에서)
        # 2. 검색으로 관련 청크 확보
        # 3. OpenAI로 답변 생성
        
        prompt = f"""
        장소 ID: {place_id}
        
        위의 정보를 바탕으로 따뜻하고 감성적인 도슨트를 한국어로 작성하세요.
        (100-150 단어)
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "당신은 UNMUTE의 AI 도슨트입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
```

## 11. app/services/ingest_service.py - Blob 업로드
```python
from azure.storage.blob import BlobClient
from app.config import settings

class IngestService:
    async def upload_poster(self, file, place_id=None, event_id=None):
        """
        포스터 이미지 Blob에 업로드
        """
        blob_name = f"raw-instagram/{place_id or event_id}_{file.filename}"
        
        blob_client = BlobClient.from_connection_string(
            conn_str=settings.AZURE_STORAGE_CONNECTION_STRING,
            container_name="raw-instagram",
            blob_name=blob_name
        )
        
        # 파일 업로드
        data = await file.read()
        blob_client.upload_blob(data, overwrite=True)
        
        # AI Search 인덱서 트리거 (선택)
        # await self.trigger_indexer()
        
        return {"blob_url": blob_client.url, "status": "uploaded"}
    
    async def upload_text(self, place_id, text):
        """
        텍스트 메타데이터 업로드
        """
        blob_name = f"raw-operator/place_{place_id}.txt"
        
        blob_client = BlobClient.from_connection_string(
            conn_str=settings.AZURE_STORAGE_CONNECTION_STRING,
            container_name="raw-operator",
            blob_name=blob_name
        )
        
        blob_client.upload_blob(text.encode('utf-8'), overwrite=True)
        
        return {"blob_url": blob_client.url, "status": "uploaded"}
```

## 12. app/services/order_service.py - 주문/재고
```python
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import Session
from app.config import settings
from datetime import datetime, timedelta

# 간단한 Order 모델
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    user_id = Column(Integer)
    quantity = Column(Integer)
    status = Column(String, default="pending")  # pending, confirmed, cancelled, expired
    expires_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class OrderService:
    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URL)
        Base.metadata.create_all(self.engine)
    
    async def create_order(self, event_id, quantity, user_id):
        """
        주문 생성
        - 재고 확인
        - Order 생성 (pending)
        - 만료 시간 설정
        """
        session = Session(self.engine)
        
        # 재고 확인 (간단한 버전)
        order = Order(
            event_id=event_id,
            user_id=user_id,
            quantity=quantity,
            status="pending",
            expires_at=datetime.utcnow() + timedelta(minutes=30)
        )
        
        session.add(order)
        session.commit()
        
        return {"order_id": order.id, "status": "pending"}
    
    async def cancel_order(self, order_id):
        """주문 취소"""
        session = Session(self.engine)
        order = session.query(Order).filter(Order.id == order_id).first()
        if order:
            order.status = "cancelled"
            session.commit()
```

## 13. 로컬 실행
```bash
# 환경 설정
cp .env.example .env
# .env 파일 수정 (실제 키 입력)

# 의존성 설치
pip install -r requirements.txt

# FastAPI 실행
python -m uvicorn app.main:app --reload

# 테스트
curl http://localhost:8000/health
curl "http://localhost:8000/api/v1/search?q=jazz"
```

## 14. PostgreSQL 스키마
```sql
CREATE TABLE places (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    location POINT,
    tags TEXT[],
    genre TEXT[],
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE events (
    id SERIAL PRIMARY KEY,
    place_id INT REFERENCES places(id),
    title VARCHAR(255),
    event_date TIMESTAMP,
    inventory_remaining INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    event_id INT REFERENCES events(id),
    user_id INT,
    quantity INT,
    status VARCHAR(50) DEFAULT 'pending',
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    place_id INT REFERENCES places(id),
    event_id INT REFERENCES events(id),
    blob_path VARCHAR(500),
    ocr_text TEXT,
    language VARCHAR(10) DEFAULT 'ko',
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

**이제 바로 시작할 수 있는 기본 구조입니다. 각 파일을 만들고 요구사항에 맞게 확장하세요!**
