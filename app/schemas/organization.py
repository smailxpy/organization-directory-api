from pydantic import BaseModel
from typing import List, Optional
from app.schemas.building import Building
from app.schemas.activity import Activity

class OrganizationBase(BaseModel):
    name: str
    phone_numbers: Optional[str] = None
    building_id: int
    activity_ids: List[int] = []

class OrganizationCreate(OrganizationBase):
    pass

class Organization(OrganizationBase):
    id: int
    building: Optional[Building]
    activities: List[Activity] = []

    class Config:
        orm_mode = True
