from pydantic import BaseModel, ConfigDict


class EquipmentBase(BaseModel):
    name: str
    code: str
    room_id: int


class EquipmentCreate(EquipmentBase):
    pass


class EquipmentUpdate(EquipmentBase):
    pass


class EquipmentRead(EquipmentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)