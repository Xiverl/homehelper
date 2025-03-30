from fastapi import APIRouter, status, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from .schemas import User, UserResponse, UserLogin
from .controllers import UserController
from ..db import get_db
from ..auth import auth


user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        404: {
            "error": "Not found"
        }
    }
)


@user_router.post('/login')
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    user_controller = UserController(session=db, auth=auth)
    token = await user_controller.get_tocken(login_data)
    return {"access_token": token}


@user_router.get(
    "/me",
    dependencies=[Depends(auth.access_token_required)],
    response_model=UserResponse
)
async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    user_controller = UserController(session=db, auth=auth)
    return await user_controller.get_current_user(request)


@user_router.post(
    "/", status_code=status.HTTP_201_CREATED,
    response_model=UserResponse
)
async def add_user(user: User, db: AsyncSession = Depends(get_db)):
    user_controller = UserController(session=db, auth=auth)
    return await user_controller.create_user(user)
