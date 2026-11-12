from pydantic import BaseModel

from app.enums.enums import EstadoTP


class GradeBase(BaseModel):
    id_evaluacion: int
    id_alumno: int
    nota: float | None = None
    estado_tp: EstadoTP | None = None
    valoracion: str | None = None


class GradeCreate(GradeBase):
    pass


class GradeUpdate(GradeBase):
    pass


class GradeResponse(GradeBase):
    id_calificacion: int

    model_config = {
        "from_attributes": True
    }