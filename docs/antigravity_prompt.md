# Antigravity Prompt: FastAPI + Azure SQL + OIDC 스캐폴딩 생성

이 프롬프트는 `SKT8LL/fastapi-community` 레포지토리에 커밋할 **초보자용 FastAPI 스캐폴딩**을 생성합니다. 복붙하여 Antigravity에 입력하세요.

---

```
당신은 GitHub 레포 "SKT8LL/fastapi-community"에 커밋할 FastAPI 스캐폴딩을 생성하는 에이전트입니다.

【 목표 】
초보자 2명이 UNMUTE(Z세대 인디 문화 OS) 서비스의 API를 분리 구현하면서,
CRUD / Swagger 문서 / Git 협업(PR) / CI/CD 자동 배포(Azure App Service + OIDC)를 동시에 배우게 합니다.

---

【 기술 스택/제약 】
- Python 3.11+ + FastAPI
- DB: Azure SQL Database (로컬 SQLite 금지)
- ORM: SQLAlchemy(동기식) + pyodbc
  - 엔진 생성: mssql+pyodbc:///?odbc_connect=urllib.parse.quote_plus(AZURE_SQL_CONNECTIONSTRING)
- DB 연결: 환경변수 AZURE_SQL_CONNECTIONSTRING(ODBC 형식)으로만 읽기
- 마이그레이션 도구(alembic) 제외 → Base.metadata.create_all만 사용
- Swagger: FastAPI 기본 /docs 사용 (각 엔드포인트에 response_model, summary 필수)
- 테스트: pytest
- CI/CD: GitHub Actions + OIDC(azure/login@v2) + Azure App Service

---

【 분리 개발 구조 】
- A 담당자: places/events 기능 (라우터/모델/스키마 분리)
- B 담당자: deals/docents 기능 (라우터/모델/스키마 분리)
- 스캐폴딩은 "작동하는 골격 + TODO 스텁"만 제공 (실제 CRUD는 학생이 구현)

---

【 생성할 파일 구조 】

```
repo-root/
  app/
    __init__.py
    main.py                    # FastAPI 앱 초기화, 라우터 등록
    db.py                      # Azure SQL 연결, SessionLocal, get_db 의존성
    models/
      __init__.py
      place.py                 # Place SQLAlchemy 모델
      event.py                 # Event SQLAlchemy 모델
      deal.py                  # Deal SQLAlchemy 모델
      docent.py                # Docent SQLAlchemy 모델
    schemas/
      __init__.py
      place.py                 # PlaceCreate, PlaceUpdate, PlaceResponse Pydantic
      event.py                 # EventCreate, EventUpdate, EventResponse Pydantic
      deal.py                  # DealCreate, DealResponse Pydantic
      docent.py                # DocenetCreate, DocenetResponse Pydantic
    routers/
      __init__.py
      places.py                # 5개 Place 엔드포인트 (TODO 스텁)
      events.py                # 6개 Event 엔드포인트 (TODO 스텁)
      deals.py                 # 4개 Deal + /deals/recommend (TODO 스텁)
      docents.py               # 4개 Docent + /docents/generate (TODO 스텁)
  scripts/
    __init__.py
    seed.py                    # 더미 데이터 생성 스크립트 (로컬/테스트용, 배포에서는 실행 금지)
  tests/
    __init__.py
    conftest.py                # pytest 공통 설정, get_db fixture
    test_health.py             # GET /health 테스트 (반드시 PASS)
  .github/
    ISSUE_TEMPLATE/
      config.yml               # blank issues 비활성
      feature.yml              # 기능 이슈 템플릿
      bug.yml                  # 버그 이슈 템플릿
    workflows/
      ci.yml                   # pytest 자동 실행
      deploy.yml               # main merge 시 Azure 배포
    pull_request_template.md   # PR 체크리스트
  requirements.txt
  .gitignore
  .env.example
  README.md
