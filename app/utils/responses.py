from typing import Generic, Optional, TypeVar, Any
from pydantic import BaseModel
from http import HTTPStatus

T = TypeVar("T")


class BaseResponse(BaseModel, Generic[T]):
    message: str
    status_code: HTTPStatus = HTTPStatus.OK
    data: Optional[T] = None


class ErrorResponse(BaseModel):
    message: str
    status_code: HTTPStatus = HTTPStatus.OK
    error: Optional[Any] = None
