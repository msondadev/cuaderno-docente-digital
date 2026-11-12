from pydantic import BaseModel


class AcademicStatusResponse(BaseModel):
    alumno_id: int

    curso_id: int

    promedio: float

    estado: str