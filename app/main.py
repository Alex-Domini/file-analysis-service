from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.base import Base
from app.core.database import engine

from app.models.file import DownloadedFile  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="File Analysis Service", lifespan=lifespan)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
