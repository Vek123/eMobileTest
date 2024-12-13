from typing import Annotated, List

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db import get_session
from models.author import Author
from schemas.author import AuthorOut, AuthorIn
from schemas.base import APIException, BaseResponse


router = APIRouter(
    tags=["AuthorAPI"],
    prefix="/authors"
)


@router.get("/")
async def list_authors(
        session: Annotated[AsyncSession, Depends(get_session)]
) -> List[AuthorOut]:
    query = select(Author).order_by(Author.id.asc())
    authors = (await session.execute(query)).scalars().all()
    authors_pydantic_list = [AuthorOut.model_validate(row, from_attributes=True) for row in authors]
    return authors_pydantic_list


@router.post("/")
async def add_author(
        author: AuthorIn,
        session: Annotated[AsyncSession, Depends(get_session)]
) -> AuthorOut:
    session.add(Author(**author.model_dump()))
    await session.commit()

    query = select(Author).order_by(Author.id.desc()).limit(1)
    added_author = (await session.execute(query)).scalar_one()
    added_author_pydantic = AuthorOut.model_validate(added_author, from_attributes=True)

    return added_author_pydantic


@router.get("/{author_id}", responses={404: {"model": APIException}})
async def get_author(
        author_id: int,
        session: Annotated[AsyncSession, Depends(get_session)]
) -> AuthorOut:
    author = await session.get(Author, author_id)
    if author is None:
        raise HTTPException(404, "Author not found")
    author_pydantic = AuthorOut.model_validate(author, from_attributes=True)

    return author_pydantic


@router.put("/{author_id}", responses={404: {"model": APIException}})
async def update_author(
        author_id: int,
        author: AuthorIn,
        session: Annotated[AsyncSession, Depends(get_session)]
) -> AuthorOut:
    existed_author = await session.get(Author, author_id)
    if existed_author is None:
        raise HTTPException(404, "Author not found")
    existed_author.name = author.name
    existed_author.second_name = author.second_name
    existed_author_pydantic = AuthorOut.model_validate(existed_author, from_attributes=True)
    await session.commit()

    return existed_author_pydantic


@router.delete("/{author_id}", responses={404: {"model": APIException}})
async def delete_author(
        author_id: int,
        session: Annotated[AsyncSession, Depends(get_session)],
) -> BaseResponse:
    existed_author = await session.get(Author, author_id)
    if existed_author is None:
        raise HTTPException(404, "Author not found")
    await session.delete(existed_author)
    await session.commit()

    return BaseResponse(status="ok")
