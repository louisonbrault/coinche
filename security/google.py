import logging
from os import environ

from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv

load_dotenv()


def get_user_info_from_token(access_token: str) -> str:
    try:
        return id_token.verify_oauth2_token(access_token, requests.Request(), environ.get("GOOGLE_APP_ID"))
    except ValueError as e:
        logging.error(e)
