from fastapi import FastAPI

from .users.user import user_router


app = FastAPI()


@app.get("/")
def hello():
    return {"message": "Hello!"}


app.include_router(user_router)
