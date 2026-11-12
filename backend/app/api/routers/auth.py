from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.user import Usuario

from app.schemas.auth import LoginRequest

from app.core.security import (
    verify_password
)


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login")
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.email == credentials.email
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )

    if not verify_password(
        credentials.password,
        usuario.contrasena_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Credenciales inválidas"
        )

    return {
        "message": "Login correcto",
        "usuario": usuario.email
    }