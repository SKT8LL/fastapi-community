from datetime import datetime, timedelta

def test_deal_lifecycle(client):
    # 1. Create a fresh deal (POST)
    payload = {
        "event_id": 999,
        "discount_rate": 25,
        "starts_at": datetime.utcnow().isoformat(),
        "ends_at": (datetime.utcnow() + timedelta(days=7)).isoformat()
    }
    
    response = client.post("/deals/", json=payload)
    assert response.status_code == 201
    data = response.json()
    
    deal_id = data["id"]
    assert data["discount_rate"] == 25
    assert data["event_id"] == 999

    # 2. List all deals (GET)
    response = client.get("/deals/")
    assert response.status_code == 200
    deals = response.json()
    
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
