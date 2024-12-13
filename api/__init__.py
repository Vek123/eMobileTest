from fastapi import APIRouter

from api.author import router as author_router
from api.book import router as book_router
from api.borrow import router as borrow_router

router = APIRouter()

router.include_router(author_router)
router.include_router(book_router)
router.include_router(borrow_router)
