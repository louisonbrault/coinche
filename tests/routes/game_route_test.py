from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import pytest

from tests.conftest import \
    complex_data, create_admin, create_user_test, create_4_users, override_get_db, valid_game_data
from database import get_db
from main import app
from routes.security import create_access_token

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_filter_by_user(session: Session):
    complex_data(session)
    response = client.get("/games?user_id=2")
    assert response.json().get("total") == 5


def test_filter_by_creator(session: Session):
    complex_data(session)
    response = client.get("/games?creator_id=2")
    assert response.json().get("total") == 0


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


def test_update_game_404(session: Session):
    create_user_test(session)
    jwt = create_access_token({"user_id": 1})
    response = client.put("/games/1", headers={"Authorization": f"Bearer {jwt}"}, json=valid_game_data())
    assert response.status_code == 404


def test_update_game_403(session: Session):
    complex_data(session)
    jwt = create_access_token({"user_id": 2})
    response = client.put("/games/1", headers={"Authorization": f"Bearer {jwt}"}, json=valid_game_data())
    assert response.status_code == 403


def test_update_game_admin(session: Session):
    complex_data(session)
    create_admin(session)
    jwt = create_access_token({"user_id": 10})
    response = client.put("/games/1", headers={"Authorization": f"Bearer {jwt}"}, json=valid_game_data())
    assert response.status_code == 200
    assert response.json().get("score_b") == 800


def test_get_game_404():
    response = client.get("/games/1")
    assert response.status_code == 404


def test_get_game(session: Session):
    complex_data(session)
    response = client.get("/games/1")
    assert response.status_code == 200
    assert response.json().get("score_a") == 1600


def test_delete_game_404(session: Session):
    create_user_test(session)
    jwt = create_access_token({"user_id": 1})
    response = client.delete("/games/1", headers={"Authorization": f"Bearer {jwt}"})
    assert response.status_code == 404


def test_delete_game_403(session: Session):
    complex_data(session)
    jwt = create_access_token({"user_id": 2})
    response = client.delete("/games/1", headers={"Authorization": f"Bearer {jwt}"})
    assert response.status_code == 403


def test_delete_game_admin(session: Session):
    complex_data(session)
    create_admin(session)
    jwt = create_access_token({"user_id": 10})
    response = client.delete("/games/1", headers={"Authorization": f"Bearer {jwt}"})
    assert response.status_code == 200
    response = client.get("/games")
    assert response.json().get("total") == 4
