from fastapi import FastAPI

from app.models import *
from app.api.routers.users import router as users_router
from app.api.routers.courses import router as courses_router
from app.api.routers.students import router as students_router
from app.api.routers.inscriptions import router as inscriptions_router
from app.api.routers.quarters import router as quarters_router
from app.api.routers.classes import router as classes_router

app = FastAPI(
    title="Cuaderno Docente Digital",
    version="0.1.0"
)

app.include_router(users_router)
app.include_router(courses_router)
app.include_router(students_router)
app.include_router(inscriptions_router)
app.include_router(quarters_router)
app.include_router(classes_router)



@app.get("/")
def root():
    return {
        "message": "API funcionando correctamente"
    }