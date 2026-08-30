from pydantic import BaseModel, ConfigDict


class PointBase(BaseModel):
    name: str
    code: str
    type: str
    unit: str | None = None
    equipment_id: int


class PointCreate(PointBase):
    pass


class PointUpdate(PointBase):
    pass


class PointRead(PointBase):
    id: int

    model_config = ConfigDict(from_attributes=True)