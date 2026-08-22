from pydantic import BaseModel, ConfigDict


class BuildingBase(BaseModel):
    name: str
    code: str


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BuildingBase):
    pass


class BuildingRead(BuildingBase):
    id: int

    model_config = ConfigDict(from_attributes=True)