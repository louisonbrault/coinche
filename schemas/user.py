from datetime import date

from pydantic import BaseModel


class UserBase(BaseModel):
    display_name: str
    facebook_id: str = None
    role: str = "writer"


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
    games: int = 0
    wins: int = 0
    stars: int = 0


class UserProfile(UserStat):
    best_teammate: str = None
    teammate_times: int = 0
    best_opponent: str = None
    oppositions: int = 0
    best_target: str = None
    victories: int = 0
    executioner: str = None
    defeats: int = 0
