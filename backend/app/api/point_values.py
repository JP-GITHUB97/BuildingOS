from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.point import Point
from app.models.point_value import PointValue
from app.schemas.point_value import PointValueCreate, PointValueRead


router = APIRouter(
    prefix="/point-values",
    tags=["Point Values"],
)


@router.post("/", response_model=PointValueRead)
def create_point_value(
    point_value: PointValueCreate,
    db: Session = Depends(get_db),
):
    point = (
        db.query(Point)
        .filter(Point.id == point_value.point_id)
        .first()
    )

    if point is None:
        raise HTTPException(
            status_code=404,
            detail="Point not found",
        )

    db_point_value = PointValue(
        value=point_value.value,
        timestamp=point_value.timestamp,
        point_id=point_value.point_id,
    )

    db.add(db_point_value)
    db.commit()
    db.refresh(db_point_value)

    return db_point_value


@router.get("/", response_model=list[PointValueRead])
def get_point_values(db: Session = Depends(get_db)):
    return db.query(PointValue).all()


@router.get("/point/{point_id}", response_model=list[PointValueRead])
def get_values_by_point(
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

    return (
        db.query(PointValue)
        .filter(PointValue.point_id == point_id)
        .order_by(PointValue.timestamp)
        .all()
    )