from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BuildingPointLatest(BaseModel):
    id: int
    name: str
    code: str
    type: str
    unit: str | None = None
    latest_value: float | None = None
    latest_timestamp: datetime | None = None


class BuildingEquipmentDetails(BaseModel):
    id: int
    name: str
    code: str
    room_id: int
    points: list[BuildingPointLatest]


class BuildingRoomDetails(BaseModel):
    id: int
    name: str
    code: str
    building_id: int
    equipments: list[BuildingEquipmentDetails]


class BuildingDetailsRead(BaseModel):
    id: int
    name: str
    code: str
    rooms: list[BuildingRoomDetails]

    model_config = ConfigDict(from_attributes=True)