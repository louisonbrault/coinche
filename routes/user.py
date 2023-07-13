from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from crud.user import \
    create_user, \
    delete_user, \
    get_stats_for_user, \
    get_stats_for_users, \
    get_user_from_id, \
    list_users, \
    update_user
from database import get_db
from schemas.user import User, UserCreate, UserProfile, UserStat, UserUpdate
from security.middlewares import authenticate, has_role

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


@user_router.put("/users/{user_id}", response_model=User, tags=["Users"])
def modify_user(
        user_id: int, user: UserUpdate, logged_in_user: User = Depends(authenticate), db: Session = Depends(get_db)):
    user_in_db = get_user_from_id(db, user_id)
    if not user_in_db:
        raise HTTPException(status_code=404, detail="User not found")
    if logged_in_user.role != "admin" and logged_in_user.id != user_in_db.id:
        raise HTTPException(status_code=403, detail="You can't modify this user")
    if logged_in_user.role != "admin" and user.role:
        raise HTTPException(status_code=403, detail="You can't change this user's rights")
    new_attributes = user.dict(exclude_none=True)
    for attr in new_attributes.keys():
        setattr(user_in_db, attr, new_attributes.get(attr))
    return update_user(db, user_in_db)


@user_router.delete("/users/{user_id}", tags=["Users"], responses={
    200: {"description": "User deleted."},
    400: {"description": "This user participates in games"}})
def remove_user(user_id: int, logged_in_user: User = Depends(authenticate), db: Session = Depends(get_db)):
    user_in_db = get_user_from_id(db, user_id)
    if not user_in_db:
        raise HTTPException(status_code=404, detail="User not found")
    if logged_in_user.role != "admin":
        raise HTTPException(status_code=403, detail="You can't delete this user")
    try:
        delete_user(db, user_in_db)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="This user participates in games")
    return {}


@user_router.get("/stats", response_model=list[UserStat], tags=["Users"])
def get_stats(db: Session = Depends(get_db)):
    return get_stats_for_users(db=db)


@user_router.post("/users", response_model=User, tags=["Users"], responses={
    200: {"description": "User created."},
    400: {"description": "User not created due to errors on request."}
})
def post_users(user: UserCreate, logged_in_user: User = Depends(authenticate), db: Session = Depends(get_db)):
    has_role("admin", logged_in_user)
    try:
        user = create_user(db=db, user=user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="A user with the same slug already exists")
    return user
