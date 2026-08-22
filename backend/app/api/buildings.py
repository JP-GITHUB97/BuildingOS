from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.building import Building
from app.schemas.building import BuildingCreate, BuildingRead


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
    db.commit()
    db.refresh(db_building)

    return db_building


@router.get("/", response_model=list[BuildingRead])
def get_buildings(db: Session = Depends(get_db)):
    return db.query(Building).all()