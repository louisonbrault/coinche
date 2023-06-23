from slugify import slugify
from sqlalchemy import case, desc, func, or_
from sqlalchemy.orm import Session, Query

from models.game import Game
from models.user import User
from schemas.user import UserCreate, UserProfile, UserStat


def list_users(db: Session):
    return db.query(User).all()


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        display_name=user.display_name,
        facebook_id=user.facebook_id,
        slug_name=slugify(user.display_name)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: User) -> User:
    db.merge(user)
    db.commit()
    db.refresh(user)
    return user


def get_user_from_id(db: Session, user_id: int) -> User:
    return db.get(User, user_id)


def get_user_from_facebook_id(db: Session, facebook_id: str) -> User:
    return db.query(User).filter(User.facebook_id == facebook_id).first()


def get_user_from_slug_name(db: Session, slug_name: str) -> User:
    return db.query(User).filter(User.slug_name == slug_name).first()


def get_stats_for_user(db: Session, user_id: int):
    teammate_query = func.sum(
        case(
            (user_id == Game.player_a1_id, case((Game.player_a2_id == User.id, 1), else_=0)),
            (user_id == Game.player_a2_id, case((Game.player_a1_id == User.id, 1), else_=0)),
            (user_id == Game.player_b1_id, case((Game.player_b2_id == User.id, 1), else_=0)),
            (user_id == Game.player_b2_id, case((Game.player_b1_id == User.id, 1), else_=0))
        )
    ).label("teammate")
    opponent_query = func.sum(
        case(
            (user_id == Game.player_a1_id, case((Game.player_a2_id != User.id, 1), else_=0)),
            (user_id == Game.player_a2_id, case((Game.player_a1_id != User.id, 1), else_=0)),
            (user_id == Game.player_b1_id, case((Game.player_b2_id != User.id, 1), else_=0)),
            (user_id == Game.player_b2_id, case((Game.player_b1_id != User.id, 1), else_=0))
        )
    ).label("opponent")
    wins_query = func.sum(
        case(
            (user_id == Game.player_a1_id,
             case((Game.player_a2_id != User.id, case((Game.a_won, 1), else_=0)), else_=0)),
            (user_id == Game.player_a2_id,
             case((Game.player_a1_id != User.id, case((Game.a_won, 1), else_=0)), else_=0)),
            (user_id == Game.player_b1_id,
             case((Game.player_b2_id != User.id, case((Game.b_won, 1), else_=0)), else_=0)),
            (
                user_id == Game.player_b2_id,
                case((Game.player_b1_id != User.id, case((Game.b_won, 1), else_=0)), else_=0))
        )
    ).label("wins")
    query = (db.query(
        User.id,
        User.display_name,
        teammate_query,
        opponent_query,
        wins_query,
        (opponent_query - wins_query).label("defeats")
    )
     .filter(User.id != user_id)
     .filter(or_(Game.player_a1_id == user_id,
                 Game.player_a2_id == user_id,
                 Game.player_b1_id == user_id,
                 Game.player_b2_id == user_id,
                 ))
     .filter(or_(
                Game.player_a1_id == User.id,
                Game.player_a2_id == User.id,
                Game.player_b1_id == User.id,
                Game.player_b2_id == User.id,
                ))
     .group_by(User.id)
     .group_by(User.display_name)
     )
    teammate = query.order_by(teammate_query.desc()).first()
    opponent = query.order_by(opponent_query.desc()).first()
    target = query.order_by(wins_query.desc()).first()
    executioner = query.order_by(desc("defeats")).first()
    simple_stats = get_simple_stat_query(db).filter(User.id == user_id).first()
    return UserProfile(
        id=simple_stats.id,
        display_name=simple_stats.display_name,
        wins=simple_stats.wins,
        games=simple_stats.games,
        stars=simple_stats.stars,
        best_teammate=teammate.display_name,
        teammate_times=teammate.teammate,
        best_opponent=opponent.display_name,
        oppositions=opponent.opponent,
        best_target=target.display_name,
        victories=target.wins,
        executioner=executioner.display_name,
        defeats=executioner.defeats
    )


def get_stats_for_users(db: Session) -> list[UserStat]:
    query = get_simple_stat_query(db)
    users = query.all()
    response = []
    for user in users:
        response.append(
            UserStat(id=user.id, display_name=user.display_name, wins=user.wins, games=user.games, stars=user.stars))
    return response


def get_simple_stat_query(db: Session) -> Query:
    wins = func.sum(
        case(
            (User.id == Game.player_a1_id, case((Game.a_won, 1), else_=0)),
            (User.id == Game.player_a2_id, case((Game.a_won, 1), else_=0)),
            else_=case((Game.b_won, 1), else_=0)
        )
    ).label("wins")
    stars = func.sum(
        case(
            (User.id == Game.player_a1_id, Game.stars_a),
            (User.id == Game.player_a2_id, Game.stars_a),
            else_=Game.stars_b
        )
    ).label("stars")
    query = (db.query(
        User.id,
        User.display_name,
        func.count(Game.id).label("games"),
        wins,
        stars
    ).filter(or_(
        Game.player_a1_id == User.id,
        Game.player_a2_id == User.id,
        Game.player_b1_id == User.id,
        Game.player_b2_id == User.id,
    )).group_by(User.id)
             .group_by(User.display_name)
             .order_by(wins.desc())
             )
    return query
