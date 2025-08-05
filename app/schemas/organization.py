from pydantic import BaseModel
from typing import List, Optional

class PhoneBase(BaseModel):
    number: str

class PhoneCreate(PhoneBase):
    pass

class Phone(PhoneBase):
    id: int

    class Config:
        orm_mode = True

class ActivityBase(BaseModel):
    name: str

class ActivityCreate(ActivityBase):
    parent_id: Optional[int] = None

class Activity(ActivityBase):
    id: int
    parent_id: Optional[int] = None

    class Config:
        orm_mode = True

class BuildingBase(BaseModel):
    address: str
    latitude: str
    longitude: str

class BuildingCreate(BuildingBase):
    pass

class Building(BuildingBase):
    id: int

    class Config:
        orm_mode = True

class OrganizationBase(BaseModel):
    name: str

class OrganizationCreate(OrganizationBase):
    building_id: int
    phone_numbers: List[str]
    activity_ids: List[int]

class Organization(OrganizationBase):
    id: int
    building_id: int
    phones: List[Phone] = []
    activities: List[Activity] = []
    building: Building

    class Config:
        orm_mode = True
