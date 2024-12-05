from datetime import datetime

from pydantic import BaseModel, Field


class GoalCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=50)


class GoalRetrieveSchema(BaseModel):
    id: int
    name: str
    created_date: datetime
    user_id: int

    class Config:
        from_attributes = True
        orm_mode = True
