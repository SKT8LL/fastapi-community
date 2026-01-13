from fastapi.testclient import TestClient
from app.main import app
from app.db import Base, engine
from app.models.deal import Deal
from datetime import datetime, timedelta

# Create tables for test
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_deal_lifecycle():
    # 1. Create a fresh deal (POST)
    # create_deal expects: event_id, discount_rate, starts_at, ends_at
    payload = {
        "event_id": 999,  # 임의의 ID
        "discount_rate": 25,
        "starts_at": datetime.utcnow().isoformat(),
        "ends_at": (datetime.utcnow() + timedelta(days=7)).isoformat()
    }
    
    response = client.post("/deals/", json=payload)
    assert response.status_code == 201
    data = response.json()
    
    # 생성된 데이터 검증
    deal_id = data["id"]
    assert data["discount_rate"] == 25
    assert data["event_id"] == 999

    # 2. List all deals (GET) should contain the new deal
    response = client.get("/deals/")
    assert response.status_code == 200
    deals = response.json()
    # 방금 만든 deal_id가 리스트 안에 있는지 확인
    found = False
    for d in deals:
        if d["id"] == deal_id:
            found = True
            break
    assert found is True

    # 3. Get specific deal (GET /{id})
    response = client.get(f"/deals/{deal_id}")
    assert response.status_code == 200
    assert response.json()["id"] == deal_id

    # 4. Delete the deal (DELETE)
    response = client.delete(f"/deals/{deal_id}")
    assert response.status_code == 204

    # 5. Verify it's gone (GET /{id} -> 404)
    response = client.get(f"/deals/{deal_id}")
    assert response.status_code == 404
