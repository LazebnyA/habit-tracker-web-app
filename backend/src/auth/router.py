from fastapi import APIRouter, Depends

from src.auth.dependencies import auth_user_issue_jwt, REFRESH_TOKEN_TYPE, UserGetterByToken, \
    ACCESS_TOKEN_TYPE
from src.repository import UserRepository
from src.schemas import UserRegScheme, UserSignInScheme, UserSchema, TokenSchema

router = APIRouter(
    prefix="",
    tags=["User"]
)


@router.post("/user/register", response_model=UserSchema, status_code=201, summary="Register a new user")
async def register_user(user: UserRegScheme) -> TokenSchema:
    user_data = await UserRepository.create_user(user)
    token_data = auth_user_issue_jwt(user_data)

    return token_data


@router.post("/user/signin")
async def signin_user(user: UserSignInScheme) -> TokenSchema:
    user_data = await UserRepository.verify_account(user)
    token_data = auth_user_issue_jwt(user_data)

    return token_data


@router.post("/refresh", response_model=TokenSchema)
def refresh_jwt(
        user: UserSchema = Depends(UserGetterByToken(REFRESH_TOKEN_TYPE)),
) -> TokenSchema:
    token_data = auth_user_issue_jwt(user)

    return token_data


@router.get("/user/data")
async def get_user_data(
        user: UserSchema = Depends(UserGetterByToken(ACCESS_TOKEN_TYPE)),
) -> UserSchema:
    user_data = await UserRepository.get_user_info(user)

    return user_data
