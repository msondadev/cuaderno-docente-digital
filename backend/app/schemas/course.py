from pydantic import BaseModel

from app.enums.enums import RegimenCurso


class CourseBase(BaseModel):
    materia: str
    division: str
    institucion: str
    regimen: RegimenCurso
    max_faltas: float
    porcentaje_minimo: float | None = None
    enlace_drive: str | None = None


class CourseCreate(CourseBase):
    id_docente: int

class CourseUpdate(CourseBase):
    id_docente: int

class CourseResponse(CourseBase):
    id_curso: int
    id_docente: int

    model_config = {
        "from_attributes": True
    }