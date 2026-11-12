from pydantic import BaseModel


class GradesSummaryResponse(BaseModel):
    alumno_id: int

    curso_id: int

    cantidad_evaluaciones: int

    promedio: float