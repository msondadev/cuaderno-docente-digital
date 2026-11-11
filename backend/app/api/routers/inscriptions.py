from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.inscription import Inscripcion
from app.models.student import Alumno
from app.models.course import Curso

from app.schemas.inscription import (
    InscriptionCreate,
    InscriptionResponse
)

from app.schemas.inscription import (
    InscriptionCreate,
    InscriptionResponse,
    InscriptionUpdate
)

router = APIRouter(
    prefix="/inscriptions",
    tags=["Inscriptions"]
)


@router.get(
    "/",
    response_model=list[InscriptionResponse]
)
def get_inscriptions(
    db: Session = Depends(get_db)
):
    return db.query(Inscripcion).all()



@router.post(
    "/",
    response_model=InscriptionResponse
)
def create_inscription(
    inscription: InscriptionCreate,
    db: Session = Depends(get_db)
):
    alumno = db.query(Alumno).filter(
        Alumno.id_alumno == inscription.id_alumno
    ).first()

    if not alumno:
        raise HTTPException(
            status_code=404,
            detail="Alumno no encontrado"
        )

    curso = db.query(Curso).filter(
        Curso.id_curso == inscription.id_curso
    ).first()

    if not curso:
        raise HTTPException(
            status_code=404,
            detail="Curso no encontrado"
        )

    nueva_inscripcion = Inscripcion(
        id_alumno=inscription.id_alumno,
        id_curso=inscription.id_curso,
        fecha_inscripcion=inscription.fecha_inscripcion,
        estado_academico=inscription.estado_academico
    )

    db.add(nueva_inscripcion)

    db.commit()

    db.refresh(nueva_inscripcion)

    return nueva_inscripcion


@router.get(
    "/{inscription_id}",
    response_model=InscriptionResponse
)
def get_inscription(
    inscription_id: int,
    db: Session = Depends(get_db)
):
    inscripcion = db.query(Inscripcion).filter(
        Inscripcion.id_inscripcion == inscription_id
    ).first()

    if not inscripcion:
        raise HTTPException(
            status_code=404,
            detail="Inscripción no encontrada"
        )

    return inscripcion


@router.put(
    "/{inscription_id}",
    response_model=InscriptionResponse
)
def update_inscription(
    inscription_id: int,
    inscription: InscriptionUpdate,
    db: Session = Depends(get_db)
):
    inscripcion = db.query(Inscripcion).filter(
        Inscripcion.id_inscripcion == inscription_id
    ).first()

    if not inscripcion:
        raise HTTPException(
            status_code=404,
            detail="Inscripción no encontrada"
        )

    inscripcion.id_alumno = inscription.id_alumno
    inscripcion.id_curso = inscription.id_curso
    inscripcion.fecha_inscripcion = inscription.fecha_inscripcion
    inscripcion.estado_academico = inscription.estado_academico

    db.commit()
    db.refresh(inscripcion)

    return inscripcion


@router.delete(
    "/{inscription_id}"
)
def delete_inscription(
    inscription_id: int,
    db: Session = Depends(get_db)
):
    inscripcion = db.query(Inscripcion).filter(
        Inscripcion.id_inscripcion == inscription_id
    ).first()

    if not inscripcion:
        raise HTTPException(
            status_code=404,
            detail="Inscripción no encontrada"
        )

    db.delete(inscripcion)

    db.commit()

    return {
        "message": "Inscripción eliminada"
    }