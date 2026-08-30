from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.building import Building
from app.models.equipment import Equipment
from app.models.point import Point
from app.models.point_value import PointValue
from app.models.room import Room
from app.schemas.building import BuildingCreate, BuildingRead, BuildingUpdate
from app.schemas.building_details import (
    BuildingDetailsRead,
    BuildingEquipmentDetails,
    BuildingPointLatest,
    BuildingRoomDetails,
)


router = APIRouter(
    prefix="/buildings",
    tags=["Buildings"],
)


@router.post("/", response_model=BuildingRead)
def create_building(
    building: BuildingCreate,
    db: Session = Depends(get_db),
):
    db_building = Building(
        name=building.name,
        code=building.code,
    )

    db.add(db_building)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Building code already exists",
        )

    db.refresh(db_building)

    return db_building


@router.get("/", response_model=list[BuildingRead])
def get_buildings(db: Session = Depends(get_db)):
    return db.query(Building).all()


@router.get("/{building_id}/details", response_model=BuildingDetailsRead)
def get_building_details(
    building_id: int,
    db: Session = Depends(get_db),
):
    building = (
        db.query(Building)
        .filter(Building.id == building_id)
        .first()
    )

    if building is None:
        raise HTTPException(
            status_code=404,
            detail="Building not found",
        )

    rooms_details = []

    rooms = (
        db.query(Room)
        .filter(Room.building_id == building_id)
        .all()
    )

    for room in rooms:
        equipments_details = []

        equipments = (
            db.query(Equipment)
            .filter(Equipment.room_id == room.id)
            .all()
        )

        for equipment in equipments:
            points_details = []

            points = (
                db.query(Point)
                .filter(Point.equipment_id == equipment.id)
                .all()
            )

            for point in points:
                latest_value = (
                    db.query(PointValue)
                    .filter(PointValue.point_id == point.id)
                    .order_by(desc(PointValue.timestamp))
                    .first()
                )

                points_details.append(
                    BuildingPointLatest(
                        id=point.id,
                        name=point.name,
                        code=point.code,
                        type=point.type,
                        unit=point.unit,
                        latest_value=(
                            latest_value.value
                            if latest_value is not None
                            else None
                        ),
                        latest_timestamp=(
                            latest_value.timestamp
                            if latest_value is not None
                            else None
                        ),
                    )
                )

            equipments_details.append(
                BuildingEquipmentDetails(
                    id=equipment.id,
                    name=equipment.name,
                    code=equipment.code,
                    room_id=room.id,
                    points=points_details,
                )
            )

        rooms_details.append(
            BuildingRoomDetails(
                id=room.id,
                name=room.name,
                code=room.code,
                building_id=building_id,
                equipments=equipments_details,
            )
        )

    return BuildingDetailsRead(
        id=building.id,
        name=building.name,
        code=building.code,
        rooms=rooms_details,
    )


@router.get("/{building_id}", response_model=BuildingRead)
def get_building(
    building_id: int,
    db: Session = Depends(get_db),
):
    building = (
        db.query(Building)
        .filter(Building.id == building_id)
        .first()
    )

    if building is None:
        raise HTTPException(
            status_code=404,
            detail="Building not found",
        )

    return building


@router.put("/{building_id}", response_model=BuildingRead)
def update_building(
    building_id: int,
    building_update: BuildingUpdate,
    db: Session = Depends(get_db),
):
    building = (
        db.query(Building)
        .filter(Building.id == building_id)
        .first()
    )

    if building is None:
        raise HTTPException(
            status_code=404,
            detail="Building not found",
        )

    building.name = building_update.name
    building.code = building_update.code

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Building code already exists",
        )

    db.refresh(building)

    return building


@router.delete(
    "/{building_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_building(
    building_id: int,
    db: Session = Depends(get_db),
):
    building = (
        db.query(Building)
        .filter(Building.id == building_id)
        .first()
    )

    if building is None:
        raise HTTPException(
            status_code=404,
            detail="Building not found",
        )

    db.delete(building)
    db.commit()