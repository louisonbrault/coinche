from datetime import datetime, timedelta
import logging
from os import environ
import traceback

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from jose import jwt
from slugify import slugify
from sqlalchemy.orm import Session

from crud.user import create_user, get_user_from_facebook_id, get_user_from_slug_name, update_user
from database import get_db
from schemas.security import AccessToken, AuthToken, HTTPError
from schemas.user import UserCreate

from security.facebook import \
    TokenInvalidException, \
    get_facebook_access_token, \
    get_facebook_id_from_auth_token, \
    get_facebook_name_from_facebook_id


security_router = APIRouter()

# Configuration du secret JWT
load_dotenv()
SECRET_KEY = environ.get("SECRET_KEY")
ALGORITHM = environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", "180")


# Fonction de génération du JWT
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=60)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Route de login pour générer le JWT et stocker le cookie de session
@security_router.post("/login", tags=["Auth"], responses={
    200: {"model": AccessToken},
    400: {
        "model": HTTPError,
        "description": "Auth token provided is invalid",
    },
    503: {
        "model": HTTPError,
        "description": "Impossible to get info from facebook",
    },
})
def login(authToken: AuthToken, db: Session = Depends(get_db)) -> AccessToken:
    try:
        access_token = get_facebook_access_token()
        user_facebook_id = get_facebook_id_from_auth_token(access_token, authToken.authToken)
    except TokenInvalidException:
        raise HTTPException(400, detail="Auth token provided is invalid")
    except Exception as e:
        logging.error(traceback.format_exception(e))
        raise HTTPException(503, detail="Impossible to get info from facebook")

    # On recherche dans la db si un utilisateur correspond à l'id facebook
    user = get_user_from_facebook_id(db, user_facebook_id)

    if not user:
        name = get_facebook_name_from_facebook_id(access_token, user_facebook_id)

        # On cherche si un utilisateur avec le même slugname existe déjà
        user = get_user_from_slug_name(db, slugify(name))

        # Si oui, on met à jour son id facebook
        if user:
            user.facebook_id = user_facebook_id
            update_user(db, user)
        # Si non, on le créé
        else:
            user_create = UserCreate(display_name=name, facebook_id=user_facebook_id)
            user = create_user(db, user_create)

    # L'authentification est réussie
    user = {"user_id": user.id, "display_name": user.display_name, "role": user.role}

    # Génération du JWT
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(user, expires_delta=access_token_expires)

    return AccessToken(access_token=access_token, expires=access_token_expires.total_seconds())
