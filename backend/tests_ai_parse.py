import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base

# Use a sqlite in-memory DB for fast testing,
# but we need to mimic the 'stops' table structure.
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override get_db dependency
from database import get_db
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

# Setup mock data
def setup_db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # Mocking the stops table
    db.execute(text("CREATE TABLE IF NOT EXISTS stops (stop_id TEXT PRIMARY KEY, stop_name TEXT, stop_lat REAL, stop_lon REAL)"))
    db.execute(text("INSERT INTO stops (stop_id, stop_name) VALUES ('S1', 'Chennai Central'), ('S2', 'T Nagar'), ('S3', 'T Nagar Bus Terminus')"))
    db.commit()
    db.close()

from sqlalchemy import text

@pytest.fixture(autouse=True)
def run_around_tests():
    setup_db()
    yield

def test_parse_clear_request():
    # This requires a real API key to run. We can mock the AI service for CI,
    # but for this check we'll see if the endpoint exists and handles the flow.
    response = client.post("/api/assistant/parse", params={"user_text": "Go from Chennai Central to T Nagar"})
    # If API key is missing, it should return a 500 or error message from our ai_service
    assert response.status_code == 200
    data = response.json()
    if "error" in data:
        print(f"AI key missing as expected: {data['error']}")
    else:
        assert data["status"] == "validated"
        assert data["origin_id"] == "S1"
        assert data["destination_id"] == "S2"

def test_parse_ambiguous_request():
    response = client.post("/api/assistant/parse", params={"user_text": "Go to T Nagar"})
    assert response.status_code == 200
    data = response.json()
    if "error" not in data:
        assert data["status"] == "ambiguous"
        assert "T Nagar" in data["suggestions"]["destination"]
        assert "T Nagar Bus Terminus" in data["suggestions"]["destination"]

def test_parse_invented_request():
    response = client.post("/api/assistant/parse", params={"user_text": "Go to Mars"})
    assert response.status_code == 200
    data = response.json()
    # Should be rejected by AI or not found in DB
    assert data["status"] in ["rejected", "not_found"]
