from typing import Optional, Self
from pydantic import BaseModel, EmailStr, Field, model_validator


class Goal(BaseModel):
    id: int
    name: str


class User(BaseModel):
    firstName: str = Field(..., min_length=1)
    lastName: str = Field(..., min_length=1)
    email: EmailStr | None = Field(default=None)
    password: str = Field(..., min_length=5)
    passwordConfirm: str = Field(..., min_length=5)

    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        pw1 = self.password
        pw2 = self.passwordConfirm
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('passwords do not match')
        return self.passwordConfirm

