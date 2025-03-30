from fastapi import FastAPI

from .db import Base, engine
from .users.routes import user_router
from .auth import auth


app = FastAPI()

app.include_router(user_router)


@app.on_event("startup")
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

auth.handle_errors(app)
