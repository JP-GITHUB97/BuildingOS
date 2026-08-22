from fastapi import FastAPI

app = FastAPI(
    title="BuildingOS API",
    description="API de supervision et de gestion des bâtiments",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "buildingos-backend",
    }