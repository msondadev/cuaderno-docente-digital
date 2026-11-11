from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base
from app.enums.enums import EstadoTP
from sqlalchemy.orm import relationship

class Calificacion(Base):
    __tablename__ = "calificaciones"

    id_calificacion: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    id_evaluacion: Mapped[int] = mapped_column(
        ForeignKey("evaluaciones.id_evaluacion"),
        nullable=False
    )

    id_alumno: Mapped[int] = mapped_column(
        ForeignKey("alumnos.id_alumno"),
        nullable=False
    )

    nota: Mapped[float | None] = mapped_column(
        Float,
        nullable=True
    )

    estado_tp: Mapped[EstadoTP | None] = mapped_column(
        Enum(EstadoTP),
        nullable=True
    )

    valoracion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    evaluacion = relationship(
    "Evaluacion",
    back_populates="calificaciones"
    )

    alumno = relationship(
        "Alumno",
        back_populates="calificaciones"
    )