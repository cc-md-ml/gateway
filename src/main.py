from fastapi import FastAPI, Depends

from src.auth import firebase
from src.config import setup_env
from src.routes import global_router


app = FastAPI(
    title="Cooleet Back-End API"
)

# load environment variables
# return value will be cached
setup_env()

# initialize firebase authentication
firebase.init_auth()

# global app router
app.include_router(global_router, prefix="/api/v1")


@app.get("/")
async def root():
    return { "message": "Hello World" }

# TODO: remove dummy
@app.get("/api/user_token")
async def hello_user(user = Depends(firebase.get_user_token)):
    return { "msg": "Hello, user", "uid": user['uid'] } 
