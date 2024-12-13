from typing import Annotated, List

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound

from db import get_session
from models.book import Book
from schemas.book import BookIn
from schemas.relations import BookOutRel
from schemas.base import APIException, BaseResponse


router = APIRouter(
    tags=["BookAPI"],
    prefix="/books"
)


@router.get("/")
async def list_book(
        session: Annotated[AsyncSession, Depends(get_session)],
) -> List[BookOutRel]:
    query = select(Book).options(joinedload(Book.author)).order_by(Book.id.asc())
    books = (await session.execute(query)).scalars().all()
    books_pydantic_list = [
        BookOutRel.model_validate(row, from_attributes=True) for row in books
    ]

    return books_pydantic_list


@router.post("/", responses={400: {"model": APIException}})
async def add_book(
        book: BookIn,
        session: Annotated[AsyncSession, Depends(get_session)],
) -> BookOutRel:
    session.add(Book(**book.model_dump()))
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(400, f"Author with id {book.author_id} is not defined")

    query = select(Book).options(joinedload(Book.author)).order_by(Book.id.desc()).limit(1)
    added_book = (await session.execute(query)).scalar_one()

    return BookOutRel.model_validate(added_book, from_attributes=True)


@router.get("/{book_id}", responses={404: {"model": APIException}})
async def get_book(
        book_id: int,
        session: Annotated[AsyncSession, Depends(get_session)],
) -> BookOutRel:
    query = select(Book).options(joinedload(Book.author)).where(Book.id == book_id)
    try:
        book = (await session.execute(query)).scalar_one()
    except NoResultFound:
        raise HTTPException(404, "Book is not found")

    return BookOutRel.model_validate(book, from_attributes=True)


@router.put("/{book_id}", responses={404: {"model": APIException}})
async def update_book(
        book_id: int,
        book: BookIn,
        session: Annotated[AsyncSession, Depends(get_session)],
) -> BookOutRel:
    stmt = update(Book).where(Book.id == book_id).values(**book.model_dump())
    await session.execute(stmt)
    await session.commit()

    query = select(Book).options(joinedload(Book.author)).where(Book.id == book_id)
    try:
        updated_book = (await session.execute(query)).scalar_one()
    except NoResultFound:
        raise HTTPException(404, "Book not found")

    return BookOutRel.model_validate(updated_book, from_attributes=True)


@router.delete("/{book_id}", responses={404: {"model": APIException}})
async def delete_book(
        book_id: int,
        session: Annotated[AsyncSession, Depends(get_session)],
) -> BaseResponse:
    query = select(Book).options(joinedload(Book.author)).where(Book.id == book_id)
    try:
        existed_book = (await session.execute(query)).scalar_one()
    except NoResultFound:
        raise HTTPException(404, "Book not found")

    await session.delete(existed_book)
    await session.commit()

    return BaseResponse(status="ok")
