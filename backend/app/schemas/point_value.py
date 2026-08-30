from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PointValueBase(BaseModel):
    value: float
    timestamp: datetime
    point_id: int


class PointValueCreate(PointValueBase):
    pass


class PointValueRead(PointValueBase):
    id: int

    model_config = ConfigDict(from_attributes=True)