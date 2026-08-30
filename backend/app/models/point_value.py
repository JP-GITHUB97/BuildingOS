from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class PointValue(Base):
    __tablename__ = "point_values"

    id: Mapped[int] = mapped_column(primary_key=True)

    value: Mapped[float] = mapped_column(Float, nullable=False)

    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    point_id: Mapped[int] = mapped_column(
        ForeignKey("points.id"),
        nullable=False,
    )

    point: Mapped["Point"] = relationship(
        back_populates="values",
    )


from app.models.point import Point