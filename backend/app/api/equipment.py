from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models.point import Point
from app.models.point_value import PointValue

from app.db.session import get_db
from app.models.equipment import Equipment
from app.models.room import Room
from app.schemas.equipment import EquipmentCreate, EquipmentRead, EquipmentUpdate
from app.schemas.equipment_details import EquipmentDetailsRead


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

@router.get("/{equipment_id}/details", response_model=EquipmentDetailsRead)
def get_equipment_details(
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

    points = (
        db.query(Point)
        .filter(Point.equipment_id == equipment_id)
        .all()
    )

    point_details = []

    for point in points:
        latest_value = (
            db.query(PointValue)
            .filter(PointValue.point_id == point.id)
            .order_by(PointValue.timestamp.desc())
            .first()
        )

        point_details.append(
            {
                "id": point.id,
                "name": point.name,
                "code": point.code,
                "type": point.type,
                "unit": point.unit,
                "latest_value": (
                    latest_value.value
                    if latest_value is not None
                    else None
                ),
                "latest_timestamp": (
                    latest_value.timestamp
                    if latest_value is not None
                    else None
                ),
            }
        )

    return {
        "id": equipment.id,
        "name": equipment.name,
        "code": equipment.code,
        "room_id": equipment.room_id,
        "points": point_details,
    }


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