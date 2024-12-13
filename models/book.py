from typing import TYPE_CHECKING, List

from sqlalchemy import String, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import BaseOrm
from models.base import int_pk

if TYPE_CHECKING:
    from models.author import Author
    from models.borrow import Borrow


class Book(BaseOrm):
    __tablename__ = "book"

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    amount: Mapped[int]
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))
    author: Mapped["Author"] = relationship(back_populates="books")
    borrows: Mapped[List["Borrow"]] = relationship(back_populates="book")

    __table_args__ = (
        Index("book_name_index", "name"),
    )
