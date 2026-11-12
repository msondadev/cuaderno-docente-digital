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

from app.models.attendance import Asistencia
from app.models.classroom import Clase
from app.models.course import Curso

from app.schemas.attendance_summary import (
    AttendanceSummaryResponse
)

from app.models.grade import Calificacion
from app.models.evaluation import Evaluacion

from app.schemas.grades_summary import (
    GradesSummaryResponse
)

from app.schemas.academic_status import (
    AcademicStatusResponse
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


@router.get(
    "/{student_id}/attendance-summary",
    response_model=AttendanceSummaryResponse
)
def get_attendance_summary(
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

    asistencias = (
        db.query(Asistencia)
        .join(Clase)
        .filter(
            Asistencia.id_alumno == student_id,
            Clase.estado == "DICTADA"
        )
        .all()
    )

    clases_dictadas = len(asistencias)

    faltas_acumuladas = 0.0

    for asistencia in asistencias:

        if asistencia.estado == "A":
            faltas_acumuladas += 1.0

        elif asistencia.estado == "T":
            faltas_acumuladas += 0.5

    curso = (
        db.query(Curso)
        .join(Clase)
        .join(Asistencia)
        .filter(
            Asistencia.id_alumno == student_id
        )
        .first()
    )

    max_faltas = curso.max_faltas if curso else 0

    faltas_restantes = max_faltas - faltas_acumuladas

    if clases_dictadas == 0:
        porcentaje_asistencia = 100

    else:
        porcentaje_asistencia = (
            (
                clases_dictadas -
                faltas_acumuladas
            )
            / clases_dictadas
        ) * 100

    return {
        "alumno_id": student_id,
        "clases_dictadas": clases_dictadas,
        "faltas_acumuladas": faltas_acumuladas,
        "faltas_restantes": faltas_restantes,
        "porcentaje_asistencia": round(
            porcentaje_asistencia,
            2
        )
    }


@router.get(
    "/{student_id}/courses/{course_id}/attendance-summary",
    response_model=AttendanceSummaryResponse
)
def get_attendance_summary_by_course(
    student_id: int,
    course_id: int,
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

    curso = db.query(Curso).filter(
        Curso.id_curso == course_id
    ).first()

    if not curso:
        raise HTTPException(
            status_code=404,
            detail="Curso no encontrado"
        )

    asistencias = (
        db.query(Asistencia)
        .join(Clase)
        .filter(
            Asistencia.id_alumno == student_id,
            Clase.id_curso == course_id,
            Clase.estado == "DICTADA"
        )
        .all()
    )

    clases_dictadas = len(asistencias)

    faltas_acumuladas = 0.0

    for asistencia in asistencias:
        if asistencia.estado == "A":
            faltas_acumuladas += 1.0

        elif asistencia.estado == "T":
            faltas_acumuladas += 0.5

    faltas_restantes = (
        curso.max_faltas - faltas_acumuladas
    )

    if clases_dictadas == 0:
        porcentaje_asistencia = 100

    else:
        porcentaje_asistencia = (
            (
                clases_dictadas -
                faltas_acumuladas
            )
            / clases_dictadas
        ) * 100

    return {
        "alumno_id": student_id,
        "clases_dictadas": clases_dictadas,
        "faltas_acumuladas": faltas_acumuladas,
        "faltas_restantes": faltas_restantes,
        "porcentaje_asistencia": round(
            porcentaje_asistencia,
            2
        )
    }


@router.get(
    "/{student_id}/courses/{course_id}/grades-summary",
    response_model=GradesSummaryResponse
)
def get_grades_summary(
    student_id: int,
    course_id: int,
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

    curso = db.query(Curso).filter(
        Curso.id_curso == course_id
    ).first()

    if not curso:
        raise HTTPException(
            status_code=404,
            detail="Curso no encontrado"
        )

    calificaciones = (
        db.query(Calificacion)
        .join(Evaluacion)
        .filter(
            Calificacion.id_alumno == student_id,
            Evaluacion.id_curso == course_id,
            Calificacion.nota.is_not(None)
        )
        .all()
    )

    cantidad_evaluaciones = len(calificaciones)

    if cantidad_evaluaciones == 0:
        promedio = 0

    else:
        promedio = sum(
            c.nota
            for c in calificaciones
        ) / cantidad_evaluaciones

    return {
        "alumno_id": student_id,
        "curso_id": course_id,
        "cantidad_evaluaciones": cantidad_evaluaciones,
        "promedio": round(promedio, 2)
    }


@router.get(
    "/{student_id}/courses/{course_id}/academic-status",
    response_model=AcademicStatusResponse
)
def get_academic_status(
    student_id: int,
    course_id: int,
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

    curso = db.query(Curso).filter(
        Curso.id_curso == course_id
    ).first()

    if not curso:
        raise HTTPException(
            status_code=404,
            detail="Curso no encontrado"
        )

    calificaciones = (
        db.query(Calificacion)
        .join(Evaluacion)
        .filter(
            Calificacion.id_alumno == student_id,
            Evaluacion.id_curso == course_id,
            Calificacion.nota.is_not(None)
        )
        .all()
    )

    cantidad = len(calificaciones)

    if cantidad == 0:
        promedio = 0

    else:
        promedio = (
            sum(c.nota for c in calificaciones)
            / cantidad
        )

    if promedio >= 8:
        estado = "PROMOVIDO"

    elif promedio >= 6:
        estado = "REGULAR"

    else:
        estado = "LIBRE"

    return {
        "alumno_id": student_id,
        "curso_id": course_id,
        "promedio": round(promedio, 2),
        "estado": estado
    }