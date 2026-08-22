from fastapi import APIRouter, Depends, HTTPException
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


@router.get("/{building_id}", response_model=BuildingRead)
def get_building(
    building_id: int,
    db: Session = Depends(get_db),
):
    building = db.query(Building).filter(Building.id == building_id).first()

    if building is None:
        raise HTTPException(
            status_code=404,
            detail="Building not found",
        )

    return building
