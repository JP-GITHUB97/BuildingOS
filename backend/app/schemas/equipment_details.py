from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EquipmentPointLatest(BaseModel):
    id: int
    name: str
    code: str
    type: str
    unit: str | None = None
    latest_value: float | None = None
    latest_timestamp: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class EquipmentDetailsRead(BaseModel):
    id: int
    name: str
    code: str
    room_id: int
    points: list[EquipmentPointLatest]