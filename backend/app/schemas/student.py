from pydantic import BaseModel
from pydantic import EmailStr


class StudentBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr | None = None


class StudentCreate(StudentBase):
    pass


class StudentResponse(StudentBase):
    id_alumno: int

    model_config = {
        "from_attributes": True
    }