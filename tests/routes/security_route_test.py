from fastapi.exceptions import HTTPException
from jose import jwt
import pytest
from sqlalchemy.orm import Session
from unittest.mock import patch

from routes.security import login
from schemas.security import AuthToken

from tests.conftest import create_user_test, create_user_without_fb_test


@patch('routes.security.get_user_info_from_token')
def test_login_facebook_api_down(mock_get_user_info_from_token):
    mock_get_user_info_from_token.side_effect = Exception("Une exception")

    with pytest.raises(HTTPException):
        login(None, None)


@patch('routes.security.get_user_info_from_token')
def test_login_invalid_token(mock_get_user_info_from_token):
    mock_get_user_info_from_token.side_effect = ValueError

    with pytest.raises(HTTPException):
        login(None, None)


@patch('routes.security.get_user_info_from_token')
def test_login_user_known(mock_get_user_info_from_token, session: Session):
    mock_get_user_info_from_token.return_value = {"sub": "123456"}

    create_user_test(session)

    auth_token = AuthToken(authToken="EAAHGObM45HcBAITMoo...")
    access_token = login(auth_token, session)
    token_dict = jwt.decode(access_token.access_token, "None", options={'verify_signature': False})
    assert token_dict.get("user_id") == 1
    assert token_dict.get("display_name") == "toto"


@patch('routes.security.get_user_info_from_token')
def test_login_user_unknown_with_same_slug(mock_get_user_info_from_token, session: Session):
    mock_get_user_info_from_token.return_value = {"sub": "123456", "name": "toto"}

    create_user_without_fb_test(session)

    auth_token = AuthToken(authToken="EAAHGObM45HcBAITMoo...")
    access_token = login(auth_token, session)
    token_dict = jwt.decode(access_token.access_token, "None", options={'verify_signature': False})
    assert token_dict.get("user_id") == 1
    assert token_dict.get("display_name") == "toto"


@patch('routes.security.get_user_info_from_token')
def test_login_user_totaly_unknown(mock_get_user_info_from_token, session: Session):
    mock_get_user_info_from_token.return_value = {"sub": "123456", "name": "tata"}

    create_user_without_fb_test(session)

    auth_token = AuthToken(authToken="EAAHGObM45HcBAITMoo...")
    access_token = login(auth_token, session)
    token_dict = jwt.decode(access_token.access_token, "None", options={'verify_signature': False})
    assert token_dict.get("user_id") == 2
    assert token_dict.get("display_name") == "tata"
