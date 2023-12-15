import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, false
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db, TestingSessionLocal

TEST_POSTGRES_DATABASE_URL = "postgresql://postgres:root@localhost/note_db"

# Create engines for PostgreSQL and SQLite databases
postgres_engine = create_engine(TEST_POSTGRES_DATABASE_URL)

# Create testing SessionLocals for PostgreSQL and SQLite
TestingSessionLocalPostgres = sessionmaker(
    autocommit=False, autoflush=False, bind=postgres_engine)


@pytest.fixture(scope="function")
def test_app():
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    return client


def override_get_db():
    db = TestingSessionLocalPostgres()
    try:
        yield db
    finally:
        db.close()

# Test cases for create_note_endpoint


def test_create_note_success(test_app):
    response = test_app.post("/notes/", json={
        "title": "This is a demo",
        "desc": "This is a demo description",
        "important": False
    })
    assert response.status_code == 200
    assert "id" in response.json()

# Unsuccessful test case for create_note_endpoint


def test_create_note_failure(test_app):
    # Sending a request without the required data (title)
    response = test_app.post("/notes/", json={
        "desc": "This is a demo description",
        "important": False
    })
    # 422 Unprocessable Entity for validation failure
    assert response.status_code == 422

# Successful test case for read_note_endpoint


def test_read_note_success(test_app):
    response = test_app.get("/notes/1")
    assert response.status_code == 200
    assert "title" in response.json()
    assert "desc" in response.json()
    assert "important" in response.json()

# Unsuccessful test case for read_note_endpoint


def test_read_note_failure(test_app):
    # Requesting a note that doesn't exist (e.g., note with id=999)
    response = test_app.get("/notes/999")
    assert response.status_code == 404


# Successful test case for update_note_endpoint
def test_update_note_success(test_app):
    test_note_id = 1
    response = test_app.put(f"/notes/update/?note_id={test_note_id}", json={
        "title": "Updated Title",
        "desc": "Updated Description",
        "important": False
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["desc"] == "Updated Description"
    assert response.json()["important"] is False

# Unsuccessful test case for update_note_endpoint


def test_update_note_failure(test_app):
    non_existing_note_id = 999
    response = test_app.put(f"/notes/update/?note_id={non_existing_note_id}", json={
        "title": "Updated Title",
        "desc": "Updated Description",
        "important": False
    })
    assert response.status_code == 404  # 404 Not Found for resource not found
    assert response.json() == {"detail": "Note not found"}

    existing_note_id = 1
    response = test_app.put(f"/notes/update/?note_id={existing_note_id}", json={
        "desc": "Updated Description",
        "important": False
    })
    assert response.status_code == 422

# Successful test case for delete_note_endpoint


def test_delete_note_success(test_app):
    test_note_id = 1
    response = test_app.delete(f"/notes/delete/?note_id={test_note_id}")
    assert response.status_code == 200
    assert response.json()["id"] == test_note_id

# Update the test_delete_note_failure test case


def test_delete_note_failure(test_app):
    non_existing_note_id = 999
    response = test_app.delete(
        f"/notes/delete/?note_id={non_existing_note_id}")
    assert response.status_code == 404  # 404 Not Found for resource not found
    assert response.json() == {"detail": "Note not found"}
