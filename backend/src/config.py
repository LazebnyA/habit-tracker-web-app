from pathlib import Path

from dotenv import load_dotenv
import os

from dataclasses import dataclass

load_dotenv()

BASE_DIR = Path(__file__).parent.parent

DATABASE_URL = os.environ.get("DATABASE_URL")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_DB = os.environ.get("POSTGRES_DB")


@dataclass(frozen=True)
class AuthJWT:
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"


AUTH_JWT = AuthJWT()
