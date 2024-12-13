import contextlib
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI

from api import router as api_router
from db import db_manager
from settings import settings


@contextlib.asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator:
    db_manager.init(settings.db_url)
    yield
    await db_manager.close()


app = FastAPI(
    title="Library",
    lifespan=lifespan,
)
app.include_router(
    api_router,
    prefix="/api/v1",
)


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.app_host, port=settings.app_port, reload=True)
