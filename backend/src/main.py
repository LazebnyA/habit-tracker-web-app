from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers.habits_router import router as habits_router
from src.routers.goals_router import router as goals_router
from src.routers.user_router import router as user_router
from src.routers.news_router import router as news_router

app = FastAPI()

origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000"
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




