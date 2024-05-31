from fastapi import FastAPI

from .routes import global_router
# from auth.router import router as auth_router


app = FastAPI(
    title="Cooleet Back-End API"
)

app.include_router(global_router, prefix="/api/v1")

@app.get("/")
async def root():
    return { "message": "Hello World" }
