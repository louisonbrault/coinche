from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.conftest import override_get_db
from database import get_db
from main import app

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_get_profile(session: Session):
    response = client.get("/users/1")
    assert response.status_code == 404
