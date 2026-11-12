from pydantic import BaseModel

from app.enums.enums import EstadoAsistencia


class AttendanceBase(BaseModel):
    id_clase: int
    id_alumno: int
    estado: EstadoAsistencia
    observacion: str | None = None


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceUpdate(AttendanceBase):
    pass


class AttendanceResponse(AttendanceBase):
    id_asistencia: int

    model_config = {
        "from_attributes": True
    }