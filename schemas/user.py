from datetime import date

from pydantic import BaseModel


class UserBase(BaseModel):
    display_name: str
    facebook_id: str = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    creation_date: date
    slug_name: str

    class Config:
        orm_mode = True


class UserLight(BaseModel):
    id: int
    display_name: str

    class Config:
        orm_mode = True


class UserStat(BaseModel):
    id: int
    display_name: str
    games: int
    wins: int
    stars: int


class UserProfile(UserStat):
    best_teammate: str
    teammate_times: int
    best_opponent: str
    oppositions: int
    best_target: str
    victories: int
    executioner: str
    defeats: int
