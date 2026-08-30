from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class Point(Base):
    __tablename__ = "points"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    unit: Mapped[str | None] = mapped_column(String(50), nullable=True)

    equipment_id: Mapped[int] = mapped_column(
        ForeignKey("equipments.id"),
        nullable=False,
    )

    equipment: Mapped["Equipment"] = relationship(
        back_populates="points",
    )


from app.models.equipment import Equipment