from datetime import date

from sqlalchemy import Date
from sqlalchemy import Integer

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base
from sqlalchemy.orm import relationship


class Cuatrimestre(Base):
    __tablename__ = "cuatrimestres"

    id_cuatrimestre: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    anio: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    numero: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    fecha_inicio: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    fecha_fin: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    clases = relationship(
    "Clase",
    back_populates="cuatrimestre"
    )

    evaluaciones = relationship(
    "Evaluacion",
    back_populates="cuatrimestre"
    )