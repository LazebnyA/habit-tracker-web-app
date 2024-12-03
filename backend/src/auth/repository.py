from fastapi import HTTPException
from sqlalchemy import select
from starlette import status

from src.auth.models import User
from src.auth.schemas import UserRegScheme, UserSchema, UserSignInScheme
from src.auth.utils import hash_password, validate_password
from src.database import db_session


class UserAlreadyExistsException(HTTPException):
    def __init__(self, email: str):
        self.detail = f"User with the provided email '{email}' already exists"
        self.status_code = status.HTTP_409_CONFLICT


class UserDoesNotExistException(HTTPException):
    def __init__(self, email: str | None = None):
        if email:
            self.detail = f"User with the provided email '{email}' does not exist"
        else:
            self.detail = f"User does not exist"

        self.status_code = status.HTTP_404_NOT_FOUND


class UserRepository:
    @staticmethod
    async def create_user(data: UserRegScheme) -> UserSchema:
        user_dict: dict = data.model_dump()

        async with db_session() as session:
            query = select(User).filter(User.email == user_dict['email'])
            result = await session.execute(query)
            if result.scalars().one_or_none():
                raise UserAlreadyExistsException(email=user_dict['email'])

            user_dict.pop('password_confirm')

            user_dict['password'] = hash_password(user_dict['password'])
            user: User = User(**user_dict)
            user_dict.pop('password')

            session.add(user)

            await session.flush()
            await session.commit()

            user_data: UserSchema = UserSchema(**user_dict)

            return user_data

    @staticmethod
    async def verify_account(data: UserSignInScheme) -> UserSchema:
        user_dict: dict = data.model_dump()

        async with db_session() as session:
            query = select(User).filter(User.email == user_dict.get('email'))
            result = await session.execute(query)
            user = result.scalars().one_or_none()

            if not user:
                raise UserDoesNotExistException(email=data.email)

            if not validate_password(user_dict['password'], user.password):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid password"
                )

            return UserSchema.from_orm(user)

    @staticmethod
    async def get_user_info(data: UserSchema) -> UserSchema:
        async with db_session() as session:
            query = select(User).filter(data.id == User.id)
            result = await session.execute(query)
            user = result.scalars().one_or_none()

            if not user:
                raise UserDoesNotExistException()

            return UserSchema.from_orm(user)
