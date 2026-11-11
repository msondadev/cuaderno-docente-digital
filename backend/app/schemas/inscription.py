from datetime import date

from pydantic import BaseModel

from app.enums.enums import EstadoAcademico


class InscriptionBase(BaseModel):
    id_alumno: int
    id_curso: int
    fecha_inscripcion: date
    estado_academico: EstadoAcademico | None = None


class InscriptionCreate(InscriptionBase):
    pass


class InscriptionUpdate(InscriptionBase):
    pass


class InscriptionResponse(InscriptionBase):
    id_inscripcion: int

    model_config = {
        "from_attributes": True
    }
