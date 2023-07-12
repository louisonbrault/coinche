from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from crud.game import create_game, delete_game, get_game_from_id, list_games, update_game
from database import get_db
from models.user import User
from schemas.game import Game, GameCreate, GameUserInfo
from security.middlewares import authenticate, has_role

game_router = APIRouter()


@game_router.get("/games", response_model=Page[GameUserInfo], tags=["Games"])
def get_games(
        user_id: int = Query(None, description="Get all games the player has participated in"),
        creator_id: int = Query(None, description="Get all games created by the user"),
        db: Session = Depends(get_db)
):
    games = list_games(db, user_id=user_id, creator_id=creator_id)
    return games


@game_router.get("/games/{game_id}", response_model=GameUserInfo, tags=["Games"])
def get_game(game_id: int, db: Session = Depends(get_db)):
    game_in_db = get_game_from_id(db, game_id)
    if not game_in_db:
        raise HTTPException(status_code=404, detail="Game not found")
    return game_in_db


@game_router.put("/games/{game_id}", response_model=GameUserInfo, tags=["Games"])
def modify_games(
        game_id: int,
        game_data: GameCreate,
        logged_in_user: User = Depends(authenticate),
        db: Session = Depends(get_db)
):
    game_in_db = get_game_from_id(db, game_id)
    if not game_in_db:
        raise HTTPException(status_code=404, detail="Game not found")
    if logged_in_user.role != "admin" and logged_in_user.id != game_in_db.creator:
        raise HTTPException(status_code=403, detail="You can't modify this game")
    new_attributes = game_data.dict(exclude_none=True)
    for attr in new_attributes.keys():
        setattr(game_in_db, attr, new_attributes.get(attr))
    return update_game(db, game_in_db)


@game_router.delete("/games/{game_id}", tags=["Games"])
def remove_game(game_id: int, logged_in_user: User = Depends(authenticate), db: Session = Depends(get_db)):
    game_in_db = get_game_from_id(db, game_id)
    if not game_in_db:
        raise HTTPException(status_code=404, detail="Game not found")
    if logged_in_user.role != "admin" and logged_in_user.id != game_in_db.creator:
        raise HTTPException(status_code=403, detail="You can't delete this game")
    return delete_game(db, game_in_db)


@game_router.post("/games", response_model=Game, tags=["Games"], responses={
    200: {"description": "Game created."},
    400: {"description": "Game not created due to errors on request."}
})
def post_games(game_data: GameCreate, user: User = Depends(authenticate), db: Session = Depends(get_db)):
    has_role("writer", user)
    try:
        game = create_game(db, game=game_data, creator_id=user.id)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Integrity error on players")
    return game
