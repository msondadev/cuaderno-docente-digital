from datetime import date

from pydantic import BaseModel


class QuarterBase(BaseModel):
    anio: int
    numero: int
    fecha_inicio: date
    fecha_fin: date


class QuarterCreate(QuarterBase):
    pass


class QuarterUpdate(QuarterBase):
    pass


class QuarterResponse(QuarterBase):
    id_cuatrimestre: int

    model_config = {
        "from_attributes": True
    }