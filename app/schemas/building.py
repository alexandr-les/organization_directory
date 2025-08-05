from pydantic import BaseModel

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
