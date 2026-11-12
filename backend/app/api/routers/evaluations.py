from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.evaluation import Evaluacion
from app.models.course import Curso
from app.models.quarter import Cuatrimestre

from app.schemas.evaluation import (
    EvaluationCreate,
    EvaluationUpdate,
    EvaluationResponse
)

router = APIRouter(
    prefix="/evaluations",
    tags=["Evaluations"]
)


@router.get(
    "/",
    response_model=list[EvaluationResponse]
)
def get_evaluations(
    db: Session = Depends(get_db)
):
    return db.query(Evaluacion).all()


@router.post(
    "/",
    response_model=EvaluationResponse
)
def create_evaluation(
    evaluation: EvaluationCreate,
    db: Session = Depends(get_db)
):
    curso = db.query(Curso).filter(
        Curso.id_curso == evaluation.id_curso
    ).first()

    if not curso:
        raise HTTPException(
            status_code=404,
            detail="Curso no encontrado"
        )

    cuatrimestre = db.query(Cuatrimestre).filter(
        Cuatrimestre.id_cuatrimestre == evaluation.id_cuatrimestre
    ).first()

    if not cuatrimestre:
        raise HTTPException(
            status_code=404,
            detail="Cuatrimestre no encontrado"
        )

    nueva_evaluacion = Evaluacion(
        id_curso=evaluation.id_curso,
        id_cuatrimestre=evaluation.id_cuatrimestre,
        titulo=evaluation.titulo,
        tipo=evaluation.tipo,
        fecha=evaluation.fecha,
        enlace_drive=evaluation.enlace_drive
    )

    db.add(nueva_evaluacion)

    db.commit()

    db.refresh(nueva_evaluacion)

    return nueva_evaluacion


@router.get(
    "/{evaluation_id}",
    response_model=EvaluationResponse
)
def get_evaluation(
    evaluation_id: int,
    db: Session = Depends(get_db)
):
    evaluacion = db.query(Evaluacion).filter(
        Evaluacion.id_evaluacion == evaluation_id
    ).first()

    if not evaluacion:
        raise HTTPException(
            status_code=404,
            detail="Evaluación no encontrada"
        )

    return evaluacion


@router.put(
    "/{evaluation_id}",
    response_model=EvaluationResponse
)
def update_evaluation(
    evaluation_id: int,
    evaluation: EvaluationUpdate,
    db: Session = Depends(get_db)
):
    evaluacion = db.query(Evaluacion).filter(
        Evaluacion.id_evaluacion == evaluation_id
    ).first()

    if not evaluacion:
        raise HTTPException(
            status_code=404,
            detail="Evaluación no encontrada"
        )

    evaluacion.id_curso = evaluation.id_curso
    evaluacion.id_cuatrimestre = evaluation.id_cuatrimestre
    evaluacion.titulo = evaluation.titulo
    evaluacion.tipo = evaluation.tipo
    evaluacion.fecha = evaluation.fecha
    evaluacion.enlace_drive = evaluation.enlace_drive

    db.commit()
    db.refresh(evaluacion)

    return evaluacion


@router.delete(
    "/{evaluation_id}"
)
def delete_evaluation(
    evaluation_id: int,
    db: Session = Depends(get_db)
):
    evaluacion = db.query(Evaluacion).filter(
        Evaluacion.id_evaluacion == evaluation_id
    ).first()

    if not evaluacion:
        raise HTTPException(
            status_code=404,
            detail="Evaluación no encontrada"
        )

    db.delete(evaluacion)

    db.commit()

    return {
        "message": "Evaluación eliminada"
    }