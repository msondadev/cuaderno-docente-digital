from app.schemas.user import UserCreate
from app.schemas.user import UserResponse

from app.schemas.course import CourseCreate
from app.schemas.course import CourseResponse

from app.schemas.student import StudentCreate
from app.schemas.student import StudentResponse

from app.schemas.course import CourseUpdate
from app.schemas.student import StudentUpdate

from app.schemas.inscription import InscriptionCreate
from app.schemas.inscription import InscriptionUpdate
from app.schemas.inscription import InscriptionResponse

from app.schemas.quarter import QuarterCreate
from app.schemas.quarter import QuarterUpdate
from app.schemas.quarter import QuarterResponse

from app.schemas.classroom import ClassCreate
from app.schemas.classroom import ClassUpdate
from app.schemas.classroom import ClassResponse

from app.schemas.attendance import AttendanceCreate
from app.schemas.attendance import AttendanceUpdate
from app.schemas.attendance import AttendanceResponse

from app.schemas.attendance_summary import (
    AttendanceSummaryResponse
)

from app.schemas.evaluation import EvaluationCreate
from app.schemas.evaluation import EvaluationUpdate
from app.schemas.evaluation import EvaluationResponse

from app.schemas.grade import GradeCreate
from app.schemas.grade import GradeUpdate
from app.schemas.grade import GradeResponse

from app.schemas.grades_summary import (
    GradesSummaryResponse
)

from app.schemas.academic_status import (
    AcademicStatusResponse
)

from app.schemas.course_statistics import (
    CourseStatisticsResponse
)

from app.schemas.auth import LoginRequest
