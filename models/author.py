from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Index

from models import BaseOrm
from models.base import int_pk

if TYPE_CHECKING:
    from models.book import Book


class Author(BaseOrm):
    __tablename__ = "author"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(50))
    second_name: Mapped[str] = mapped_column(String(50))
    books: Mapped[List["Book"]] = relationship(back_populates="author")

    __table_args__ = (
        Index("author_name_index", "name", "second_name"),
    )
