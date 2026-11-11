from sqlalchemy import Boolean, Enum, Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base
from app.enums.enums import RolUsuario
from sqlalchemy.orm import relationship


class Usuario(Base):
    __tablename__ = "usuarios"

    id_usuario: Mapped[int] = mapped_column(
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

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    contrasena_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    rol: Mapped[RolUsuario] = mapped_column(
        Enum(RolUsuario),
        nullable=False
    )

    activo: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    cursos = relationship(
    "Curso",
    back_populates="docente"
    )