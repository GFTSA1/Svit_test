import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

from main import app
from models import LogEntry, User
from database import get_db, Base
from datetime import datetime

TEST_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

client = TestClient(app)


def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def setup_db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    db = TestSessionLocal()
    yield db
    db.close()


def test_upload_file_success(setup_db):
    file_content = b"Test log content"
    files = {"file": ("test_log.txt", file_content)}

    response = client.post("/upload", files=files)

    assert response.status_code == 200
    assert response.json()["filename"] == "test_log.txt"
    assert response.json()["content"] == "Test log content"

    assert os.path.exists("logs/test_log.txt")


def test_upload_file_conflict(setup_db):
    file_content = b"Test log content"
    files = {"file": ("test_log.txt", file_content)}

    client.post("/upload", files=files)

    response = client.post("/upload", files=files)

    assert response.status_code == 409
    assert response.json()["detail"] == "The file with the same name already exists"


def get_auth_token():
    response_token = client.post(
        "/login", json={"username": "test_user", "password": "1254"}
    )
    assert response_token.status_code == 200
    print(response_token.json())
    return f"Bearer {response_token.json()['access_token']}"


def test_get_logs(setup_db):
    db = setup_db
    test_log = LogEntry(
        filename="test_log.txt", content="Sample log entry", timestamp=datetime.utcnow()
    )
    db.add(test_log)
    db.commit()

    response = client.get("/logs")

    assert response.status_code == 401
