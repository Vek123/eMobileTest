from typing import List

from schemas.author import AuthorOut
from schemas.book import BookOutWoAuthorId, BookOut
from schemas.borrow import BorrowOutWoBookId


class AuthorOutRel(AuthorOut):
    books: List["BookOut"]


class BookOutRel(BookOutWoAuthorId):
    author: "AuthorOut"


class BorrowOutRel(BorrowOutWoBookId):
    book: "BookOutRel"
