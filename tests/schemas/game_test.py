from datetime import date

import pytest

from schemas.game import GameCreate

# Données de test
test_data = [
    (True, 1560, 1, False, 60, 0, True),  # Cas nominal 1
    (True, 120, 1, False, 1560, 3, True),  # Cas nominal 2
    (True, 1560, 1, True, 60, 0, False),  # Les deux équipes ont gangé
    (True, 1560, 3, False, 60, 0, False),  # L'équipe A a trois étoiles
    (False, 1560, 1, True, 60, 0, False),  # L'équipe B a moins de point que A
    (False, 1560, 1, True, 1530, 0, False),  # L'équipe B a moins de point que A
    (False, 0, 4, True, 0, 4, False),  # Les deux équipes on 3 étoiles
]


# Définition du test paramétré
@pytest.mark.parametrize("a_won, score_a, stars_a, b_won, score_b, stars_b, valid_data", test_data)
def test_winning_conditions(a_won, score_a, stars_a, b_won, score_b, stars_b, valid_data):
    error_thrown = False
    try:
        data = {
            "date": date.today(),
            "creator": 1,
            "player_a1_id": 1,
            "player_a2_id": 2,
            "player_b1_id": 3,
            "player_b2_id": 4,
            "score_a": score_a,
            "score_b": score_b,
            "stars_a": stars_a,
            "stars_b": stars_b,
            "a_won": a_won,
            "b_won": b_won,
        }
        GameCreate(**data)
    except Exception as e:
        error_thrown = True
        print(e)
    assert error_thrown != valid_data
