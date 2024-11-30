from typing import Annotated

from fastapi import Depends, APIRouter

from src.repository import UserRepository
from src.schemas import UserRegScheme, UserSignInScheme, UserSchema

router = APIRouter(
    prefix="",
    tags=["User"]
)


@router.post("/user/register", response_model=UserSchema, status_code=201, summary="Register a new user")
async def register_user(user: UserRegScheme) -> UserSchema:
    """
    Handles user registration.

    Args:
        user (UserRegScheme): The registration details provided by the client.
    Returns:
        user_data (UserSchema): The created user object (or a response indicating successful registration).
    Raises:
        HTTPException: If user creation fails.
    """
    user_data: UserSchema = await UserRepository.create_user(user)

    return user_data


@router.post("/user/signin")
async def signin_user(user: UserSignInScheme):
    user_data: UserSchema = await UserRepository.verify_account(user)
    return user_data
