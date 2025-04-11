from fastapi import status
from fastapi.responses import JSONResponse
from typing import Any


def success_response(
    data: Any = None, status_code: status = status.HTTP_200_OK, message: str = "Success"
):
    return JSONResponse(
        content={"data": data, "message": message, "status_code": status_code},
        status_code=status_code,
    )


def error_response(message: str, status_code: status, error: Any = None):
    return JSONResponse(
        content={"error": error, "message": message, "status_code": status_code},
        status_code=status_code,
    )
