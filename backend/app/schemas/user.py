from pydantic import BaseModel
from pydantic import EmailStr

from app.enums.enums import RolUsuario


class UserBase(BaseModel):
    nombre: str
    apellido: str
    email: EmailStr
    rol: RolUsuario


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id_usuario: int
    activo: bool

    model_config = {
        "from_attributes": True
    }