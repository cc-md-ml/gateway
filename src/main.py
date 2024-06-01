from fastapi import FastAPI

from src.config import setup_env
from src.routes import global_router


app = FastAPI(
    title="Cooleet Back-End API"
)

# load environment variables
# return value will be cached
setup_env()

app.include_router(global_router, prefix="/api/v1")

@app.get("/")
async def root():
    return { "message": "Hello World" }
