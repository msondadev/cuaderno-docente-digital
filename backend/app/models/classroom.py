from datetime import date

from sqlalchemy import Date
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base
from app.enums.enums import EstadoClase
from sqlalchemy.orm import relationship


class Clase(Base):
    __tablename__ = "clases"

    id_clase: Mapped[int] = mapped_column(
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

    fecha: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    estado: Mapped[EstadoClase] = mapped_column(
        Enum(EstadoClase),
        nullable=False
    )

    tema: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True
    )

    curso = relationship(
    "Curso",
    back_populates="clases"
    )

    cuatrimestre = relationship(
    "Cuatrimestre",
    back_populates="clases"
    )

    asistencias = relationship(
    "Asistencia",
    back_populates="clase"
    )