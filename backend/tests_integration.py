import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from database import Base, get_db
from .auth_models import User

# Setup Test DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_integration.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    # Seed a test admin and user
    admin = User(email="admin@transit.com", hashed_password="hashed_password", role="admin")
    user = User(email="user@transit.com", hashed_password="hashed_password", role="user")
    db.add(admin)
    db.add(user)
    db.commit()
    db.close()

def test_auth_flow():
    # Test registration
    reg_res = client.post("/api/auth/register", json={"email": "new@test.com", "password": "password123"})
    assert reg_res.status_code == 200

    # Test login
    login_res = client.post("/api/auth/login", json={"email": "new@test.com", "password": "password123"})
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]

    # Test protected route access
    headers = {"Authorization": f"Bearer {token}"}
    pref_res = client.get("/api/user/preferences", headers=headers)
    assert pref_res.status_code == 200

def test_role_security():
    # Login as standard user
    login_res = client.post("/api/auth/login", json={"email": "user@transit.com", "password": "password123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Attempt to access admin endpoint
    admin_res = client.get("/api/admin/health", headers=headers)
    assert admin_res.status_code == 403 # Forbidden

def test_ai_parse_integration():
    # Test a natural language request (Mocking the AI call internally if necessary)
    # In integration, we check the endpoint pipeline from request -> AI -> DB Resolution
    res = client.post("/api/assistant/parse", params={"user_text": "Go from Central to T Nagar"})
    assert res.status_code == 200
    # Result depends on seeded 'stops' data in the integration DB
