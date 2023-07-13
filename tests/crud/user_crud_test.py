import pytest
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from crud.game import create_game
from crud.user import delete_user, get_stats_for_user, get_stats_for_users, get_user_from_id, list_users
from schemas.game import GameCreate
from tests.conftest import complex_data, create_4_users, create_admin, create_user_test, valid_game_data


def test_get_stats_for_user(session: Session):
    complex_data(session)
    stats_for_user_1 = get_stats_for_user(session, 1)
    assert stats_for_user_1.id == 1
    assert stats_for_user_1.display_name == "toto"
    assert stats_for_user_1.games == 5
    assert stats_for_user_1.wins == 3
    assert stats_for_user_1.stars == 0
    assert stats_for_user_1.best_teammate == "titi"
    assert stats_for_user_1.teammate_times == 2
    assert stats_for_user_1.best_opponent == "tata"
    assert stats_for_user_1.oppositions == 4
    assert stats_for_user_1.best_target == "tutu"
    assert stats_for_user_1.victories == 3
    assert stats_for_user_1.executioner == "tata"
    assert stats_for_user_1.defeats == 2


def test_get_stat_for_user_no_games(session: Session):
    create_user_test(session)
    stats = get_stats_for_user(session, 1)
    assert stats.id == 1
    assert stats.display_name == "toto"
    assert stats.games == 0


def test_get_stats_for_users(session: Session):
    complex_data(session)
    stats = get_stats_for_users(session)
    assert stats[0].id == 3
    assert stats[0].display_name == "titi"
    assert stats[0].wins == 4
    assert stats[0].games == 5
    assert stats[0].stars == 0


def test_delete_user(session: Session):
    user = create_user_test(session)
    delete_user(session, user)
    assert len(list_users(session)) == 0


def test_delete_user_with_games(session: Session):
    complex_data(session)
    user = get_user_from_id(session, 1)
    with pytest.raises(IntegrityError):
        delete_user(session, user)
        assert len(list_users(session)) == 4


def test_delete_creator(session: Session):
    admin = create_admin(session)
    create_4_users(session)
    create_game(session, GameCreate(**valid_game_data()), 10)
    with pytest.raises(IntegrityError):
        delete_user(session, admin)
        assert len(list_users(session)) == 5
