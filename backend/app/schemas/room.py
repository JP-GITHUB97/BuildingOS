from pydantic import BaseModel, ConfigDict


class RoomBase(BaseModel):
    name: str
    code: str
    building_id: int


class RoomCreate(RoomBase):
    pass


class RoomUpdate(RoomBase):
    pass


class RoomRead(RoomBase):
    id: int

    model_config = ConfigDict(from_attributes=True)