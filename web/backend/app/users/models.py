from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from ..db import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        unique=True,
        autoincrement=True
    )
    username = Column(
        String,
        unique=True
    )
    email = Column(
        String,
        unique=True
    )
    password = Column(
        String
    )
    created_at = Column(
        DateTime,
        default=datetime.now
    )
