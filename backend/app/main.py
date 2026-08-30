from fastapi import FastAPI

from app.api.buildings import router as buildings_router
from app.api.rooms import router as rooms_router
from app.api.equipment import router as equipment_router
from app.api.points import router as points_router


app = FastAPI(
    title="BuildingOS API",
    description="API de supervision et de gestion des bâtiments",
    version="0.1.0",
)


app.include_router(buildings_router)
app.include_router(rooms_router)
app.include_router(equipment_router)
app.include_router(points_router)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "buildingos-backend",
    }