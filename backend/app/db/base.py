from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.models.user import Usuario
from app.models.course import Curso
from app.models.student import Alumno
from app.models.inscription import Inscripcion
from app.models.quarter import Cuatrimestre
from app.models.classroom import Clase
from app.models.attendance import Asistencia
from app.models.evaluation import Evaluacion
from app.models.grade import Calificacion