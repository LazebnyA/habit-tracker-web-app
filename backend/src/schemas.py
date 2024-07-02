from datetime import datetime
from typing import Self
from pydantic import BaseModel, EmailStr, Field, model_validator, ConfigDict


class Goal(BaseModel):
    id: int
    name: str


class UserRegScheme(BaseModel):
    firstName: str = Field(..., min_length=1)
    lastName: str = Field(..., min_length=1)
    email: EmailStr = Field(min_length=1)
    password: str = Field(..., min_length=5)
    passwordConfirm: str = Field(..., min_length=5)

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        pw1 = self.password
        pw2 = self.passwordConfirm
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return self.passwordConfirm


class UserSignInScheme(BaseModel):
    email: EmailStr = Field(min_length=1)
    password: str = Field(..., min_length=5)


class UserOrmScheme(BaseModel):
    firstName: str
    lastName: str
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
