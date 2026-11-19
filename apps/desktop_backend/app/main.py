from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

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


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    detail = exc.detail

    if isinstance(detail, dict):
        error = detail
    else:
        error = {
            "code": {
                404: "NOT_FOUND",
                400: "BAD_REQUEST",
                409: "CONFLICT",
                503: "SERVICE_UNAVAILABLE"
            }.get(exc.status_code, "HTTP_ERROR"),
            "message": str(detail),
            "recoverable": exc.status_code >= 500,
            "details": {}
        }

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": error}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "The request data is invalid.",
                "recoverable": False,
                "details": {}
            }
        }
    )


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
                "error": {
                    "code": "BACKEND_UNAVAILABLE",
                    "message": "Backend is temporarily unavailable.",
                    "recoverable": True,
                    "details": {}
                }
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
