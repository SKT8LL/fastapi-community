# FastAPI Community – UNMUTE Backend API

Z세대를 위한 Indie Culture OS의 백엔드 API 스캐폴딩입니다.

## 🚀 Quick Start

### 1. 환경 준비
```bash
git clone https://github.com/SKT8LL/fastapi-community.git
cd fastapi-community

# [macOS] pyodbc 시스템 의존성 설치
brew install unixodbc

# uv 설치 (없을 경우)
pip install uv

# 가상 환경 생성 및 의존성 설치
uv venv
source .venv/bin/activate  # macOS/Linux
# 또는
.venv\Scripts\activate  # Windows

uv pip install -r requirements.txt
```

### 2. 환경 변수 설정
```bash
# .env 파일 생성 (.env.example 참고)
cp .env.example .env

# .env 에디트 (Azure PostgreSQL 연결 문자열 입력)
DATABASE_URL="postgresql+psycopg2://user:password@host:5432/dbname"
```

### 3. 서버 실행
```bash
uv run uvicorn app.main:app --reload
```

### 4. API 문서 확인
브라우저에서: http://localhost:8000/docs

---

## 📋 기능 분담

### 정필상: Places & Events
- branch : feature/palce_event
- CRUD 엔드포인트: GET /places, POST /places, PATCH /places/{id}, DELETE /places/{id}
- Event 엔드포인트: GET /events, POST /events, GET /events/{id}, ...
- CRUD에 대한 정확한 이해를 가지고 할 것.

### 김진욱: Deals & Docents
- branch : feature/deal_docent
- Deal CRUD + POST /deals/recommend (동적 할인율 계산)
- Docent CRUD + POST /docents/generate (템플릿 기반 생성)

---

## 🧪 테스트

```bash
pytest -v
```

---

## 📚 기술 스택
- **Framework**: FastAPI
- **DB**: Azure Database for PostgreSQL
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
- `main` 브랜치는 직접 push 금지 (PR로만 merge)
- 기능 브랜치: `feature/places-events`, `feature/deals-docents`
- PR 전 `pytest -v` 실행 필수

---

더 자세한 정보는 `fastapi_assignment_guide.md` 를 참고하세요!
