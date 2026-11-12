from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.grade import Calificacion
from app.models.evaluation import Evaluacion
from app.models.student import Alumno

from app.schemas.grade import (
    GradeCreate,
    GradeUpdate,
    GradeResponse
)

router = APIRouter(
    prefix="/grades",
    tags=["Grades"]
)


@router.get(
    "/",
    response_model=list[GradeResponse]
)
def get_grades(
    db: Session = Depends(get_db)
):
    return db.query(Calificacion).all()


@router.post(
    "/",
    response_model=GradeResponse
)
def create_grade(
    grade: GradeCreate,
    db: Session = Depends(get_db)
):
    evaluacion = db.query(Evaluacion).filter(
        Evaluacion.id_evaluacion == grade.id_evaluacion
    ).first()

    if not evaluacion:
        raise HTTPException(
            status_code=404,
            detail="Evaluación no encontrada"
        )

    alumno = db.query(Alumno).filter(
        Alumno.id_alumno == grade.id_alumno
    ).first()

    if not alumno:
        raise HTTPException(
            status_code=404,
            detail="Alumno no encontrado"
        )

    nueva_calificacion = Calificacion(
        id_evaluacion=grade.id_evaluacion,
        id_alumno=grade.id_alumno,
        nota=grade.nota,
        estado_tp=grade.estado_tp,
        valoracion=grade.valoracion
    )

    db.add(nueva_calificacion)

    db.commit()

    db.refresh(nueva_calificacion)

    return nueva_calificacion


@router.get(
    "/{grade_id}",
    response_model=GradeResponse
)
def get_grade(
    grade_id: int,
    db: Session = Depends(get_db)
):
    calificacion = db.query(Calificacion).filter(
        Calificacion.id_calificacion == grade_id
    ).first()

    if not calificacion:
        raise HTTPException(
            status_code=404,
            detail="Calificación no encontrada"
        )

    return calificacion


@router.put(
    "/{grade_id}",
    response_model=GradeResponse
)
def update_grade(
    grade_id: int,
    grade: GradeUpdate,
    db: Session = Depends(get_db)
):
    calificacion = db.query(Calificacion).filter(
        Calificacion.id_calificacion == grade_id
    ).first()

    if not calificacion:
        raise HTTPException(
            status_code=404,
            detail="Calificación no encontrada"
        )

    calificacion.id_evaluacion = grade.id_evaluacion
    calificacion.id_alumno = grade.id_alumno
    calificacion.nota = grade.nota
    calificacion.estado_tp = grade.estado_tp
    calificacion.valoracion = grade.valoracion

    db.commit()
    db.refresh(calificacion)

    return calificacion


@router.delete(
    "/{grade_id}"
)
def delete_grade(
    grade_id: int,
    db: Session = Depends(get_db)
):
    calificacion = db.query(Calificacion).filter(
        Calificacion.id_calificacion == grade_id
    ).first()

    if not calificacion:
        raise HTTPException(
            status_code=404,
            detail="Calificación no encontrada"
        )

    db.delete(calificacion)

    db.commit()

    return {
        "message": "Calificación eliminada"
    }