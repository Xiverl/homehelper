from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    username: str = Field(
        min_length=3,
        max_length=15
    )
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
