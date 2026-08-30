from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.equipment import Equipment
from app.models.point import Point
from app.schemas.point import PointCreate, PointRead, PointUpdate


router = APIRouter(
    prefix="/points",
    tags=["Points"],
)


@router.post("/", response_model=PointRead)
def create_point(
    point: PointCreate,
    db: Session = Depends(get_db),
):
    equipment = (
        db.query(Equipment)
        .filter(Equipment.id == point.equipment_id)
        .first()
    )

    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found",
        )

    existing_point = (
        db.query(Point)
        .filter(Point.code == point.code)
        .first()
    )

    if existing_point is not None:
        raise HTTPException(
            status_code=409,
            detail="Point code already exists",
        )

    db_point = Point(
        name=point.name,
        code=point.code,
        type=point.type,
        unit=point.unit,
        equipment_id=point.equipment_id,
    )

    db.add(db_point)

    try:
        db.commit()
        db.refresh(db_point)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Point code already exists",
        )

    return db_point


@router.get("/", response_model=list[PointRead])
def get_points(db: Session = Depends(get_db)):
    return db.query(Point).all()


@router.get("/{point_id}", response_model=PointRead)
def get_point(
    point_id: int,
    db: Session = Depends(get_db),
):
    point = (
        db.query(Point)
        .filter(Point.id == point_id)
        .first()
    )

    if point is None:
        raise HTTPException(
            status_code=404,
            detail="Point not found",
        )

    return point


@router.put("/{point_id}", response_model=PointRead)
def update_point(
    point_id: int,
    point: PointUpdate,
    db: Session = Depends(get_db),
):
    db_point = (
        db.query(Point)
        .filter(Point.id == point_id)
        .first()
    )

    if db_point is None:
        raise HTTPException(
            status_code=404,
            detail="Point not found",
        )

    equipment = (
        db.query(Equipment)
        .filter(Equipment.id == point.equipment_id)
        .first()
    )

    if equipment is None:
        raise HTTPException(
            status_code=404,
            detail="Equipment not found",
        )

    existing_point = (
        db.query(Point)
        .filter(
            Point.code == point.code,
            Point.id != point_id,
        )
        .first()
    )

    if existing_point is not None:
        raise HTTPException(
            status_code=409,
            detail="Point code already exists",
        )

    db_point.name = point.name
    db_point.code = point.code
    db_point.type = point.type
    db_point.unit = point.unit
    db_point.equipment_id = point.equipment_id

    try:
        db.commit()
        db.refresh(db_point)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Point code already exists",
        )

    return db_point


@router.delete("/{point_id}", status_code=204)
def delete_point(
    point_id: int,
    db: Session = Depends(get_db),
):
    db_point = (
        db.query(Point)
        .filter(Point.id == point_id)
        .first()
    )

    if db_point is None:
        raise HTTPException(
            status_code=404,
            detail="Point not found",
        )

    db.delete(db_point)
    db.commit()