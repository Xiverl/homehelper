from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from authx import AuthX

from .schemas import User, UserLogin
from .models import UserModel


class UserController():
    """Класс для операций модели пользоватлей."""
    def __init__(self, session: AsyncSession, auth: AuthX):
        self.session = session
        self.auth = auth
        self.hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def create_user(self, user: User):
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == user.email)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists"
            )

        hashed_password = self._get_password_hash(user.password)

        user_obj = UserModel(
            username=user.username,
            email=user.email,
            password=hashed_password
        )
        try:
            self.session.add(user_obj)
            await self.session.commit()
            await self.session.refresh(user_obj)
            return user_obj
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(
                status_code=422,
                detail=f"Error user create: {str(e)}"
            )

    async def list_user(self):
        result = await self.session.execute(select(UserModel))
        users = result.scalars().all()
        return users

    async def get_user(self, user_id: int):
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        return user

    async def get_current_user(self, request: Request):
        email = self._get_decode_email_in_token(request=request)
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=401,
                detail={"message": "Not auth"}
            )
        return user

    async def edit_user(self, user_id: int, user_data: dict):
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        for key, value in user_data.items():
            if key == "password":
                value = self._get_password_hash(value)
            setattr(user, key, value)

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete_user(self, user_id: int):
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        await self.session.delete(user)
        await self.session.commit()
        return {"message": "User deleted successfully"}

    async def get_tocken(self, login_data: UserLogin):
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == login_data.email)
        )
        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password"
            )

        if not self._verify_password(login_data.password, user.password):
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password"
            )
        return self.auth.create_access_token(uid=user.email)

    def _get_password_hash(self, password):
        return self.hasher.hash(password)

    def _verify_password(self, plain_password, hashed_password):
        return self.hasher.verify(plain_password, hashed_password)

    def _get_decode_email_in_token(self, request: Request):
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(
                status_code=401,
                detail="Authorization header is missing"
            )
        token_str = token.replace("Bearer ", "")
        payload = self.auth._decode_token(token_str)
        return payload.sub
