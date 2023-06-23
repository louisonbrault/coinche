from os import environ

from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt
from sqlalchemy.orm import Session

from crud.user import get_user_from_id
from database import get_db
from models.user import User
from schemas.game import GameCreate


load_dotenv()
SECRET_KEY = environ.get("SECRET_KEY")
ALGORITHM = environ.get("ALGORITHM", "HS256")

security = HTTPBearer()


async def authenticate(token: str = Depends(security), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user = get_user_from_id(db, payload.get("user_id"))
        return user
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def has_role(role: str):
    def decorator(func):
        async def wrapper(game_data: GameCreate, user=Depends(authenticate), db: Session = Depends(get_db)):
            if user.role != role and user.role != "admin":
                raise HTTPException(status_code=403, detail="Access denied")
            return func(user, game_data, db)
        return wrapper
    return decorator
