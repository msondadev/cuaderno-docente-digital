from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base
from sqlalchemy.orm import relationship


class Alumno(Base):
    __tablename__ = "alumnos"

    id_alumno: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    apellido: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    email: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    inscripciones = relationship(
    "Inscripcion",
    back_populates="alumno"
    )

    asistencias = relationship(
    "Asistencia",
    back_populates="alumno"
    )

    calificaciones = relationship(
    "Calificacion",
    back_populates="alumno"
    )