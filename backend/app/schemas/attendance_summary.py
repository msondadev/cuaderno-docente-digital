from pydantic import BaseModel


class AttendanceSummaryResponse(BaseModel):
    alumno_id: int

    clases_dictadas: int

    faltas_acumuladas: float

    faltas_restantes: float

    porcentaje_asistencia: float
