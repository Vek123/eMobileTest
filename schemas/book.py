from pydantic import Field

from schemas.base import Base


class BookWoAuthorId(Base):
    name: str = Field(max_length=255)
    description: str
    amount: int


class BookIn(BookWoAuthorId):
    author_id: int


class BookOutWoAuthorId(BookWoAuthorId):
    id: int


class BookOut(BookIn):
    id: int
