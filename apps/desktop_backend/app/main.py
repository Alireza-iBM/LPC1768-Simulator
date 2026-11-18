from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.sessions import router as sessions_router
from app.api.simulation import router as simulation_router
from app.websocket.websocket_router import router as websocket_router


app = FastAPI(
    title="LPC1768 Simulator Backend",
    description="Desktop Backend for LPC1768 Simulator",
    version="0.1.0"
)


# Backend availability state
app.state.backend_available = True


@app.middleware("http")
async def backend_availability_middleware(request, call_next):

    control_path = "/api/v1/test/backend-availability"

    if (
        not app.state.backend_available
        and request.url.path != control_path
    ):
        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "error": "BACKEND_UNAVAILABLE",
                "message": "Backend is temporarily unavailable"
            }
        )

    return await call_next(request)


@app.get("/")
def root():
    return {
        "message": "LPC1768 Simulator Backend is running"
    }


@app.get("/api/v1/health")
def health_check():

    return {
        "status": "ok",
        "service": "desktop-backend",
        "backend_available": app.state.backend_available
    }


@app.post("/api/v1/test/backend-availability")
def set_backend_availability(available: bool):

    app.state.backend_available = available

    return {
        "success": True,
        "backend_available": app.state.backend_available,
        "message": (
            "Backend is available"
            if available
            else "Backend is unavailable"
        )
    }


app.include_router(sessions_router, prefix="/api/v1")
app.include_router(simulation_router, prefix="/api/v1")
app.include_router(websocket_router)