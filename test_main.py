from fastapi.testclient import TestClient
from main import app, candidates_db, next_id
import main

client = TestClient(app)


def setup_function():
    """Reset state before each test."""
    candidates_db.clear()
    main.next_id = 1


# --- POST /candidates ---

def test_create_candidate():
    response = client.post("/candidates", json={
        "name": "John Doe",
        "email": "john@example.com",
        "skill": "Python",
        "status": "applied",
    })
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "John Doe"
    assert data["email"] == "john@example.com"
    assert data["skill"] == "Python"
    assert data["status"] == "applied"


def test_create_candidate_invalid_email():
    response = client.post("/candidates", json={
        "name": "Jane",
        "email": "not-an-email",
        "skill": "Java",
        "status": "applied",
    })
    assert response.status_code == 422


def test_create_candidate_invalid_status():
    response = client.post("/candidates", json={
        "name": "Jane",
        "email": "jane@example.com",
        "skill": "Java",
        "status": "hired",
    })
    assert response.status_code == 422


def test_create_candidate_duplicate_email():
    client.post("/candidates", json={
        "name": "John Doe",
        "email": "john@example.com",
        "skill": "Python",
        "status": "applied",
    })
    response = client.post("/candidates", json={
        "name": "John Copy",
        "email": "john@example.com",
        "skill": "Go",
        "status": "applied",
    })
    assert response.status_code == 400


# --- GET /candidates ---

def test_get_all_candidates():
    client.post("/candidates", json={"name": "A", "email": "a@x.com", "skill": "Python", "status": "applied"})
    client.post("/candidates", json={"name": "B", "email": "b@x.com", "skill": "Java", "status": "interview"})
    response = client.get("/candidates")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_candidates_filter_by_status():
    client.post("/candidates", json={"name": "A", "email": "a@x.com", "skill": "Python", "status": "applied"})
    client.post("/candidates", json={"name": "B", "email": "b@x.com", "skill": "Java", "status": "interview"})
    response = client.get("/candidates?status=interview")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["status"] == "interview"


def test_get_candidates_filter_invalid_status():
    response = client.get("/candidates?status=hired")
    assert response.status_code == 422


# --- PUT /candidates/{id}/status ---

def test_update_candidate_status():
    client.post("/candidates", json={"name": "A", "email": "a@x.com", "skill": "Python", "status": "applied"})
    response = client.put("/candidates/1/status", json={"status": "interview"})
    assert response.status_code == 200
    assert response.json()["status"] == "interview"


def test_update_candidate_status_not_found():
    response = client.put("/candidates/999/status", json={"status": "interview"})
    assert response.status_code == 404


def test_update_candidate_status_invalid():
    client.post("/candidates", json={"name": "A", "email": "a@x.com", "skill": "Python", "status": "applied"})
    response = client.put("/candidates/1/status", json={"status": "hired"})
    assert response.status_code == 422
