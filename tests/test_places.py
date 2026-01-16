from fastapi import status

def test_create_place(client):
    response = client.post(
        "/places/",
        json={
            "name": "Test Museum",
            "category": "Museum",
            "latitude": 37.5,
            "longitude": 127.0,
            "tags": "art,history",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Test Museum"
    assert "id" in data
    return data["id"]

def test_list_places(client):
    # Ensure at least one place exists
    client.post(
        "/places/",
        json={
            "name": "Another Place",
            "category": "Park",
            "latitude": 36.5,
            "longitude": 128.0,
        },
    )
    response = client.get("/places/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_get_place(client):
    # Create first
    create_res = client.post(
        "/places/",
        json={
            "name": "Get Me",
            "category": "Spot",
            "latitude": 35.5,
            "longitude": 129.0,
        },
    )
    place_id = create_res.json()["id"]

    # Get
    response = client.get(f"/places/{place_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Get Me"
    assert data["id"] == place_id

def test_update_place(client):
    # Create first
    create_res = client.post(
        "/places/",
        json={
            "name": "Old Name",
            "category": "Old Category",
            "latitude": 30.0,
            "longitude": 130.0,
        },
    )
    place_id = create_res.json()["id"]

    # Update
    response = client.patch(
        f"/places/{place_id}",
        json={"name": "New Name"},
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "New Name"
    assert data["category"] == "Old Category" # Should remain unchanged

def test_delete_place(client):
    # Create first
    create_res = client.post(
        "/places/",
        json={
            "name": "Delete Me",
            "category": "Trash",
            "latitude": 0.0,
            "longitude": 0.0,
        },
    )
    place_id = create_res.json()["id"]

    # Delete
    response = client.delete(f"/places/{place_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify deleted
    response = client.get(f"/places/{place_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
