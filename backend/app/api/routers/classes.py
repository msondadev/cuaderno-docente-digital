from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.classroom import Clase
from app.models.course import Curso
from app.models.quarter import Cuatrimestre

from app.schemas.classroom import (
    ClassCreate,
    ClassUpdate,
    ClassResponse
)

router = APIRouter(
    prefix="/classes",
    tags=["Classes"]
)


@router.get(
    "/",
    response_model=list[ClassResponse]
)
def get_classes(
    db: Session = Depends(get_db)
):
    return db.query(Clase).all()


@router.post(
    "/",
    response_model=ClassResponse
)
def create_class(
    classroom: ClassCreate,
    db: Session = Depends(get_db)
):
    curso = db.query(Curso).filter(
        Curso.id_curso == classroom.id_curso
    ).first()

    if not curso:
        raise HTTPException(
            status_code=404,
            detail="Curso no encontrado"
        )

    cuatrimestre = db.query(Cuatrimestre).filter(
        Cuatrimestre.id_cuatrimestre == classroom.id_cuatrimestre
    ).first()

    if not cuatrimestre:
        raise HTTPException(
            status_code=404,
            detail="Cuatrimestre no encontrado"
        )

    nueva_clase = Clase(
        id_curso=classroom.id_curso,
        id_cuatrimestre=classroom.id_cuatrimestre,
        fecha=classroom.fecha,
        estado=classroom.estado,
        tema=classroom.tema
    )

    db.add(nueva_clase)

    db.commit()

    db.refresh(nueva_clase)

    return nueva_clase


@router.get(
    "/{class_id}",
    response_model=ClassResponse
)
def get_class(
    class_id: int,
    db: Session = Depends(get_db)
):
    clase = db.query(Clase).filter(
        Clase.id_clase == class_id
    ).first()

    if not clase:
        raise HTTPException(
            status_code=404,
            detail="Clase no encontrada"
        )

    return clase


@router.put(
    "/{class_id}",
    response_model=ClassResponse
)
def update_class(
    class_id: int,
    classroom: ClassUpdate,
    db: Session = Depends(get_db)
):
    clase = db.query(Clase).filter(
        Clase.id_clase == class_id
    ).first()

    if not clase:
        raise HTTPException(
            status_code=404,
            detail="Clase no encontrada"
        )

    clase.id_curso = classroom.id_curso
    clase.id_cuatrimestre = classroom.id_cuatrimestre
    clase.fecha = classroom.fecha
    clase.estado = classroom.estado
    clase.tema = classroom.tema

    db.commit()
    db.refresh(clase)

    return clase


@router.delete(
    "/{class_id}"
)
def delete_class(
    class_id: int,
    db: Session = Depends(get_db)
):
    clase = db.query(Clase).filter(
        Clase.id_clase == class_id
    ).first()

    if not clase:
        raise HTTPException(
            status_code=404,
            detail="Clase no encontrada"
        )

    db.delete(clase)

    db.commit()

    return {
        "message": "Clase eliminada"
    }