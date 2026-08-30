from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Equipment(Base):
    __tablename__ = "equipments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    room_id: Mapped[int] = mapped_column(
        ForeignKey("rooms.id"),
        nullable=False,
    )

    room: Mapped["Room"] = relationship(
        back_populates="equipments",
    )

    points: Mapped[list["Point"]] = relationship(
        back_populates="equipment",
        cascade="all, delete-orphan",
    )


from app.models.room import Room
from app.models.point import Point