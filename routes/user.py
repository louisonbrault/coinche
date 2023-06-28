from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from crud.user import create_user, get_stats_for_user, get_stats_for_users, list_users
from database import get_db
from schemas.user import User, UserCreate, UserProfile, UserStat
from security.middlewares import has_role

user_router = APIRouter()


@user_router.get("/users", response_model=list[User], tags=["Users"])
def get_users(db: Session = Depends(get_db)):
    return list_users(db=db)


@user_router.get("/users/{user_id}", response_model=UserProfile, tags=["Users"])
def get_profile(user_id: int, db: Session = Depends(get_db)):
    stats = get_stats_for_user(db, user_id)
    if not stats:
        raise HTTPException(status_code=404, detail="User not found")
    return stats


@user_router.get("/stats", response_model=list[UserStat], tags=["Users"])
def get_stats(db: Session = Depends(get_db)):
    return get_stats_for_users(db=db)


@user_router.post("/users", response_model=User, tags=["Users"], responses={
    200: {"description": "User created."},
    400: {"description": "User not created due to errors on request."}
})
@has_role("admin")
def post_users(user: UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(db=db, user=user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="A user with the same slug already exists")
    return user
