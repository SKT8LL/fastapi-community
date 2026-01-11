## What does this PR do?
<!-- 한 줄 설명 -->

## How to test?
<!-- 테스트 방법 -->
1. 로컬에서 `git pull origin [branch]`
2. `source .venv/bin/activate` 및 `uvicorn app.main:app --reload` 실행
3. http://localhost:8000/docs에서 엔드포인트 확인

## Checklist
- [ ] Tested in /docs (Swagger)
- [ ] Using AZURE_SQL_CONNECTIONSTRING env variable
- [ ] `pytest -v` passes
- [ ] No hardcoded secrets or DB credentials
- [ ] Code reviewed by teammate
