from typing import TYPE_CHECKING, Optional

from sqlalchemy import String, ForeignKey, Date, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import BaseOrm
from models.base import int_pk

if TYPE_CHECKING:
    from models.book import Book


class Borrow(BaseOrm):
    __tablename__ = "Borrow"

    id: Mapped[int_pk]
    book: Mapped["Book"] = relationship(back_populates="borrows")
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"))
    reader_name: Mapped[str] = mapped_column(String(50))
    issue_date: Mapped[Date] = mapped_column(Date(), server_default=func.current_date())
    return_date: Mapped[Optional[Date]] = mapped_column(Date(), nullable=True)

    __table_args__ = (
        Index("borrow_reader_index", "reader_name"),
    )
