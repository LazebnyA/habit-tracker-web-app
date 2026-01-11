from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from repository import UserRepository
from schemas import UserRegScheme, UserSignInScheme

router = APIRouter(prefix="", tags=["User"])


@router.post("/user/register")
async def register_user(
    user: UserRegScheme, session: AsyncSession = Depends(get_async_session)
):
    user_repo = UserRepository(session)
    user_reg = await user_repo.add_user(user)
    return user_reg


@router.post("/user/signin")
async def signin_user(user: Annotated[UserSignInScheme, Depends()]):
    user_data = await UserRepository.verify_account(user)
    return user_data
