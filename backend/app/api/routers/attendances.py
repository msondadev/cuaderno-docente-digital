from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.attendance import Asistencia
from app.models.classroom import Clase
from app.models.student import Alumno

from app.schemas.attendance import (
    AttendanceCreate,
    AttendanceUpdate,
    AttendanceResponse
)

router = APIRouter(
    prefix="/attendances",
    tags=["Attendances"]
)


@router.get(
    "/",
    response_model=list[AttendanceResponse]
)
def get_attendances(
    db: Session = Depends(get_db)
):
    return db.query(Asistencia).all()


@router.post(
    "/",
    response_model=AttendanceResponse
)
def create_attendance(
    attendance: AttendanceCreate,
    db: Session = Depends(get_db)
):
    clase = db.query(Clase).filter(
        Clase.id_clase == attendance.id_clase
    ).first()

    if not clase:
        raise HTTPException(
            status_code=404,
            detail="Clase no encontrada"
        )

    alumno = db.query(Alumno).filter(
        Alumno.id_alumno == attendance.id_alumno
    ).first()

    if not alumno:
        raise HTTPException(
            status_code=404,
            detail="Alumno no encontrado"
        )

    nueva_asistencia = Asistencia(
        id_clase=attendance.id_clase,
        id_alumno=attendance.id_alumno,
        estado=attendance.estado,
        observacion=attendance.observacion
    )

    db.add(nueva_asistencia)

    db.commit()

    db.refresh(nueva_asistencia)

    return nueva_asistencia


@router.get(
    "/{attendance_id}",
    response_model=AttendanceResponse
)
def get_attendance(
    attendance_id: int,
    db: Session = Depends(get_db)
):
    asistencia = db.query(Asistencia).filter(
        Asistencia.id_asistencia == attendance_id
    ).first()

    if not asistencia:
        raise HTTPException(
            status_code=404,
            detail="Asistencia no encontrada"
        )

    return asistencia


@router.put(
    "/{attendance_id}",
    response_model=AttendanceResponse
)
def update_attendance(
    attendance_id: int,
    attendance: AttendanceUpdate,
    db: Session = Depends(get_db)
):
    asistencia = db.query(Asistencia).filter(
        Asistencia.id_asistencia == attendance_id
    ).first()

    if not asistencia:
        raise HTTPException(
            status_code=404,
            detail="Asistencia no encontrada"
        )

    asistencia.id_clase = attendance.id_clase
    asistencia.id_alumno = attendance.id_alumno
    asistencia.estado = attendance.estado
    asistencia.observacion = attendance.observacion

    db.commit()
    db.refresh(asistencia)

    return asistencia


@router.delete(
    "/{attendance_id}"
)
def delete_attendance(
    attendance_id: int,
    db: Session = Depends(get_db)
):
    asistencia = db.query(Asistencia).filter(
        Asistencia.id_asistencia == attendance_id
    ).first()

    if not asistencia:
        raise HTTPException(
            status_code=404,
            detail="Asistencia no encontrada"
        )

    db.delete(asistencia)

    db.commit()

    return {
        "message": "Asistencia eliminada"
    }