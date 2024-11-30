from datetime import datetime
from typing import Self
from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict


class Goal(BaseModel):
    id: int
    name: str


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    email: EmailStr
    first_name: str
    last_name: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class UserRegScheme(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(min_length=5)
    password_confirm: str = Field(min_length=5)


class UserSignInScheme(BaseModel):
    email: EmailStr
    password: str = Field(min_length=5)


class UserOrmScheme(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class DatabaseScheme(BaseModel):
    id: int
    name: str
    created_date: datetime

    model_config = ConfigDict(from_attributes=True)


class GoalDatabaseModel(DatabaseScheme):
    userID: int


class HabitDatabaseModel(DatabaseScheme):
    goalID: int


class TrackInfoDatabaseModel(BaseModel):
    id: int
    date: str = Field(..., min_length=10)
    is_checked: bool
    habitID: int

    model_config = ConfigDict(from_attributes=True)


class NewsDatabaseModel(BaseModel):
    id: int
    created_date: datetime
    title: str
    content: str
    userID: int

    model_config = ConfigDict(from_attributes=True)


class HabitDateModel(BaseModel):
    date: str = Field(default="YYYY_MM_DD", min_length=10)


class UserEmail(BaseModel):
    email: EmailStr


class GoalID(BaseModel):
    id: int


class HabitName(BaseModel):
    name: str


class GoalOrmScheme(BaseModel):
    name: str


class NewsScheme(BaseModel):
    user_id: int
    title: str
    content: str
