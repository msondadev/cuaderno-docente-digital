from datetime import date

from sqlalchemy import Date
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base
from app.enums.enums import EstadoAcademico
from sqlalchemy.orm import relationship


class Inscripcion(Base):
    __tablename__ = "inscripciones"

    id_inscripcion: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    id_alumno: Mapped[int] = mapped_column(
        ForeignKey("alumnos.id_alumno"),
        nullable=False
    )

    id_curso: Mapped[int] = mapped_column(
        ForeignKey("cursos.id_curso"),
        nullable=False
    )

    fecha_inscripcion: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    estado_academico: Mapped[EstadoAcademico | None] = mapped_column(
        Enum(EstadoAcademico),
        nullable=True
    )

    alumno = relationship(
    "Alumno",
    back_populates="inscripciones"
    )

    curso = relationship(
        "Curso",
        back_populates="inscripciones"
    )