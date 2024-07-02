from contextlib import asynccontextmanager
from typing import AsyncIterator, Callable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.habits_router import router as habits_router
from src.routers.goals_router import router as goals_router
from src.routers.user_router import router as user_router
from src.routers.news_router import router as news_router

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

app = FastAPI()

origins = [
    "https://habit-tracker-template.onrender.com",
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://localhost:3002",
    "http://192.168.1.3:3000",
    "http://192.168.1.4:3000",
    "http://192.168.1.4:3002",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}


app.include_router(goals_router)
app.include_router(user_router)
app.include_router(habits_router)
app.include_router(news_router)


# Async context manager to initialize FastAPICache with Redis
@asynccontextmanager
async def lifespan() -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    try:
        yield
    finally:
        await redis.close()


app.lifespan_context = lifespan


# Register the context manager with the app
@app.on_event("startup")
async def startup_event():
    async with lifespan():
        print("FastAPICache initialized")



