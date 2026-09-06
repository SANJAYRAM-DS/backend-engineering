from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError
from app.core.exceptions import AppException
import logging

logger = logging.getLogger(__name__)

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handler for custom domain exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handler for Pydantic input validation errors (422 Unprocessable Entity)."""
    details = []
    for err in exc.errors():
        field_path = " -> ".join(str(x) for x in err.get("loc", []))
        details.append({
            "field": field_path,
            "issue": err.get("msg", "Invalid input value.")
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Input validation failed. Please check payload fields.",
                "details": details
            }
        }
    )

async def db_integrity_exception_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """Handler for database constraint violations (409 Conflict)."""
    logger.error(f"Database Integrity Error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "success": False,
            "error": {
                "code": "RESOURCE_CONFLICT",
                "message": "Database constraint violation. Entity already exists or violates relation constraints.",
                "details": []
            }
        }
    )

async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global fallback for unhandled 500 server errors (Hides internal stack traces for security)."""
    logger.exception(f"Unhandled Internal Server Error on {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred on the server. Please try again later.",
                "details": []
            }
        }
    )
