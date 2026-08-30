from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.equipment import Equipment
from app.models.room import Room
from app.schemas.equipment import EquipmentCreate, EquipmentRead, EquipmentUpdate


router = APIRouter(
    prefix="/equipments",
    tags=["Equipments"],
)


@router.post("/", response_model=EquipmentRead)
def create_equipment(
    equipment: EquipmentCreate,
    db: Session = Depends(get_db),
):
    room = (
        db.query(Room)
        .filter(Room.id == equipment.room_id)
        .first()
    )

    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )

    existing_equipment = (
        db.query(Equipment)
        .filter(Equipment.code == equipment.code)
        .first()
    )

    if existing_equipment is not None:
        raise HTTPException(
            status_code=409,
            detail="Equipment code already exists",
        )

    db_equipment = Equipment(
        name=equipment.name,
        code=equipment.code,
        room_id=equipment.room_id,
    )

    db.add(db_equipment)

    try:
        db.commit()
        db.refresh(db_equipment)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Equipment code already exists",
        )

    return db_equipment


@router.get("/", response_model=list[EquipmentRead])
def get_equipments(db: Session = Depends(get_db)):
    return db.query(Equipment).all()


@router.get("/{equipment_id}", response_model=EquipmentRead)
def get_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
):
    equipment = (
        db.query(Equipment)
        .filter(Equipment.id == equipment_id)
        .first()
    )

    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found",
        )

    return equipment


@router.put("/{equipment_id}", response_model=EquipmentRead)
def update_equipment(
    equipment_id: int,
    equipment: EquipmentUpdate,
    db: Session = Depends(get_db),
):
    db_equipment = (
        db.query(Equipment)
        .filter(Equipment.id == equipment_id)
        .first()
    )

    if db_equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found",
        )

    room = (
        db.query(Room)
        .filter(Room.id == equipment.room_id)
        .first()
    )

    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )

    existing_equipment = (
        db.query(Equipment)
        .filter(
            Equipment.code == equipment.code,
            Equipment.id != equipment_id,
        )
        .first()
    )

    if existing_equipment is not None:
        raise HTTPException(
            status_code=409,
            detail="Equipment code already exists",
        )

    db_equipment.name = equipment.name
    db_equipment.code = equipment.code
    db_equipment.room_id = equipment.room_id

    try:
        db.commit()
        db.refresh(db_equipment)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Equipment code already exists",
        )

    return db_equipment


@router.delete("/{equipment_id}", status_code=204)
def delete_equipment(
    equipment_id: int,
    db: Session = Depends(get_db),
):
    db_equipment = (
        db.query(Equipment)
        .filter(Equipment.id == equipment_id)
        .first()
    )

    if db_equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found",
        )

    db.delete(db_equipment)
    db.commit()