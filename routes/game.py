from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from crud.game import create_game, list_games
from database import get_db
from models.user import User
from schemas.game import Game, GameCreate, GameUserInfo
from security.middlewares import has_role

game_router = APIRouter()


@game_router.get("/games", response_model=list[GameUserInfo], tags=["Games"])
def get_games(user_id: int = None, skip: int = None, limit: int = None, db: Session = Depends(get_db)):
    games = list_games(db, user_id=user_id, skip=skip, limit=limit)
    return games


@game_router.post("/games", response_model=Game, tags=["Games"], responses={
    200: {"description": "Game created."},
    400: {"description": "Game not created due to errors on request."}
})
@has_role("writer")
def post_games(user: User, game_data: GameCreate, db: Session = Depends(get_db)):
    try:
        game = create_game(db, game=game_data, creator_id=user.id)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Integrity error on players")
    return game
