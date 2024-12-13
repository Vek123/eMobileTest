from pydantic import Field

from schemas.base import Base


class AuthorIn(Base):
    name: str = Field(max_length=50)
    second_name: str = Field(max_length=50)


class AuthorOut(AuthorIn):
    id: int
