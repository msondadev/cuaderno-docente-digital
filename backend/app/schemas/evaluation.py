from datetime import date

from pydantic import BaseModel

from app.enums.enums import TipoEvaluacion


class EvaluationBase(BaseModel):
    id_curso: int
    id_cuatrimestre: int
    titulo: str
    tipo: TipoEvaluacion
    fecha: date
    enlace_drive: str | None = None


class EvaluationCreate(EvaluationBase):
    pass


class EvaluationUpdate(EvaluationBase):
    pass


class EvaluationResponse(EvaluationBase):
    id_evaluacion: int

    model_config = {
        "from_attributes": True
    }