from fastapi import FastAPI

from app.models import *
from app.api.routers.users import router as users_router

app = FastAPI(
    title="Cuaderno Docente Digital",
    version="0.1.0"
)

app.include_router(users_router)


@app.get("/")
def root():
    return {
        "message": "API funcionando correctamente"
    }