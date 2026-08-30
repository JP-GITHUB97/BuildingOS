from app.db.session import Base, engine
from app.models.building import Building
from app.models.room import Room
from app.models.equipment import Equipment

def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")