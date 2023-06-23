from os import environ
import requests

from dotenv import load_dotenv

load_dotenv()


class TokenInvalidException(Exception):
    pass


def get_facebook_access_token() -> str:
    client_id = environ.get("FACEBOOK_APP_ID")
    client_secret = environ.get("FACEBOOK_APP_SECRET")
    base_url = "https://graph.facebook.com/oauth/access_token"
    url = f"{base_url}?client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials"

    response = requests.get(url)
    return response.json().get("access_token")


def get_facebook_id_from_auth_token(access_token: str, auth_token: str) -> str:
    url = f"https://graph.facebook.com/v17.0/debug_token?input_token={auth_token}"

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers).json().get("data")

    if not response.get("is_valid"):
        raise TokenInvalidException("The token provided is invalid")

    return response.get("user_id")


def get_facebook_name_from_facebook_id(access_token: str, facebook_id: str) -> str:
    url = f"https://graph.facebook.com/v17.0/{facebook_id}/"

    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, headers=headers).json()

    return response.get("name")
