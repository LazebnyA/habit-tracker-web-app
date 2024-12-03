from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from starlette import status

from src.auth.utils import decode_jwt, create_jwt
from src.schemas import UserSchema, TokenSchema

http_bearer = HTTPBearer(auto_error=True)

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def get_current_token_payload(
        credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
) -> dict:
    token = credentials.credentials
    try:
        payload = decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {e}"
        )

    return payload


async def get_user_by_jwt(
        payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    user_data = {
        'id': int(payload['sub']),
        'email': payload['email']
    }

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return UserSchema(**user_data)


def validate_token_type(payload: dict, valid_token_type: str) -> None:
    token_type = payload.get(TOKEN_TYPE_FIELD)
    if token_type != valid_token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type {token_type!r} expected {valid_token_type!r}"
        )


class UserGetterByToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    async def __call__(
            self, payload: dict = Depends(get_current_token_payload)
    ) -> UserSchema:
        validate_token_type(payload, self.token_type)
        return await get_user_by_jwt(payload)


def generate_token(
        user: UserSchema, token_type: str
):
    jwt_payload = {
        'sub': user.id,
        'email': user.email,
    }

    token = create_jwt(token_type, jwt_payload)
    return token


def auth_user_issue_jwt(
        user: UserSchema
) -> TokenSchema:
    access_token = generate_token(user, ACCESS_TOKEN_TYPE)
    refresh_token = generate_token(user, REFRESH_TOKEN_TYPE)

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token
    )
