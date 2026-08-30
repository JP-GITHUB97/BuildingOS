from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Room(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    building_id: Mapped[int] = mapped_column(
        ForeignKey("buildings.id"),
        nullable=False,
    )

    building: Mapped["Building"] = relationship(
        back_populates="rooms",
    )

    equipments: Mapped[list["Equipment"]] = relationship(
        back_populates="room",
        cascade="all, delete-orphan",
    )


from app.models.building import Building
from app.models.equipment import Equipment