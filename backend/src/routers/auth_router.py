from typing import Annotated

from fastapi import Depends, APIRouter

from src.auth.utils import create_access_token, create_refresh_token
from src.repository import UserRepository
from src.schemas import UserRegScheme, UserSignInScheme, UserSchema, TokenSchema

router = APIRouter(
    prefix="",
    tags=["User"]
)


def auth_user_issue_jwt(
        user: UserSchema
) -> TokenSchema:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/user/register", response_model=UserSchema, status_code=201, summary="Register a new user")
async def register_user(user: UserRegScheme) -> TokenSchema:
    """
    Handles user registration.

    Args:
        user (UserRegScheme): The registration details provided by the client.
    Returns:
        user_data (UserSchema): The created user object (or a response indicating successful registration).
    Raises:
        HTTPException: If user creation fails.
    """
    user_data = await UserRepository.create_user(user)
    token_data = auth_user_issue_jwt(user_data)

    return token_data


@router.post("/user/signin")
async def signin_user(user: UserSignInScheme) -> TokenSchema:
    user_data: UserSchema = await UserRepository.verify_account(user)
    token_data = auth_user_issue_jwt(user_data)

    return token_data
