import uuid
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user():
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    response = client.post("/register", json={
        "username": username,
        "password": "testpass123"
    })
    assert response.status_code == 200

def test_login_user():
    username = f"testuser_{uuid.uuid4().hex[:8]}"
    # First register
    client.post("/register", json={
        "username": username,
        "password": "testpass456"
    })
    # Then login
    response = client.post("/login", json={
        "username": username,
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

def test_create_and_get_task_authenticated():
    username = f"authflowuser_{uuid.uuid4().hex[:8]}"

    # Register a user
    client.post("/register", json={
        "username": username,
        "password": "authflowpass"
    })

    # Log in and grab the token
    login_response = client.post("/login", json={
        "username": username,
        "password": "authflowpass"
    })
    token = login_response.json()  # /login endpoint returns the token directly

    headers = {"Authorization": f"Bearer {token}"}

    # Create a task using the token
    create_response = client.post("/tasks", json={
        "title": "Test task from auth flow",
        "done": False
    }, headers=headers)
    assert create_response.status_code == 200
    task_id = create_response.json()["id"]

    # Fetch the same task back
    get_response = client.get(f"/tasks/{task_id}", headers=headers)
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Test task from auth flow"