from datetime import date
from typing import Annotated, List

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy import select, text
from sqlalchemy.orm import joinedload, contains_eager
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound

from db import get_session
from models.book import Book
from schemas.borrow import BorrowIn
from schemas.base import APIException, BaseResponse
from models.borrow import Borrow
from schemas.relations import BorrowOutRel

router = APIRouter(
    tags=["BorrowAPI"],
    prefix="/borrows",
)


@router.get("/")
async def list_borrow(
        session: Annotated[AsyncSession, Depends(get_session)],
) -> List[BorrowOutRel]:
    query = (select(Borrow)
             .join(Borrow.book)
             .join(Book.author)
             .options(contains_eager(Borrow.book, Book.author))
             .order_by(Borrow.id.asc()))
    borrows = (await session.execute(query)).scalars().all()
    borrows_pydantic_list = [
        BorrowOutRel.model_validate(row, from_attributes=True) for row in borrows
    ]

    return borrows_pydantic_list


@router.post("/", responses={400: {"model": APIException}, 406: {"model": APIException}})
async def add_borrow(
        borrow: BorrowIn,
        session: Annotated[AsyncSession, Depends(get_session)],
) -> BorrowOutRel:
    existed_book = await session.get(Book, borrow.book_id)
    if existed_book is None:
        raise HTTPException(400, f"Book with id {borrow.book_id} is not defined")
    if existed_book.amount <= 0:
        raise HTTPException(406, "There are no books available")

    session.add(Borrow(**borrow.model_dump()))
    await session.commit()

    query = (select(Borrow)
             .join(Borrow.book)
             .join(Book.author)
             .options(contains_eager(Borrow.book, Book.author))
             .order_by(Borrow.id.desc())
             .limit(1))

    added_borrow = (await session.execute(query)).scalar_one()
    if added_borrow.return_date is None:
        added_borrow.book.amount -= 1
    added_borrow_pydantic = BorrowOutRel.model_validate(
        added_borrow, from_attributes=True
    )
    await session.commit()

    return added_borrow_pydantic


@router.get("/{borrow_id}", responses={404: {"model": APIException}})
async def get_borrow(
        borrow_id: int,
        session: Annotated[AsyncSession, Depends(get_session)],
) -> BorrowOutRel:
    query = (select(Borrow)
             .join(Borrow.book)
             .join(Book.author)
             .options(contains_eager(Borrow.book, Book.author))
             .where(Borrow.id == borrow_id))
    try:
        borrow = (await session.execute(query)).scalar_one()
    except NoResultFound:
        raise HTTPException(404, "Borrow not found")

    return BorrowOutRel.model_validate(borrow, from_attributes=True)


@router.patch("/{borrow_id}/return", responses={404: {"model": APIException}})
async def update_borrow_status(
        borrow_id: int,
        return_date: date,
        session: Annotated[AsyncSession, Depends(get_session)],
) -> BaseResponse:
    query = (select(Borrow)
             .join(Borrow.book)
             .join(Book.author)
             .options(contains_eager(Borrow.book, Book.author))
             .where(Borrow.id == borrow_id))
    try:
        existed_borrow = (await session.execute(query)).scalar_one()
    except NoResultFound:
        raise HTTPException(404, "Borrow not found")

    if existed_borrow.return_date is None:
        existed_borrow.return_date = return_date
        existed_borrow.book.amount += 1
        await session.commit()

    return BaseResponse(status="ok")
