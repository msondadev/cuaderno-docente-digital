from pydantic import BaseModel


class CourseStatisticsResponse(BaseModel):
    curso_id: int

    cantidad_alumnos: int

    promedio_curso: float

    ausentismo_promedio: float