from pydantic import BaseModel, EmailStr, Field


class UserRegScheme(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(min_length=5)
    password_confirm: str = Field(min_length=5)


class UserSchema(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr

    class Config:
        from_attributes = True
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class UserSignInScheme(BaseModel):
    email: EmailStr
    password: str = Field(min_length=5)


class UserOrmScheme(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
