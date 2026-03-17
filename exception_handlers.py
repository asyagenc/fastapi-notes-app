import logging
from fastapi import Request, HTTPException, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def error_response(message: str, code: str, field=None):
    return {
        "success": False,
        "message": message,
        "error_code": code,
        "field": field
    }


def register_exception_handlers(app: FastAPI):
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        first_error = exc.errors()[0]
        loc = first_error.get("loc", [])
        error_type = first_error.get("type", "")

        if error_type == "json_invalid":
            return JSONResponse(
                status_code=422,
                content=error_response("Invalid JSON format.", "INVALID_JSON")
            )

        field = loc[-1] if loc else "unknown"

        messages = {
            ("text", "string_type"): "The 'text' field must be a string.",
            ("important", "bool_type"): "The 'important' field must be true or false.",
            ("important", "bool_parsing"): "The 'important' field must be true or false.",
            ("note_id", "uuid_parsing"): "The 'note_id' must be a valid UUID.",
            ("username", "string_type"): "The 'username' field must be a string.",
            ("username", "missing"): "The 'username' field is required.",
            ("text", "missing"): "The 'text' field is required.",
        }

        message = messages.get((field, error_type))

        if message is None:
            logger.warning(
                "Unhandled validation error — field: %r, type: %r, loc: %r, url: %s %s",
                field, error_type, loc, request.method, request.url
            )
            message = "Invalid request data."

        return JSONResponse(
            status_code=422,
            content=error_response(
                message,
                "VALIDATION_ERROR",
                field if isinstance(field, str) else None
            )
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        if isinstance(exc.detail, dict):
            return JSONResponse(status_code=exc.status_code, content=exc.detail)

        return JSONResponse(
            status_code=exc.status_code,
            content=error_response(str(exc.detail), "HTTP_ERROR")
        )