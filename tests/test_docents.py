def test_docent_lifecycle(client):
    # 1. Create a fresh docent (POST)
    payload = {
        "place_id": 101,
        "tone": "serene",
        "content": "이곳은 아주 조용하고 평화로운 공간입니다."
    }
    
    response = client.post("/docents/", json=payload)
    assert response.status_code == 201
    data = response.json()
    
    docent_id = data["id"]
    assert data["tone"] == "serene"
    assert data["place_id"] == 101

    # 2. List all docents (GET)
    response = client.get("/docents/")
    assert response.status_code == 200
    docents = response.json()
    
    found = False
    for d in docents:
        if d["id"] == docent_id:
            found = True
            break
    assert found is True

    # 3. Get specific docent (GET /{id})
    response = client.get(f"/docents/{docent_id}")
    assert response.status_code == 200
    assert response.json()["id"] == docent_id

    # 4. Delete the docent (DELETE)
    response = client.delete(f"/docents/{docent_id}")
    assert response.status_code == 204

    # 5. Verify it's gone (GET /{id} -> 404)
    response = client.get(f"/docents/{docent_id}")
    assert response.status_code == 404

def test_generate_docent(client):
    # Special endpoint test
    payload = {
        "place_id": 500,
        "tone": "energetic"
    }
    response = client.post("/docents/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "energetic" in data["content"]
