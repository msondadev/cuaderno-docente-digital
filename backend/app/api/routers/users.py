from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.user import Usuario

from app.schemas.user import UserCreate
from app.schemas.user import UserResponse

from fastapi import HTTPException

from app.schemas.user import UserUpdate


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get(
    "/",
    response_model=list[UserResponse]
)
def get_users(
    db: Session = Depends(get_db)
):
    return db.query(Usuario).all()

@router.get(
    "/{user_id}",
    response_model=UserResponse
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.id_usuario == user_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario


@router.post(
    "/",
    response_model=UserResponse
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    nuevo_usuario = Usuario(
        nombre=user.nombre,
        apellido=user.apellido,
        email=user.email,
        contrasena_hash=user.password,
        rol=user.rol,
        activo=True
    )

    db.add(nuevo_usuario)

    db.commit()

    db.refresh(nuevo_usuario)

    return nuevo_usuario


@router.put(
    "/{user_id}",
    response_model=UserResponse
)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.id_usuario == user_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    usuario.nombre = user.nombre
    usuario.apellido = user.apellido
    usuario.email = user.email
    usuario.rol = user.rol
    usuario.activo = user.activo

    db.commit()
    db.refresh(usuario)

    return usuario


@router.delete(
    "/{user_id}"
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    usuario = db.query(Usuario).filter(
        Usuario.id_usuario == user_id
    ).first()

    if not usuario:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    db.delete(usuario)

    db.commit()

    return {
        "message": "Usuario eliminado"
    }
