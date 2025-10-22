from pydantic import BaseModel
from typing import Optional, List

class ActivityBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class ActivityCreate(ActivityBase):
    pass

class Activity(ActivityBase):
    id: int
    children: List["Activity"] = []

    class Config:
        orm_mode = True
