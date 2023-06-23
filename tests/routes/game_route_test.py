from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest

from tests.conftest import create_4_users, override_get_db, valid_game_data
from database import get_db
from main import app
from routes.security import create_access_token

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_game_without_bearer(session: Session):
    create_4_users(session)
    body = valid_game_data()
    response = client.post("/games", json=body)
    assert response.status_code == 403


test_data = [
    (create_access_token({"user_id": 1}), 200),  # Cas nominal 1
    ("invalid token", 401),  # Token invalide
    (create_access_token({"user_id": 2}), 403),  # Droits insufisants
]


@pytest.mark.parametrize("jwt, response_code", test_data)
def test_create_game(session: Session, jwt: str, response_code: int):
    create_4_users(session)
    body = valid_game_data()
    response = client.post("/games", headers={"Authorization": f"Bearer {jwt}"}, json=body)
    assert response.status_code == response_code
