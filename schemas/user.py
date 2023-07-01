from datetime import date
from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    display_name: str
    google_id: str = None
    role: str = "writer"


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    display_name: Optional[str]
    google_id: Optional[str]
    role: Optional[str]


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
