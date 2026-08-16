from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/register", json={
        "username": "testuser123",
        "password": "testpass123"
    })
    assert response.status_code == 200

def test_login_user():
    # First register
    client.post("/register", json={
        "username": "testuser456",
        "password": "testpass456"
    })
    # Then login
    response = client.post("/login", json={
        "username": "testuser456",
        "password": "testpass456"
    })
    assert response.status_code == 200

def test_get_tasks_unauthorized():
    response = client.get("/tasks")
    assert response.status_code == 401

def test_invalid_login():
    response = client.post("/login", json={
        "username": "wronguser",
        "password": "wrongpass"
    })
    assert response.status_code == 401