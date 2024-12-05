from fastapi import APIRouter

from src.repository import NewsRepository
from src.schemas import NewsScheme, NewsDatabaseModel

router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@router.get("/get")
async def get_posts() -> list[NewsDatabaseModel]:
    return await NewsRepository.get_news()

@router.post("/create")
async def create_post(post_data: NewsScheme):
    post_response = await NewsRepository.post_news(post_data)

    return post_response

