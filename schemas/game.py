from datetime import date

from pydantic import BaseModel, Field, root_validator

from .user import UserLight


class GameBase(BaseModel):
    date: date
    score_a: int = Field(ge=0)
    score_b: int = Field(ge=0)
    stars_a: int = Field(ge=0, le=4)
    stars_b: int = Field(ge=0, le=4)
    a_won: bool
    b_won: bool


def check_winning_conditions(score_winner: int, stars_winner: int, score_loser: int, stars_loser: int):
    if stars_loser >= 3 > stars_winner:
        return
    if score_loser > score_winner:
        raise ValueError("Winner can't win with less points than loser")
    if score_winner < 1500 and stars_loser < 3:
        raise ValueError("Winner can't win with less than 1500 points")
    if stars_winner >= 3:
        raise ValueError("Winner can't win with 3 stars")


class GameCreate(GameBase):
    player_a1_id: int
    player_a2_id: int
    player_b1_id: int
    player_b2_id: int

    @root_validator
    def validate_players(cls, values):
        players = [values['player_a1_id'], values['player_a2_id'], values['player_b1_id'], values['player_b2_id']]
        has_duplicates = len(players) != len(set(players))
        if has_duplicates:
            raise ValueError('All players must be different')

        return values

    @root_validator
    def validate_winner(cls, values):
        if values['a_won'] == values['b_won']:
            raise ValueError("a_won and b_won can't be equal")
        if values['a_won']:
            check_winning_conditions(values['score_a'], values['stars_a'], values['score_b'], values['stars_b'])
        else:
            check_winning_conditions(values['score_b'], values['stars_b'], values['score_a'], values['stars_a'])
        return values


class Game(GameBase):
    id: int
    creator: int
    player_a1_id: int
    player_a2_id: int
    player_b1_id: int
    player_b2_id: int

    class Config:
        orm_mode = True


class GameUserInfo(GameBase):
    id: int
    creator: int
    player_a1: UserLight
    player_a2: UserLight
    player_b1: UserLight
    player_b2: UserLight

    class Config:
        orm_mode = True
