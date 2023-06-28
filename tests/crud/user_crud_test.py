from sqlalchemy.orm import Session

from crud.user import get_stats_for_user, get_stats_for_users
from tests.conftest import complex_data, create_user_test


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
