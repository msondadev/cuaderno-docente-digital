from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Enum

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base
from app.enums.enums import RegimenCurso
from sqlalchemy.orm import relationship


class Curso(Base):
    __tablename__ = "cursos"

    id_curso: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    materia: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    division: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    institucion: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    regimen: Mapped[RegimenCurso] = mapped_column(
        Enum(RegimenCurso),
        nullable=False
    )

    max_faltas: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    porcentaje_minimo: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    enlace_drive: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    id_docente: Mapped[int] = mapped_column(
        ForeignKey("usuarios.id_usuario"),
        nullable=False
    )

    docente = relationship(
    "Usuario",
    back_populates="cursos"
    )

    inscripciones = relationship(
    "Inscripcion",
    back_populates="curso"
    )

    clases = relationship(
    "Clase",
    back_populates="curso"
    )

    evaluaciones = relationship(
    "Evaluacion",
    back_populates="curso"
    )