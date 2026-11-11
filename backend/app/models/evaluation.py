from datetime import date

from sqlalchemy import Date
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base
from app.enums.enums import TipoEvaluacion
from sqlalchemy.orm import relationship


class Evaluacion(Base):
    __tablename__ = "evaluaciones"

    id_evaluacion: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    id_curso: Mapped[int] = mapped_column(
        ForeignKey("cursos.id_curso"),
        nullable=False
    )

    id_cuatrimestre: Mapped[int] = mapped_column(
        ForeignKey("cuatrimestres.id_cuatrimestre"),
        nullable=False
    )

    titulo: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    tipo: Mapped[TipoEvaluacion] = mapped_column(
        Enum(TipoEvaluacion),
        nullable=False
    )

    fecha: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    enlace_drive: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    curso = relationship(
    "Curso",
    back_populates="evaluaciones"
    )

    cuatrimestre = relationship(
    "Cuatrimestre",
    back_populates="evaluaciones"
    )

    calificaciones = relationship(
    "Calificacion",
    back_populates="evaluacion"
    )