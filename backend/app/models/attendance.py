from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base
from app.enums.enums import EstadoAsistencia
from sqlalchemy.orm import relationship


class Asistencia(Base):
    __tablename__ = "asistencias"

    id_asistencia: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    id_clase: Mapped[int] = mapped_column(
        ForeignKey("clases.id_clase"),
        nullable=False
    )

    id_alumno: Mapped[int] = mapped_column(
        ForeignKey("alumnos.id_alumno"),
        nullable=False
    )

    estado: Mapped[EstadoAsistencia] = mapped_column(
        Enum(EstadoAsistencia),
        nullable=False
    )

    observacion: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    clase = relationship(
    "Clase",
    back_populates="asistencias"
)

    alumno = relationship(
        "Alumno",
        back_populates="asistencias"
    )