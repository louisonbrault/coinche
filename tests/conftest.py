import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from models.game import Game
from models.user import User  # noqa
from database import Base  # noqa

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    Base.metadata.create_all(bind=engine)
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(name="session")
def session():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        Base.metadata.drop_all(bind=engine)


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def create_user_test(session: Session):
    db_user = User(
        id=1,
        slug_name="toto",
        display_name="toto",
        google_id="123456"
    )
    session.add(db_user)
    session.commit()
    return db_user


def create_admin(session: Session):
    db_user = User(
        id=10,
        slug_name="tyty",
        display_name="tyty",
        role="admin"
    )
    session.add(db_user)
    session.commit()
    return db_user


def create_user_without_fb_test(session: Session):
    db_user = User(
        id=1,
        slug_name="toto",
        display_name="toto"
    )
    session.add(db_user)
    session.commit()
    return db_user


def create_4_users(session: Session):
    a1 = User(id=1, slug_name="toto", display_name="toto")
    a2 = User(id=2, slug_name="tata", display_name="tata", role="viewer")
    b1 = User(id=3, slug_name="titi", display_name="titi")
    b2 = User(id=4, slug_name="tutu", display_name="tutu")
    session.bulk_save_objects([a1, a2, b1, b2])
    session.commit()


def valid_game_data():
    return {
        "date": "2023-06-11",
        "score_a": 1600,
        "score_b": 800,
        "stars_a": 0,
        "stars_b": 1,
        "a_won": True,
        "b_won": False,
        "player_a1_id": 1,
        "player_a2_id": 2,
        "player_b1_id": 3,
        "player_b2_id": 4
    }


def complex_data(session: Session):
    create_4_users(session)
    g1 = Game(score_a=1600, score_b=20, a_won=True, b_won=False, player_a1_id=1, player_a2_id=2, player_b1_id=3,
              player_b2_id=4, creator=1)
    g2 = Game(score_a=1600, score_b=20, a_won=True, b_won=False, player_a1_id=1, player_a2_id=3, player_b1_id=2,
              player_b2_id=4, creator=1)
    g3 = Game(score_a=600, score_b=2220, a_won=False, b_won=True, player_a1_id=4, player_a2_id=2, player_b1_id=3,
              player_b2_id=1, creator=1)
    g4 = Game(score_a=100, score_b=2220, a_won=False, b_won=True, player_a1_id=1, player_a2_id=4, player_b1_id=3,
              player_b2_id=2, creator=1)
    g5 = Game(score_a=1600, score_b=20, a_won=True, b_won=False, player_a1_id=3, player_a2_id=2, player_b1_id=1,
              player_b2_id=4, creator=1)
    session.bulk_save_objects([g1, g2, g3, g4, g5])
    session.commit()
