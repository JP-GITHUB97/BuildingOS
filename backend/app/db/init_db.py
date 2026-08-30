from app.db.session import Base, engine
from app.models.building import Building
from app.models.room import Room
from app.models.equipment import Equipment
from app.models.point import Point
from app.models.point_value import PointValue

def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")