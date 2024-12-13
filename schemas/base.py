import datetime

from pydantic import BaseModel


class Base(BaseModel):
    ...


class BaseResponse(BaseModel):
    status: str


class APIException(BaseModel):
    detail: str
