# FastAPI Community 과제 가이드

**Project**: SKT8LL/fastapi-community  
**Date**: 2026-01-11  
**Version**: 1.0  
**Audience**: 진욱, 필상 (및 향후 팀원)

---

## 📌 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [UNMUTE 서비스와 API 매핑](#unmute-서비스와-api-매핑)
3. [기능 분담](#기능-분담)
4. [환경 세팅](#환경-세팅)
5. [로컬 개발 가이드](#로컬-개발-가이드)
6. [GitHub 협업 규칙](#github-협업-규칙)
7. [배포 및 CI/CD](#배포-및-cicd)
8. [이슈 트래킹](#이슈-트래킹)
9. [Swagger 문서 확인](#swagger-문서-확인)
10. [완료 기준 (Definition of Done)](#완료-기준--definition-of-done)

---

## 프로젝트 개요

### 🎯 목표
FastAPI + Azure SQL + GitHub Actions를 이용해 **UNMUTE(Z세대를 위한 Indie Culture OS)** 서비스의 백엔드 API를 구현하면서 동시에 다음을 익힌다:
- **CRUD 구현**: Create, Read, Update, Delete 기본 패턴
- **Swagger 문서**: OpenAPI 기반 자동 API 문서화
- **Git 협업**: 브랜치, PR, 코드 리뷰
- **CI/CD 자동화**: GitHub Actions로 테스트 및 Azure 배포 자동화
- **이슈 트래킹**: GitHub Issues + Projects로 프로젝트 관리

### 🎭 UNMUTE란?
- **개념**: 로컬 인디 문화(밴드 공연, 영화관, 독립서점, 팝업, 소극장)를 한 앱에서 발견 → 이동 → 예약 → 경험할 수 있는 OS
- **핵심 기능**:
  1. **Culture Pin**: T-map 위 취향 맞춤 인디 공간 지도
  2. **Last-minute Indie Deal**: 마감 임박 이벤트의 동적 할인
  3. **A. Docent**: AI 기반 공간/공연 감정적 설명
  4. **Realtime Performance Feed**: 공연 중 관객↔퍼포머 실시간 상호작용
  5. **Debut Incubator**: 신인 창작자 6개월 무료 육성

---

## UNMUTE 서비스와 API 매핑

### 📊 데이터 모델 (4가지 핵심 엔티티)

| 엔티티 | 설명 | 주요 필드 |
|--------|------|---------|
| **Place** | 밴드클럽, 영화관, 서점, 팝업 등 문화 공간 | id, name, category, tags, latitude, longitude, created_at |
| **Event** | 특정 Place에서 일어나는 공연/상영/토크 | id, place_id(FK), title, start_time, remaining_seats, created_at |
| **Deal** | Last-minute 할인(특정 Event에 적용) | id, event_id(FK), discount_rate, starts_at, ends_at, created_at |
| **Docent** | "왜 이 공간이 당신과 맞는가"라는 AI 설명 | id, place_id(FK), tone, content, created_at |

### 🔗 관계도
```
Place (1) ─────────── (N) Event
  │                      │
  │                      ├─── (1) Deal (Optional, per Event)
  │
  └─── (1:N) Docent
```

### 🌐 핵심 엔드포인트 (초기 스캐폴딩 제공, CRUD는 학생 구현)

#### A 담당자 (진욱): Places & Events 축
```
GET    /health                    # 헬스 체크
GET    /places                    # 모든 장소 조회 (필터/검색 선택)
POST   /places                    # 새 장소 생성
GET    /places/{place_id}         # 특정 장소 상세
PATCH  /places/{place_id}         # 장소 정보 수정
DELETE /places/{place_id}         # 장소 삭제

GET    /events                    # 모든 이벤트 조회
POST   /events                    # 새 이벤트 생성
GET    /events/{event_id}         # 특정 이벤트 상세
PATCH  /events/{event_id}         # 이벤트 정보 수정
DELETE /events/{event_id}         # 이벤트 삭제
GET    /places/{place_id}/events  # 특정 Place의 모든 Event
```

#### B 담당자 (필상): Deals & Docents 축
```
GET    /deals                     # 모든 딜 조회
POST   /deals                     # 새 딜 생성
GET    /deals/{deal_id}           # 특정 딜 상세
DELETE /deals/{deal_id}           # 딜 삭제
POST   /deals/recommend           # 동적 할인율 계산 (입력: event_id, remaining_seats, minutes_to_start)

GET    /docents                   # 모든 도슨트 조회
POST   /docents                   # 새 도슨트 생성
GET    /docents/{docent_id}       # 특정 도슨트 상세
DELETE /docents/{docent_id}       # 도슨트 삭제
POST   /docents/generate          # 템플릿 기반 도슨트 생성 (입력: place_id, tone)
```

---

## 기능 분담

### A 담당자: 진욱 (Places & Events)
**기간**: 1주 ~ 1.5주

**구현 내용**:
- `models/place.py`: Place SQLAlchemy 모델
- `models/event.py`: Event SQLAlchemy 모델
- `schemas/place.py`: PlaceCreate, PlaceUpdate, PlaceResponse Pydantic 스키마
- `schemas/event.py`: EventCreate, EventUpdate, EventResponse Pydantic 스키마
- `routers/places.py`: 5개 Place 엔드포인트
- `routers/events.py`: 6개 Event 엔드포인트 + `GET /places/{place_id}/events`

**DoD (Definition of Done)**:
- 모든 엔드포인트가 `/docs`에서 "Try it out" 가능
- SQL 쿼리 로직 동작 (CRUD 실제 작동)
- 상태 코드 정확 (201 for POST, 404 for not found, etc.)
- PR 1개 이상 생성 후 코드 리뷰 완료
- pytest 통과

**Issues**:
- Create: `[Feature] A-1: Place CRUD & Swagger` (라벨: `area:places-events`, `type:feature`)
- Create: `[Feature] A-2: Event CRUD & Relationship` (라벨: `area:places-events`, `type:feature`)

---

### B 담당자: 필상 (Deals & Docents)
**기간**: 1주 ~ 1.5주

**구현 내용**:
- `models/deal.py`: Deal SQLAlchemy 모델
- `models/docent.py`: Docent SQLAlchemy 모델
- `schemas/deal.py`: DealCreate, DealResponse Pydantic 스키마
- `schemas/docent.py`: DocenetCreate, DocenetResponse Pydantic 스키마
- `routers/deals.py`: 4개 Deal 엔드포인트 + `POST /deals/recommend` (동적 할인율 계산)
- `routers/docents.py`: 4개 Docent 엔드포인트 + `POST /docents/generate` (템플릿 기반)

**동적 할인율 계산 규칙** (`/deals/recommend`):
```python
# 입력:
{
  "event_id": 1,
  "remaining_seats": 8,
  "minutes_to_start": 22,
  "total_capacity": 30
}

# 로직:
occupancy_rate = (total_capacity - remaining_seats) / total_capacity
discount_rate = (occupancy_rate * 20) + (minutes_to_start * 2)  # 간단 규칙
# 최종 응답:
{
  "discount_rate": 35,
  "discounted_price": 6500,  # 원가 10000 기준
  "expires_at": "2026-01-11T12:30:00"
}
```

**DoD (Definition of Done)**:
- 모든 엔드포인트가 `/docs`에서 "Try it out" 가능
- SQL 쿼리 로직 동작
- `/deals/recommend` 계산 로직 동작
- `/docents/generate`에서 최소 템플릿 기반 텍스트 반환
- PR 1개 이상 생성 후 코드 리뷰 완료
- pytest 통과

**Issues**:
- Create: `[Feature] B-1: Deal CRUD & Dynamic Discount Logic` (라벨: `area:deals-docents`, `type:feature`)
- Create: `[Feature] B-2: Docent CRUD & Template Generation` (라벨: `area:deals-docents`, `type:feature`)

---

## 환경 세팅

### 1️⃣ Python 환경 준비 (로컬)

#### macOS / Linux
```bash
cd ~/Desktop  # 또는 원하는 경로
git clone https://github.com/SKT8LL/fastapi-community.git
cd fastapi-community

# Python 가상 환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

#### Windows (PowerShell)
```powershell
git clone https://github.com/SKT8LL/fastapi-community.git
cd fastapi-community

python -m venv venv
.\venv\Scripts\Activate.ps1

pip install -r requirements.txt
```

### 2️⃣ 환경 변수 설정

**로컬 개발용 `.env` 파일 생성** (레포에 커밋하면 안 됨)

```bash
# .env (git에 커밋하지 말 것)
AZURE_SQL_CONNECTIONSTRING="Driver={ODBC Driver 17 for SQL Server};Server=tcp:[YOUR_SERVER].database.windows.net,1433;Database=[YOUR_DB];Uid=[YOUR_USER];Pwd=[YOUR_PASSWORD];Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
PINECONE_API_KEY="your-pinecone-api-key"
PINECONE_INDEX="unmute-index"
```

**`.env.example` 예시** (레포에 커밋되는 파일, 실제 값 없음)
```bash
# .env.example
AZURE_SQL_CONNECTIONSTRING="Driver={ODBC Driver 17 for SQL Server};Server=tcp:[SERVER].database.windows.net,1433;Database=[DB_NAME];Uid=[USERNAME];Pwd=[PASSWORD];Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
PINECONE_API_KEY="your-api-key"
PINECONE_INDEX="unmute-index"
```

### 3️⃣ 데이터베이스 초기화 (선택)

스케폴딩 제공 시 더미 데이터를 Azure SQL에 넣는 스크립트가 포함됩니다:

```bash
# (배포 전에는 실행 금지. 로컬 개발/테스트 시에만)
python -m scripts.seed
```

---

## 로컬 개발 가이드

### 1️⃣ 서버 실행

```bash
# 가상환경 활성화 (이미 했으면 스킵)
source venv/bin/activate  # macOS/Linux
# 또는
.\venv\Scripts\Activate.ps1  # Windows

# FastAPI 개발 서버 시작
uvicorn app.main:app --reload
```

**출력 예시**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 2️⃣ API 테스트 (Swagger)

브라우저에서 열기:
```
http://localhost:8000/docs
```

**Swagger UI에서 할 수 있는 것**:
- 모든 엔드포인트 확인
- "Try it out" 버튼으로 직접 호출
- Request/Response 예시 확인
- 상태 코드 확인 (200, 201, 404, 422 등)

### 3️⃣ 테스트 실행

```bash
# pytest 실행 (모든 tests/*.py)
pytest -v

# 특정 파일만 테스트
pytest tests/test_health.py -v

# 커버리지 리포트 보기 (선택)
pytest --cov=app tests/
```

### 4️⃣ 코드 스타일 확인 (선택)

```bash
# 기본 스타일 체크
black app/ --check

# 자동 수정
black app/

# Lint (flake8 권장)
flake8 app/ --max-line-length=120
```

---

## GitHub 협업 규칙

### ✅ 브랜치 전략

| 브랜치 | 용도 | 누구 |
|--------|------|-----|
| `main` | 배포되는 안정 코드 (직접 push 금지) | 관리자만 merge |
| `feature/places-events` | A 담당자의 작업 | 진욱 |
| `feature/deals-docents` | B 담당자의 작업 | 필상 |
| `bugfix/*` | 버그 수정 | 누구든 필요시 |
| `refactor/*` | 코드 정리 | 누구든 필요시 |

### 📝 작업 흐름

#### Step 1: 로컬에서 시작
```bash
# main 업데이트
git checkout main
git pull origin main

# 기능 브랜치 생성
git checkout -b feature/places-events
# (또는 git checkout -b feature/deals-docents)
```

#### Step 2: 코드 구현
```bash
# 파일 수정
vi app/routers/places.py

# 변경사항 확인
git status

# 스테이징
git add app/routers/places.py
# 또는 전체
git add .

# 커밋 (작은 단위로!)
git commit -m "feat: implement GET /places endpoint"
git commit -m "fix: handle 404 for non-existent place"
```

#### Step 3: 푸시 & PR 생성
```bash
# 브랜치 푸시
git push origin feature/places-events

# GitHub 웹에서 PR 생성
# (또는 gh pr create --title "Places & Events CRUD" --body "...")
```

#### Step 4: 코드 리뷰 & 머지
- 상대방(또는 리뷰어)이 PR 확인
- `/docs`에서 엔드포인트 직접 호출해보기
- "Approve" 후 "Merge" (스쿼시 권장)
- 로컬에서 `git pull origin main` 하면 최신 코드 반영

### 📋 커밋 메시지 규칙 (선택 사항이지만 권장)

```
feat: 새 기능 추가
fix: 버그 수정
refactor: 코드 정리 (기능 변화 없음)
test: 테스트 추가/수정
docs: 문서만 수정
chore: 의존성, 빌드 설정 등

예시:
git commit -m "feat: add Place CRUD endpoints"
git commit -m "fix: handle timezone in start_time"
git commit -m "test: add test for GET /places/{id}"
```

### ❌ 하면 안 되는 것
```bash
# ❌ 절대 금지: main에 직접 푸시
git push origin main

# ❌ merge 전 반드시 테스트 실행
pytest -v  # PR 머지 전에 실행해야 함

# ❌ .db 파일이나 .env 파일 커밋
git add app.db   # ❌ 금지
git add .env     # ❌ 금지
```

---

## 배포 및 CI/CD

### 🔐 OIDC 인증 (Azure + GitHub Actions)

**과제 제공자(당신)가 Azure에서 해야 할 것**:

1. **Azure 리소스 생성** (이미 했으면 스킵)
   - Resouce Group 생성
   - Azure SQL Database 생성 + 서버/사용자명/비밀번호 기록
   - Azure App Service 생성 (Python 3.11, Linux)

2. **Entra ID (Azure AD)에 앱 등록**
   ```
   Azure Portal → Entra ID → App registrations → New registration
   - Name: fastapi-community-deploy
   - 생성 후 Client ID, Tenant ID 기록
   ```

3. **Federated Credentials 추가**
   ```
   앱 등록 → Certificates & secrets → Federated credentials → Add credential
   - Scenario: GitHub Actions deploying to Azure
   - Organization: SKT8LL (또는 개인 계정)
   - Repository: fastapi-community
   - Entity type: Branch
   - Branch name: main
   - Credential details: 자동 생성됨
   ```

4. **서비스 주체에 역할 부여**
   ```
   Resource Group → Access control (IAM) → Add role assignment
   - Role: Contributor (또는 Deployment Contributor)
   - Assign to: (위에서 만든 앱)
   ```

5. **GitHub Secrets 추가**
   ```
   GitHub Repo → Settings → Secrets and variables → Actions → New repository secret
   
   필수 secrets:
   - AZURE_CLIENT_ID         : (Entra ID 앱의 Client ID)
   - AZURE_TENANT_ID         : (Tenant ID)
   - AZURE_SUBSCRIPTION_ID   : (Subscription ID)
   - AZURE_RESOURCE_GROUP    : (리소스 그룹 이름)
   - AZURE_WEBAPP_NAME       : (App Service 이름)
   - AZURE_SQL_CONNECTIONSTRING : (SQL 연결 문자열)
   - PINECONE_API_KEY        : (Pinecone API 키)
   - PINECONE_INDEX          : (Pinecone 인덱스 이름)
   ```

### 🚀 CI/CD 워크플로 제공 파일

**`.github/workflows/ci.yml`** (PR 및 main push 시 테스트 실행)
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

**`.github/workflows/deploy.yml`** (main merge 후 자동 배포)
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

      # Configure App Settings (환경 변수 주입)
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

      # Deploy to Web App
      - name: Deploy to Web App
        uses: azure/webapps-deploy@v3
        with:
          app-name: ${{ secrets.AZURE_WEBAPP_NAME }}
          package: .
```

### 📊 배포 확인

1. **PR 제출**: GitHub Actions의 CI 워크플로 실행 확인 ✅
   - 로그 보기: PR → "Checks" 탭
   
2. **main에 머지**: CD 워크플로 실행
   - 로그 보기: "Actions" 탭 → 최신 workflow run

3. **배포 완료**: App Service에서 접속 테스트
   ```
   https://[YOUR_WEBAPP_NAME].azurewebsites.net/docs
   ```

---

## 이슈 트래킹

### 📋 이슈 생성 규칙

**GitHub Issues → "New issue" → 템플릿 선택**

#### Feature 이슈 (`.github/ISSUE_TEMPLATE/feature.yml`)
```markdown
Title: [Feature] A-1: Place CRUD & Swagger

Area: places/events

Endpoints to implement:
- POST /places
- GET /places
- GET /places/{place_id}
- PATCH /places/{place_id}
- DELETE /places/{place_id}

Definition of Done:
- [ ] All endpoints callable in /docs
- [ ] SQL queries working (CRUD logic complete)
- [ ] Correct HTTP status codes (201, 200, 404, etc.)
- [ ] PR created and code reviewed
- [ ] pytest passes
```

#### Bug 이슈 (`.github/ISSUE_TEMPLATE/bug.yml`)
```markdown
Title: [Bug] /places returns 500 error

Repro steps:
1. GET /places
2. See error response

Expected:
200 response with list of places

Actual:
500 Internal Server Error

Logs:
[error traceback here]
```

### 🎯 이슈 라벨 (자동 추가)

| 라벨 | 의미 |
|-----|------|
| `area:places-events` | A 담당자(진욱) 영역 |
| `area:deals-docents` | B 담당자(필상) 영역 |
| `type:feature` | 새 기능 |
| `type:bug` | 버그 리포트 |
| `status:in-progress` | 작업 중 |
| `status:blocked` | 막힌 상태 |
| `status:review` | 리뷰 대기 |

### 📊 GitHub Projects (선택)

**권장 보드 설정**:
- **Backlog**: 아직 시작 안 한 이슈
- **In progress**: 작업 중인 이슈
- **In review**: PR/코드 리뷰 대기
- **Done**: 완료된 이슈

**사용 방법**:
1. 이슈 생성 시 자동으로 "Backlog"에 추가
2. 이슈에 "Assignees" 추가 (진욱 또는 필상)
3. 작업 시작하면 "In progress"로 이동
4. PR 생성 시 "In review"로 이동
5. 코드 머지 후 "Done"으로 이동

**담당자별 필터 뷰** (권장):
- View "🧑‍💻 진욱": Filter by Assignee = 진욱
- View "🧑‍💻 필상": Filter by Assignee = 필상

---

## Swagger 문서 확인

### 🌐 로컬에서 접속

```
http://localhost:8000/docs
```

### ✅ Swagger에 나타나는 항목들

각 엔드포인트마다:
- **Summary**: 간단한 설명 (예: "Create a new place")
- **Description**: 자세한 설명
- **Parameters**: 입력값 (경로, 쿼리, 바디)
- **Response models**: 출력 데이터 구조 (JSON 예시)
- **Status codes**: 가능한 응답 코드 (200, 201, 404 등)

### 📝 코드 예시 (Swagger가 자동으로 읽음)

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(prefix="/places", tags=["places"])

@router.get(
    "/",
    summary="List all places",
    description="Retrieve all culture spaces with optional filtering",
    response_model=list[PlaceResponse],
    status_code=status.HTTP_200_OK
)
async def list_places(db: Session = Depends(get_db)):
    """
    Get all places.
    
    - **Returns**: List of places
    """
    places = db.query(Place).all()
    return places
```

**생성되는 Swagger 항목**:
- Summary: "List all places"
- Description: "Retrieve all culture spaces..."
- Response model: PlaceResponse 스키마 표시
- 예시 JSON 자동 표시

---

## 완료 기준 (Definition of Done)

### ✅ A 담당자 (진욱) - Places/Events 체크리스트

- [ ] **환경 세팅**
  - [ ] 로컬 venv 생성 및 pip install -r requirements.txt
  - [ ] .env 파일 생성 (AZURE_SQL_CONNECTIONSTRING 포함)
  - [ ] uvicorn 서버 실행 확인

- [ ] **코드 구현**
  - [ ] `models/place.py` 구현 (Place SQLAlchemy 모델)
  - [ ] `models/event.py` 구현 (Event SQLAlchemy 모델, place_id FK)
  - [ ] `schemas/place.py` 구현 (PlaceCreate, PlaceUpdate, PlaceResponse)
  - [ ] `schemas/event.py` 구현 (EventCreate, EventUpdate, EventResponse)
  - [ ] `routers/places.py` 구현 (5개 엔드포인트 + CRUD 로직)
  - [ ] `routers/events.py` 구현 (6개 엔드포인트 + 관계 처리)

- [ ] **Swagger & 테스트**
  - [ ] http://localhost:8000/docs에서 모든 엔드포인트 보이는지 확인
  - [ ] POST /places → 201 Created + 데이터 저장 확인
  - [ ] GET /places → 200 OK + 리스트 반환 확인
  - [ ] GET /places/{id} → 200 OK 또는 404 Not Found 확인
  - [ ] PATCH /places/{id} → 200 OK + 업데이트 확인
  - [ ] DELETE /places/{id} → 204 No Content 또는 200 OK 확인
  - [ ] GET /events 및 POST /events 동일하게 확인
  - [ ] GET /places/{place_id}/events → 해당 place의 events만 반환 확인

- [ ] **Git & PR**
  - [ ] 기능 브랜치 `feature/places-events` 생성
  - [ ] 작은 단위로 커밋 (최소 3개 이상)
  - [ ] PR 생성 + 설명 작성
  - [ ] 코드 리뷰 완료 (필상 또는 관리자)
  - [ ] 코드 리뷰 반영 (수정 있을 시)
  - [ ] Approve 후 Merge (main 브랜치)

- [ ] **테스트**
  - [ ] `pytest -v` 실행 → 모든 테스트 PASS
  - [ ] `/docs`에서 "Try it out" 버튼으로 실제 호출 확인

---

### ✅ B 담당자 (필상) - Deals/Docents 체크리스트

- [ ] **환경 세팅**
  - [ ] 로컬 venv 생성 및 pip install -r requirements.txt
  - [ ] .env 파일 생성
  - [ ] uvicorn 서버 실행 확인

- [ ] **코드 구현**
  - [ ] `models/deal.py` 구현 (Deal SQLAlchemy 모델, event_id FK)
  - [ ] `models/docent.py` 구현 (Docent SQLAlchemy 모델, place_id FK)
  - [ ] `schemas/deal.py` 구현 (DealCreate, DealResponse)
  - [ ] `schemas/docent.py` 구현 (DocenetCreate, DocenetResponse)
  - [ ] `routers/deals.py` 구현 (4개 기본 + POST /deals/recommend)
    - POST /deals/recommend 로직: 남은 좌석, 시작까지 분 단위 시간을 입력받아 동적 할인율 계산
  - [ ] `routers/docents.py` 구현 (4개 기본 + POST /docents/generate)
    - POST /docents/generate 로직: place_id, tone을 받아 템플릿 기반 설명 생성

- [ ] **Swagger & 테스트**
  - [ ] http://localhost:8000/docs에서 모든 엔드포인트 보이는지 확인
  - [ ] POST /deals → 201 Created 확인
  - [ ] GET /deals → 200 OK + 리스트 반환 확인
  - [ ] GET /deals/{id} → 200 OK 또는 404 확인
  - [ ] POST /deals/recommend → 200 OK + discount_rate 필드 포함 확인
  - [ ] POST /docents → 201 Created 확인
  - [ ] GET /docents → 200 OK 확인
  - [ ] POST /docents/generate → 200 OK + content 필드 포함 확인

- [ ] **Git & PR**
  - [ ] 기능 브랜치 `feature/deals-docents` 생성
  - [ ] 작은 단위로 커밋 (최소 3개 이상)
  - [ ] PR 생성 + 설명 작성
  - [ ] 코드 리뷰 완료 (진욱 또는 관리자)
  - [ ] Approve 후 Merge (main 브랜치)

- [ ] **테스트**
  - [ ] `pytest -v` 실행 → 모든 테스트 PASS
  - [ ] `/docs`에서 "Try it out"으로 실제 호출 확인

---

## 최종 배포 및 발표

### 📌 최종 체크리스트

- [ ] main 브랜치에 A, B 담당자의 코드 모두 머지
- [ ] CI 워크플로 실행 및 PASS
- [ ] CD 워크플로 실행 → Azure App Service 배포 완료
- [ ] https://[YOUR_WEBAPP_NAME].azurewebsites.net/docs 접속 확인
- [ ] 모든 엔드포인트 작동 확인
- [ ] 데이터 베이스(Azure SQL)에 데이터 저장됨 확인

### 🎤 발표 준비

- [ ] `/docs` 화면 캡처 (모든 엔드포인트 보이게)
- [ ] 각 엔드포인트 "Try it out" 데모 시연
- [ ] 깃 커밋/PR 이력 보여주기
- [ ] 배포 로그 보여주기 (Actions → Deploy 워크플로)

---

## 참고 자료 & 문제 해결

### 📚 도움이 될 링크들

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [SQLAlchemy ORM 튜토리얼](https://docs.sqlalchemy.org/en/20/orm/)
- [Pydantic 스키마 가이드](https://docs.pydantic.dev/latest/)
- [Azure SQL + Python 퀵스타트](https://learn.microsoft.com/ko-kr/azure/azure-sql/database/azure-sql-python-quickstart)
- [GitHub Actions 공식 문서](https://docs.github.com/ko/actions)
- [Azure OIDC 설정 가이드](https://docs.github.com/ko/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)

### 🔧 흔한 문제 & 해결법

#### 1. "ModuleNotFoundError: No module named 'app'"
```bash
# 해결: 프로젝트 루트에서 실행
cd fastapi-community
uvicorn app.main:app --reload
```

#### 2. "AZURE_SQL_CONNECTIONSTRING is not set"
```bash
# 해결: .env 파일 확인 및 load_dotenv 호출
# app/main.py 상단에
from dotenv import load_dotenv
load_dotenv()
```

#### 3. "Connection to Azure SQL failed"
```bash
# 해결: 연결 문자열 형식 확인
# 올바른 형식 예:
Driver={ODBC Driver 17 for SQL Server};
Server=tcp:[server].database.windows.net,1433;
Database=[db];
Uid=[user];
Pwd=[password];
Encrypt=yes;
TrustServerCertificate=no;
Connection Timeout=30;
```

#### 4. "POST /places returns 422 Unprocessable Entity"
```bash
# 해결: Swagger에서 Request body 예시 확인
# 또는 POST 시 필수 필드 확인
GET /docs → POST /places → Try it out → Schema 확인
```

#### 5. "pytest fails: fixture 'db' not found"
```bash
# 해결: conftest.py 생성 또는 테스트에서 db fixture 수정
# tests/conftest.py 생성하고 get_db 오버라이드
```

---

## 연락처 & 피드백

**과제 관련 Q&A**:
- 이슈 생성: GitHub Issues (라벨: `type:question`)
- 긴급: Direct message

**피드백 환영**:
- PR 리뷰 시 건설적인 의견
- 문서 개선 제안
- 배포 후 성능/안정성 이슈 리포트

---

**마지막 조언**: 천천히 진행하세요. CRUD를 먼저 완벽히 익힌 후, 테스트와 배포까지 순서대로 경험하는 것이 가장 좋습니다. 🚀

**Happy coding! 🎭✨**
