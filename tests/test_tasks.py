import pytest
import os
from fastapi.testclient import TestClient
from app.main import app
from app.db import get_db_connection, init_db
import sqlite3

TEST_DB = "test_tasks.db"

def override_get_db():
    conn = sqlite3.connect(TEST_DB, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

app.dependency_overrides[get_db_connection] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    """Create a fresh database for every test, then tear it down."""
    # Setup
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()
    
    yield
    
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_task_success():
    payload = {"title": "Finish the portfolio"}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Finish the portfolio"
    assert data["done"] is False
    assert "id" in data
    assert "created_at" in data

def test_create_task_invalid_title():
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 400
    assert "validation error" in response.json()["error"].lower()

    long_title = "a" * 121
    response = client.post("/tasks", json={"title": long_title})
    assert response.status_code == 400

def test_get_list_tasks():
    client.post("/tasks", json={"title": "Task 1"})
    client.post("/tasks", json={"title": "Task 2"})
    
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task 1"

def test_get_task_not_found():
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"error": "Task not found"}

def test_patch_update_task():
    create_res = client.post("/tasks", json={"title": "Old Title"})
    task_id = create_res.json()["id"]
    
    update_res = client.patch(f"/tasks/{task_id}", json={"title": "New Title", "done": True})
    assert update_res.status_code == 200
    assert update_res.json()["title"] == "New Title"
    assert update_res.json()["done"] is True
    
    get_res = client.get(f"/tasks/{task_id}")
    assert get_res.json()["title"] == "New Title"

def test_delete_task():
    create_res = client.post("/tasks", json={"title": "To Delete"})
    task_id = create_res.json()["id"]
    
    del_res = client.delete(f"/tasks/{task_id}")
    assert del_res.status_code == 204
    
    get_res = client.get(f"/tasks/{task_id}")
    assert get_res.status_code == 404