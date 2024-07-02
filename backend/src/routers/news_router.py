from fastapi import APIRouter
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache

from src.repository import NewsRepository
from src.schemas import NewsScheme, NewsDatabaseModel

router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@router.get("/get")
@cache(expire=180)
async def get_posts() -> list[NewsDatabaseModel]:
    return await NewsRepository.get_news()

@router.post("/create")
async def create_post(post_data: NewsScheme):
    post_response = await NewsRepository.post_news(post_data)

    await FastAPICache.clear()

    return post_response

