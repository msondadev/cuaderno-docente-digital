from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.course import Curso

from app.schemas.course import (
    CourseCreate,
    CourseResponse
)

from fastapi import HTTPException

from app.schemas.course import (
    CourseCreate,
    CourseResponse,
    CourseUpdate
)

from app.models.user import Usuario


from app.models.inscription import Inscripcion
from app.models.attendance import Asistencia
from app.models.classroom import Clase
from app.models.grade import Calificacion
from app.models.evaluation import Evaluacion

from app.schemas.course_statistics import (
    CourseStatisticsResponse
)


router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.get(
    "/",
    response_model=list[CourseResponse]
)
def get_courses(
    db: Session = Depends(get_db)
):
    return db.query(Curso).all()


@router.post(
    "/",
    response_model=CourseResponse
)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):
    docente = db.query(Usuario).filter(
        Usuario.id_usuario == course.id_docente
    ).first()

    if not docente:
        raise HTTPException(
            status_code=404,
            detail="Docente no encontrado"
        )

    nuevo_curso = Curso(
        materia=course.materia,
        division=course.division,
        institucion=course.institucion,
        regimen=course.regimen,
        max_faltas=course.max_faltas,
        porcentaje_minimo=course.porcentaje_minimo,
        enlace_drive=course.enlace_drive,
        id_docente=course.id_docente
    )

    db.add(nuevo_curso)

    db.commit()

    db.refresh(nuevo_curso)

    return nuevo_curso


@router.get(
    "/{course_id}",
    response_model=CourseResponse
)
def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    curso = db.query(Curso).filter(
        Curso.id_curso == course_id
    ).first()

    if not curso:
        raise HTTPException(
            status_code=404,
            detail="Curso no encontrado"
        )

    return curso


@router.put(
    "/{course_id}",
    response_model=CourseResponse
)
def update_course(
    course_id: int,
    course: CourseUpdate,
    db: Session = Depends(get_db)
):
    curso = db.query(Curso).filter(
        Curso.id_curso == course_id
    ).first()

    if not curso:
        raise HTTPException(
            status_code=404,
            detail="Curso no encontrado"
        )

    docente = db.query(Usuario).filter(
        Usuario.id_usuario == course.id_docente
    ).first()

    if not docente:
        raise HTTPException(
            status_code=404,
            detail="Docente no encontrado"
        )

    curso.materia = course.materia
    curso.division = course.division
    curso.institucion = course.institucion
    curso.regimen = course.regimen
    curso.max_faltas = course.max_faltas
    curso.porcentaje_minimo = course.porcentaje_minimo
    curso.enlace_drive = course.enlace_drive
    curso.id_docente = course.id_docente

    db.commit()
    db.refresh(curso)

    return curso


@router.delete(
    "/{course_id}"
)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db)
):
    curso = db.query(Curso).filter(
        Curso.id_curso == course_id
    ).first()

    if not curso:
        raise HTTPException(
            status_code=404,
            detail="Curso no encontrado"
        )

    db.delete(curso)

    db.commit()

    return {
        "message": "Curso eliminado"
    }


@router.get(
    "/{course_id}/statistics",
    response_model=CourseStatisticsResponse
)
def get_course_statistics(
    course_id: int,
    db: Session = Depends(get_db)
):
    curso = db.query(Curso).filter(
        Curso.id_curso == course_id
    ).first()

    if not curso:
        raise HTTPException(
            status_code=404,
            detail="Curso no encontrado"
        )

    inscripciones = (
        db.query(Inscripcion)
        .filter(
            Inscripcion.id_curso == course_id
        )
        .all()
    )

    cantidad_alumnos = len(inscripciones)

    calificaciones = (
        db.query(Calificacion)
        .join(Evaluacion)
        .filter(
            Evaluacion.id_curso == course_id,
            Calificacion.nota.is_not(None)
        )
        .all()
    )

    if len(calificaciones) == 0:
        promedio_curso = 0

    else:
        promedio_curso = (
            sum(c.nota for c in calificaciones)
            / len(calificaciones)
        )

    asistencias = (
        db.query(Asistencia)
        .join(Clase)
        .filter(
            Clase.id_curso == course_id,
            Clase.estado == "DICTADA"
        )
        .all()
    )

    if len(asistencias) == 0:
        ausentismo_promedio = 0

    else:
        faltas = 0

        for asistencia in asistencias:

            if asistencia.estado == "A":
                faltas += 1

            elif asistencia.estado == "T":
                faltas += 0.5

        ausentismo_promedio = (
            faltas / len(asistencias)
        ) * 100

    return {
        "curso_id": course_id,
        "cantidad_alumnos": cantidad_alumnos,
        "promedio_curso": round(
            promedio_curso,
            2
        ),
        "ausentismo_promedio": round(
            ausentismo_promedio,
            2
        )
    }