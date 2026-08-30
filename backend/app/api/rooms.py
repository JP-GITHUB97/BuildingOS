from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.building import Building
from app.models.room import Room
from app.schemas.room import RoomCreate, RoomRead, RoomUpdate


router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"],
)


@router.post("/", response_model=RoomRead)
def create_room(
    room: RoomCreate,
    db: Session = Depends(get_db),
):
    building = (
        db.query(Building)
        .filter(Building.id == room.building_id)
        .first()
    )

    if building is None:
        raise HTTPException(
            status_code=404,
            detail="Building not found",
        )

    existing_room = (
        db.query(Room)
        .filter(Room.code == room.code)
        .first()
    )

    if existing_room is not None:
        raise HTTPException(
            status_code=409,
            detail="Room code already exists",
        )

    db_room = Room(
        name=room.name,
        code=room.code,
        building_id=room.building_id,
    )

    db.add(db_room)

    try:
        db.commit()
        db.refresh(db_room)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Room code already exists",
        )

    return db_room

@router.get("/", response_model=list[RoomRead])
def get_rooms(db: Session = Depends(get_db)):
    return db.query(Room).all()

@router.get("/{room_id}", response_model=RoomRead)
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
):
    room = (
        db.query(Room)
        .filter(Room.id == room_id)
        .first()
    )

    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )

    return room

@router.put("/{room_id}", response_model=RoomRead)
def update_room(
    room_id: int,
    room: RoomUpdate,
    db: Session = Depends(get_db),
):
    db_room = (
        db.query(Room)
        .filter(Room.id == room_id)
        .first()
    )

    if db_room is None:
        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )

    building = (
        db.query(Building)
        .filter(Building.id == room.building_id)
        .first()
    )

    if building is None:
        raise HTTPException(
            status_code=404,
            detail="Building not found",
        )

    existing_room = (
        db.query(Room)
        .filter(
            Room.code == room.code,
            Room.id != room_id,
        )
        .first()
    )

    if existing_room is not None:
        raise HTTPException(
            status_code=409,
            detail="Room code already exists",
        )

    db_room.name = room.name
    db_room.code = room.code
    db_room.building_id = room.building_id

    try:
        db.commit()
        db.refresh(db_room)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Room code already exists",
        )

    return db_room

@router.delete("/{room_id}", status_code=204)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
):
    db_room = (
        db.query(Room)
        .filter(Room.id == room_id)
        .first()
    )

    if db_room is None:
        raise HTTPException(
            status_code=404,
            detail="Room not found",
        )

    db.delete(db_room)
    db.commit()