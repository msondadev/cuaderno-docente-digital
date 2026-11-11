from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.quarter import Cuatrimestre

from app.schemas.quarter import (
    QuarterCreate,
    QuarterUpdate,
    QuarterResponse
)

router = APIRouter(
    prefix="/quarters",
    tags=["Quarters"]
)


@router.get(
    "/",
    response_model=list[QuarterResponse]
)
def get_quarters(
    db: Session = Depends(get_db)
):
    return db.query(Cuatrimestre).all()


@router.post(
    "/",
    response_model=QuarterResponse
)
def create_quarter(
    quarter: QuarterCreate,
    db: Session = Depends(get_db)
):
    nuevo_cuatrimestre = Cuatrimestre(
        anio=quarter.anio,
        numero=quarter.numero,
        fecha_inicio=quarter.fecha_inicio,
        fecha_fin=quarter.fecha_fin
    )

    db.add(nuevo_cuatrimestre)

    db.commit()

    db.refresh(nuevo_cuatrimestre)

    return nuevo_cuatrimestre


@router.get(
    "/{quarter_id}",
    response_model=QuarterResponse
)
def get_quarter(
    quarter_id: int,
    db: Session = Depends(get_db)
):
    cuatrimestre = db.query(Cuatrimestre).filter(
        Cuatrimestre.id_cuatrimestre == quarter_id
    ).first()

    if not cuatrimestre:
        raise HTTPException(
            status_code=404,
            detail="Cuatrimestre no encontrado"
        )

    return cuatrimestre


@router.put(
    "/{quarter_id}",
    response_model=QuarterResponse
)
def update_quarter(
    quarter_id: int,
    quarter: QuarterUpdate,
    db: Session = Depends(get_db)
):
    cuatrimestre = db.query(Cuatrimestre).filter(
        Cuatrimestre.id_cuatrimestre == quarter_id
    ).first()

    if not cuatrimestre:
        raise HTTPException(
            status_code=404,
            detail="Cuatrimestre no encontrado"
        )

    cuatrimestre.anio = quarter.anio
    cuatrimestre.numero = quarter.numero
    cuatrimestre.fecha_inicio = quarter.fecha_inicio
    cuatrimestre.fecha_fin = quarter.fecha_fin

    db.commit()
    db.refresh(cuatrimestre)

    return cuatrimestre


@router.delete(
    "/{quarter_id}"
)
def delete_quarter(
    quarter_id: int,
    db: Session = Depends(get_db)
):
    cuatrimestre = db.query(Cuatrimestre).filter(
        Cuatrimestre.id_cuatrimestre == quarter_id
    ).first()

    if not cuatrimestre:
        raise HTTPException(
            status_code=404,
            detail="Cuatrimestre no encontrado"
        )

    db.delete(cuatrimestre)

    db.commit()

    return {
        "message": "Cuatrimestre eliminado"
    }