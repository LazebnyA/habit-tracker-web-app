import jwt

from src.config import AUTH_JWT


def encode_jwt_token(
        payload: dict,
        private_key: str = AUTH_JWT.private_key_path.read_text(),
        algorithm: str = AUTH_JWT.algorithm,
):
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded


def decode_jwt_token(
        token: str | bytes,
        public_key: str = AUTH_JWT.public_key_path.read_text(),
        algorithm: str = AUTH_JWT.algorithm,
):
    decoded = jwt.decode(token, public_key, algorithms=[algorithm])
    return decoded
