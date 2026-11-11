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