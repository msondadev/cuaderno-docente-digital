from datetime import date

from pydantic import BaseModel

from app.enums.enums import EstadoClase


class ClassBase(BaseModel):
    id_curso: int
    id_cuatrimestre: int
    fecha: date
    estado: EstadoClase
    tema: str | None = None


class ClassCreate(ClassBase):
    pass


class ClassUpdate(ClassBase):
    pass


class ClassResponse(ClassBase):
    id_clase: int

    model_config = {
        "from_attributes": True
    }