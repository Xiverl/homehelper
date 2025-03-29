from fastapi import APIRouter

from .schemas import User


USER_DB = []

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        404: {
            "error": "Not found"
        }
    }
)


@user_router.get("/")
def user_list():
    return {"users": USER_DB}


@user_router.post("/")
def add_user(user: User):
    global USER_DB
    user_info = {
        "username": user.username,
        "email": user.email,
        "password": user.password
    }
    USER_DB.append(user_info)
    return user_info
