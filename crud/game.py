
from sqlalchemy import or_
from sqlalchemy.orm import Session

from models.game import Game as GameModel
from schemas.game import GameCreate


def list_games(db: Session, user_id: int = None, skip: int = 0, limit: int = 100):
    query = db.query(GameModel).order_by(GameModel.date.desc(), GameModel.id.desc()).offset(skip).limit(limit)
    if user_id:
        query = query.filter(or_(
            GameModel.player_a1 == user_id,
            GameModel.player_a2 == user_id,
            GameModel.player_b1 == user_id,
            GameModel.player_b2 == user_id,
        ))
    return query.all()


def create_game(db: Session, game: GameCreate, creator_id: int):
    db_game = GameModel(**game.dict(), creator=creator_id)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game
