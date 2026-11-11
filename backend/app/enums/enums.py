from enum import Enum


class RolUsuario(str, Enum):
    DOCENTE = "DOCENTE"
    PRECEPTOR = "PRECEPTOR"


class RegimenCurso(str, Enum):
    SECUNDARIA = "SECUNDARIA"
    TERCIARIO = "TERCIARIO"


class EstadoAcademico(str, Enum):
    REGULAR = "REGULAR"
    LIBRE = "LIBRE"
    PROMOVIDO = "PROMOVIDO"


class EstadoClase(str, Enum):
    DICTADA = "DICTADA"
    SIN_ACTIVIDAD = "SIN_ACTIVIDAD"


class EstadoAsistencia(str, Enum):
    PRESENTE = "P"
    AUSENTE = "A"
    TARDANZA = "T"


class TipoEvaluacion(str, Enum):
    PARCIAL = "PARCIAL"
    FINAL = "FINAL"
    TP = "TP"
    AVANCE = "AVANCE"


class EstadoTP(str, Enum):
    PENDIENTE = "PENDIENTE"
    ENTREGADO = "ENTREGADO"
    REHACER = "REHACER"
    APROBADO = "APROBADO"
