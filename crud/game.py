from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import or_
from sqlalchemy.orm import Session

from models.game import Game as GameModel
from schemas.game import GameCreate


def list_games(db: Session, user_id: int = None, creator_id: int = None):
    query = db.query(GameModel).order_by(GameModel.date.desc(), GameModel.id.desc())
    if user_id:
        query = query.filter(or_(
            GameModel.player_a1_id == user_id,
            GameModel.player_a2_id == user_id,
            GameModel.player_b1_id == user_id,
            GameModel.player_b2_id == user_id,
        ))
    if creator_id:
        query = query.filter(GameModel.creator == creator_id)
    return paginate(query)


def get_game_from_id(db: Session, game_id: int) -> GameModel:
    return db.get(GameModel, game_id)


def create_game(db: Session, game: GameCreate, creator_id: int):
    db_game = GameModel(**game.dict(), creator=creator_id)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def update_game(db: Session, game: GameModel) -> GameModel:
    db.merge(game)
    db.commit()
    db.refresh(game)
    return game
