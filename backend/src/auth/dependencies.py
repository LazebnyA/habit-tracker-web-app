from jwt.exceptions import InvalidTokenError

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import EmailStr
from starlette import status

from src.auth.utils import hash_password, encode_jwt, decode_jwt, validate_password, create_access_token, \
    create_refresh_token, TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from src.schemas import UserSchema, TokenSchema

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(prefix="/jwt", tags=["JWT"], dependencies=[Depends(http_bearer)])

john = UserSchema(
    email="john@example.com",
    password=hash_password("marmelad18A!")
)

sam = UserSchema(
    email="sam@example.com",
    password=hash_password("secret")
)

users_db: dict[EmailStr, UserSchema] = {
    john.email: john,
    sam.email: sam
}


def validate_auth_user(
        email: EmailStr,
        password: str) -> UserSchema:
    unauthenticated_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid email or password",
    )

    if not (user := users_db.get(email)):
        raise unauthenticated_exception

    if not validate_password(
            password=password,
            hashed_password=user.password
    ):
        raise unauthenticated_exception

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account is no longer active"
        )

    return user


@router.post("/login", response_model=TokenSchema)
def auth_user_issue_jwt(
        user: UserSchema = Depends(validate_auth_user)
) -> TokenSchema:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token
    )


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


def get_current_user(
        payload: dict = Depends(get_current_token_payload),
) -> UserSchema:
    email: str | None = payload.get("sub")

    if user := users_db.get(email):
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found"
    )


def validate_token_type(payload: dict, valid_token_type: str) -> None:
    token_type = payload.get(TOKEN_TYPE_FIELD)
    if token_type != valid_token_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type {token_type!r} expected {ACCESS_TOKEN_TYPE!r}"
        )


class UserGetterByToken:
    def __init__(self, token_type: str):
        self.token_type = token_type

    def __call__(self, payload: Depends(get_current_token_payload)):
        validate_token_type(payload, self.token_type)
        return get_current_user(payload)


def get_active_current_user(
        user: UserSchema = Depends(UserGetterByToken(ACCESS_TOKEN_TYPE))
) -> UserSchema:
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="This account is no longer active"
    )


@router.post("/refresh", response_model=TokenSchema)
def auth_refresh_jwt(
        user: UserSchema = Depends(UserGetterByToken(REFRESH_TOKEN_TYPE))
) -> TokenSchema:
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.get("/users/me")
def check_info(
        user: UserSchema = Depends(get_active_current_user),
):
    return {
        "email": user.email,
        "active": user.active,
    }
