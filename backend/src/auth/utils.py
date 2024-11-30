from datetime import timedelta, datetime, UTC

import bcrypt
import jwt

from src.config import AUTH_JWT
from src.schemas import UserSchema

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def encode_jwt(
        payload: dict,
        expire_timedelta: timedelta,
        private_key: str = AUTH_JWT.private_key_path.read_text(),
        algorithm: str = AUTH_JWT.algorithm,
):
    to_encode = payload.copy()
    now = datetime.now(UTC)

    expire = now + expire_timedelta

    to_encode.update(
        exp=expire,
        iat=now
    )

    encoded = jwt.encode(to_encode, private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = AUTH_JWT.public_key_path.read_text(),
        algorithm: str = AUTH_JWT.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded


def create_jwt(
        token_type: str,
        token_payload: dict,
        expire_timedelta: timedelta
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_payload)
    return encode_jwt(
        payload=jwt_payload,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: UserSchema) -> str:
    jwt_payload = {"sub": user.email}
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_payload=jwt_payload,
        expire_timedelta=timedelta(days=AUTH_JWT.access_token_expires_days),
    )


def create_refresh_token(user: UserSchema) -> str:
    jwt_payload = {"sub": user.email}
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_payload=jwt_payload,
        expire_timedelta=timedelta(days=AUTH_JWT.refresh_token_expires_days),
    )


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)

    return hashed_password


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)
