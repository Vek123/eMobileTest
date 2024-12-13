from datetime import date
from typing import Optional

from pydantic import Field

from schemas.base import Base


class BorrowWoBookId(Base):
    reader_name: str = Field(max_length=50)
    issue_date: date
    return_date: Optional[date] = Field(default=None)


class BorrowIn(BorrowWoBookId):
    book_id: int


class BorrowOutWoBookId(BorrowWoBookId):
    id: int


class BorrowOut(BorrowIn):
    id: int
