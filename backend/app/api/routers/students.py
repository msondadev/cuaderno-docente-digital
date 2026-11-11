from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.student import Alumno

from app.schemas.student import (
    StudentCreate,
    StudentResponse,
    StudentUpdate
)

router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.get(
    "/",
    response_model=list[StudentResponse]
)
def get_students(
    db: Session = Depends(get_db)
):
    return db.query(Alumno).all()


@router.post(
    "/",
    response_model=StudentResponse
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):
    nuevo_alumno = Alumno(
        nombre=student.nombre,
        apellido=student.apellido,
        email=student.email
    )

    db.add(nuevo_alumno)

    db.commit()

    db.refresh(nuevo_alumno)

    return nuevo_alumno


@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    alumno = db.query(Alumno).filter(
        Alumno.id_alumno == student_id
    ).first()

    if not alumno:
        raise HTTPException(
            status_code=404,
            detail="Alumno no encontrado"
        )

    return alumno


@router.put(
    "/{student_id}",
    response_model=StudentResponse
)
def update_student(
    student_id: int,
    student: StudentUpdate,
    db: Session = Depends(get_db)
):
    alumno = db.query(Alumno).filter(
        Alumno.id_alumno == student_id
    ).first()

    if not alumno:
        raise HTTPException(
            status_code=404,
            detail="Alumno no encontrado"
        )

    alumno.nombre = student.nombre
    alumno.apellido = student.apellido
    alumno.email = student.email

    db.commit()
    db.refresh(alumno)

    return alumno


@router.delete(
    "/{student_id}"
)
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    alumno = db.query(Alumno).filter(
        Alumno.id_alumno == student_id
    ).first()

    if not alumno:
        raise HTTPException(
            status_code=404,
            detail="Alumno no encontrado"
        )

    db.delete(alumno)

    db.commit()

    return {
        "message": "Alumno eliminado"
    }