```

---

【 데이터 모델/스키마 최소 요구사항 】

#### Place (문화 공간)
- id: int (PK)
- name: str
- category: str (예: "band_club", "cinema", "bookstore", "popup")
- tags: str (또는 JSON, 예: "indie,vintage,lounge")
- latitude: float
- longitude: float
- created_at: datetime

#### Event (공연/상영/토크)
- id: int (PK)
- place_id: int (FK → Place.id)
- title: str
- start_time: datetime
- remaining_seats: int
- created_at: datetime

#### Deal (Last-minute 할인)
- id: int (PK)
- event_id: int (FK → Event.id)
- discount_rate: int (0-100)
- starts_at: datetime
- ends_at: datetime
- created_at: datetime

#### Docent (AI 도슨트)
- id: int (PK)
- place_id: int (FK → Place.id)
- tone: str (예: "energetic", "serene", "cultural")
- content: text (설명 텍스트)
- created_at: datetime

---

【 API 엔드포인트 (스텁 형태: 라우팅/문서는 완성, 로직은 TODO) 】

#### Health Check
- GET /health → {"status": "ok"} [작동 확인용, 반드시 완성]

#### Places (A 담당자)
- GET /places → [Place] (list)
- POST /places → Place (201 Created)
- GET /places/{place_id} → Place (200 OK) 또는 404 Not Found
- PATCH /places/{place_id} → Place (200 OK)
- DELETE /places/{place_id} → {} (204 No Content 또는 200 OK)

#### Events (A 담당자)
- GET /events → [Event] (list)
- POST /events → Event (201 Created)
- GET /events/{event_id} → Event (200 OK) 또는 404
- PATCH /events/{event_id} → Event (200 OK)
- DELETE /events/{event_id} → {} (204 또는 200)
- GET /places/{place_id}/events → [Event] (해당 place의 events만)

#### Deals (B 담당자)
- GET /deals → [Deal] (list)
- POST /deals → Deal (201 Created)
- GET /deals/{deal_id} → Deal (200 OK) 또는 404
- DELETE /deals/{deal_id} → {} (204 또는 200)
- POST /deals/recommend → {discount_rate, discounted_price, expires_at}
  - 입력: {event_id, remaining_seats, minutes_to_start, total_capacity}
  - 로직 (스텁): discount_rate = (occupancy_rate * 20) + (minutes_to_start * 2) 정도의 간단 계산만 스텁으로 둔다

#### Docents (B 담당자)
- GET /docents → [Docent] (list)
- POST /docents → Docent (201 Created)
- GET /docents/{docent_id} → Docent (200 OK) 또는 404
- DELETE /docents/{docent_id} → {} (204 또는 200)
- POST /docents/generate → {content}
  - 입력: {place_id, tone}
  - 로직 (스텁): 템플릿 기반 텍스트 생성만 구현 (예: f"당신의 {tone} 취향이 이 공간과 맞습니다.")

---

【 주요 파일 내용 상세 】

#### app/main.py
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import db
from app.routers import places, events, deals, docents

# DB 초기화
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
```

#### app/db.py
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
import urllib.parse
from typing import Generator

# 환경변수에서 ODBC 연결 문자열 읽기
odbc_str = os.getenv("AZURE_SQL_CONNECTIONSTRING")
if not odbc_str:
    raise ValueError("AZURE_SQL_CONNECTIONSTRING environment variable not set")

