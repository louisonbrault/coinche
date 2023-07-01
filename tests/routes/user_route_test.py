from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from tests.conftest import override_get_db
from database import get_db
from main import app
from routes.security import create_access_token
from tests.conftest import create_4_users, create_admin, create_user_test

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_get_profile(session: Session):
    response = client.get("/users/1")
    assert response.status_code == 404


def test_update_user_no_auth(session: Session):
    response = client.put("/users/1")
    assert response.status_code == 403


def test_update_user_that_not_exists(session: Session):
    create_user_test(session)
    jwt = create_access_token({"user_id": 1})
    response = client.put("/users/2", headers={"Authorization": f"Bearer {jwt}"}, json={"google_id": 0})
    assert response.status_code == 404


def test_update_user_without_right(session: Session):
    create_4_users(session)
    jwt = create_access_token({"user_id": 1})
    response = client.put("/users/2", headers={"Authorization": f"Bearer {jwt}"}, json={"google_id": 0})
    assert response.status_code == 403


def test_update_user_modify_role(session: Session):
    create_4_users(session)
    jwt = create_access_token({"user_id": 1})
    response = client.put("/users/1", headers={"Authorization": f"Bearer {jwt}"}, json={"role": "admin"})
    assert response.status_code == 403


def test_update_user(session: Session):
    create_4_users(session)
    jwt = create_access_token({"user_id": 1})
    response = client.put("/users/1", headers={"Authorization": f"Bearer {jwt}"}, json={"display_name": "Jean Michel"})
    assert response.status_code == 200
    assert response.json().get("display_name") == "Jean Michel"


def test_update_user_admin(session: Session):
    create_4_users(session)
    create_admin(session)
    jwt = create_access_token({"user_id": 10})
    response = client.put("/users/2", headers={"Authorization": f"Bearer {jwt}"}, json={"google_id": 0})
    assert response.status_code == 200
    assert response.json().get("google_id") == "0"