# mssql+pyodbc 엔진 생성
connection_string = f"mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(odbc_str)}"
engine = create_engine(connection_string, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """FastAPI 의존성: DB 세션 반환"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

#### 라우터 예시 (app/routers/places.py)
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.place import Place
from app.schemas.place import PlaceCreate, PlaceUpdate, PlaceResponse

router = APIRouter(prefix="/places", tags=["places"])

@router.get(
    "/",
    summary="List all places",
    description="Retrieve all culture spaces",
    response_model=list[PlaceResponse],
    status_code=status.HTTP_200_OK
)
async def list_places(db: Session = Depends(get_db)):
    """Get all places."""
    # TODO: Query DB and return list
    return []

@router.post(
    "/",
    summary="Create a new place",
    response_model=PlaceResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_place(place: PlaceCreate, db: Session = Depends(get_db)):
    """Create a new place."""
    # TODO: Create and save to DB
    raise NotImplementedError("TODO: Implement place creation")

# 다른 엔드포인트도 유사한 구조로 TODO 스텁
```

#### app/models/place.py
```python
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base

class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), index=True)
    category = Column(String(100))
    tags = Column(String(500), nullable=True)
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    events = relationship("Event", back_populates="place")
    docents = relationship("Docent", back_populates="place")
```

#### app/schemas/place.py
```python
from pydantic import BaseModel
from datetime import datetime

class PlaceCreate(BaseModel):
    name: str
    category: str
    tags: str | None = None
    latitude: float
    longitude: float

class PlaceUpdate(BaseModel):
    name: str | None = None
    category: str | None = None
    tags: str | None = None
    latitude: float | None = None
    longitude: float | None = None

class PlaceResponse(BaseModel):
    id: int
    name: str
    category: str
    tags: str | None
    latitude: float
    longitude: float
    created_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemy 호환성
```

---

【 .github/workflows/ci.yml 】
```yaml
name: CI

on:
  pull_request:
  push:
    branches: [ "main" ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest -v
```

【 .github/workflows/deploy.yml 】
```yaml
name: Deploy to Azure App Service (OIDC)

on:
  push:
    branches: [ "main" ]

permissions:
  id-token: write
  contents: read

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - run: pip install -r requirements.txt
      - run: pytest -v

      # OIDC login to Azure
      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      # Configure App Settings
      - name: Configure App Settings
        uses: azure/CLI@v2
        with:
          inlineScript: |
            az webapp config appsettings set \
              --resource-group ${{ secrets.AZURE_RESOURCE_GROUP }} \
              --name ${{ secrets.AZURE_WEBAPP_NAME }} \
              --settings \
                AZURE_SQL_CONNECTIONSTRING='${{ secrets.AZURE_SQL_CONNECTIONSTRING }}' \
                PINECONE_API_KEY='${{ secrets.PINECONE_API_KEY }}' \
                PINECONE_INDEX='${{ secrets.PINECONE_INDEX }}'

      # Deploy
      - name: Deploy to Web App
        uses: azure/webapps-deploy@v3
        with:
          app-name: ${{ secrets.AZURE_WEBAPP_NAME }}
          package: .
```

---

【 .github/ISSUE_TEMPLATE/feature.yml 】
```yaml
name: Feature
description: Implement an API feature (CRUD + Swagger)
title: "[Feature] "
labels: ["feature"]
body:
  - type: dropdown
    id: area
    attributes:
      label: Responsibility Area
      options: ["places/events (A)", "deals/docents (B)", "infra"]
    validations:
      required: true
  - type: textarea
    id: endpoints
    attributes:
      label: Endpoints to Implement
      placeholder: |
        - GET /places
        - POST /places
        - GET /places/{id}
        ...
    validations:
      required: true
  - type: checkboxes
    id: done
    attributes:
      label: Definition of Done
      options:
        - label: All endpoints callable in /docs (Swagger Try it out)
          required: true
        - label: Uses AZURE_SQL_CONNECTIONSTRING from env (no hardcoded DB)
          required: true
        - label: PR created and code reviewed
          required: true
        - label: pytest passes
          required: true
```

【 .github/ISSUE_TEMPLATE/bug.yml 】
```yaml
name: Bug
description: Report a bug
title: "[Bug] "
labels: ["bug"]
body:
  - type: textarea
    id: repro
    attributes:
      label: Steps to Reproduce
    validations:
      required: true
  - type: textarea
    id: expected
    attributes:
      label: Expected Behavior
    validations:
      required: true
  - type: textarea
    id: logs
    attributes:
      label: Logs / Screenshots
```

【 .github/pull_request_template.md 】
```markdown
## What does this PR do?
<!-- 한 줄 설명 -->

## How to test?
<!-- 테스트 방법 -->
1. 로컬에서 `git pull origin [branch]`
2. `uvicorn app.main:app --reload` 실행
3. http://localhost:8000/docs에서 엔드포인트 확인

## Checklist
- [ ] Tested in /docs (Swagger)
- [ ] Using AZURE_SQL_CONNECTIONSTRING env variable
- [ ] `pytest -v` passes
- [ ] No hardcoded secrets or DB credentials
- [ ] Code reviewed by teammate
```

---

【 requirements.txt 】
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
pyodbc==5.0.1
pydantic==2.5.0
python-dotenv==1.0.0
pytest==7.4.3
httpx==0.25.2
```

---

【 .env.example 】
```
AZURE_SQL_CONNECTIONSTRING="Driver={ODBC Driver 17 for SQL Server};Server=tcp:[SERVER].database.windows.net,1433;Database=[DB_NAME];Uid=[USERNAME];Pwd=[PASSWORD];Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
PINECONE_API_KEY="your-api-key"
PINECONE_INDEX="unmute-index"
```

---

【 .gitignore 】
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE
.vscode/
.idea/
*.swp
*.swo

# Env
.env
.env.local
.env.*.local

# DB (로컬 SQLite는 없지만, 안전하게)
*.db
*.sqlite
*.sqlite3

# Misc
.DS_Store
.coverage
htmlcov/
```

---

【 README.md 】
```markdown
# FastAPI Community – UNMUTE Backend API

Z세대를 위한 Indie Culture OS의 백엔드 API 스캐폴딩입니다.

## 🚀 Quick Start

### 1. 환경 준비
\`\`\`bash
git clone https://github.com/SKT8LL/fastapi-community.git
cd fastapi-community

# 가상 환경 생성
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 또는
.\venv\Scripts\Activate.ps1  # Windows

# 의존성 설치
pip install -r requirements.txt
\`\`\`

### 2. 환경 변수 설정
\`\`\`bash
# .env 파일 생성 (.env.example 참고)
cp .env.example .env

# .env 에디트 (실제 Azure SQL 연결 문자열 입력)
AZURE_SQL_CONNECTIONSTRING="Driver={...};Server=...;Database=...;Uid=...;Pwd=..."
\`\`\`

### 3. 서버 실행
\`\`\`bash
uvicorn app.main:app --reload
\`\`\`

### 4. API 문서 확인
브라우저에서: http://localhost:8000/docs

---

## 📋 기능 분담

### A 담당자 (진욱): Places & Events
- CRUD 엔드포인트: GET /places, POST /places, PATCH /places/{id}, DELETE /places/{id}
- Event 엔드포인트: GET /events, POST /events, GET /events/{id}, ...

### B 담당자 (필상): Deals & Docents
- Deal CRUD + POST /deals/recommend (동적 할인율 계산)
- Docent CRUD + POST /docents/generate (템플릿 기반 생성)

---

## 🧪 테스트

\`\`\`bash
pytest -v
\`\`\`

---

## 📚 기술 스택
- **Framework**: FastAPI
- **DB**: Azure SQL Database
- **ORM**: SQLAlchemy
- **Validation**: Pydantic
- **Testing**: pytest
- **CI/CD**: GitHub Actions + OIDC + Azure App Service

---

## 🔗 관련 링크
- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Azure SQL + Python 가이드](https://learn.microsoft.com/ko-kr/azure/azure-sql/database/azure-sql-python-quickstart)
- [GitHub Actions OIDC](https://docs.github.com/ko/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)

---

## 📝 Git 규칙
- \`main\` 브랜치는 직접 push 금지 (PR로만 merge)
- 기능 브랜치: \`feature/places-events\`, \`feature/deals-docents\`
- PR 전 \`pytest -v\` 실행 필수

---

더 자세한 정보는 \`fastapi_assignment_guide.md\` 를 참고하세요!
\`\`\`

---

【 tests/conftest.py 】
```python
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db import Base, get_db
from app.main import app

# 테스트 DB (in-memory SQLite, 또는 별도 테스트 Azure SQL)
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
```

【 tests/test_health.py 】
```python
def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
```

---

【 생성 지침 】
1. 위 전체 파일을 실제로 생성한다.
2. 코드는 실행 가능해야 하고 (최소 uvicorn app.main:app --reload 성공), 
   GET /health 와 /docs 는 즉시 작동해야 한다.
3. 각 라우터/모델/스키마는 구조는 완성하되, 
   CRUD 로직은 NotImplementedError("TODO: ...") 또는 빈 리스트 반환으로 스텁화한다.
4. 모든 엔드포인트는 response_model, summary, description 을 지정해서
   /docs 에서 깔끔하게 보이도록 한다.
5. 더미 데이터 스크립트(seed.py)는 로컬 테스트용이고, 배포 시 실행되지 않도록 주석 처리하기.
```

---

## 사용 방법

1. 위 프롬프트를 **전체 복사**
2. Antigravity(또는 Claude/GPT)에 입력
3. 생성된 파일들을 GitHub 레포에 커밋
4. 진욱, 필상에게 클론하라고 안내

완료!
