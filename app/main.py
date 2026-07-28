import httpx

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.base import Base
from app.core.database import engine


from app.models.file import DownloadedFile  # noqa: F401

from app.core.config import settings

from app.api.routers.download import router as download_router
from app.api.routers.files_router import router as files_router
from app.api.routers.web_router import router as web_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with httpx.AsyncClient(
        timeout=30.0,
        headers={
            "X-Candidate-Id": settings.CANDIDATE_ID,
            "Accept": "application/json",
        },
    ) as client:
        app.state.http_client = client
        yield

    await engine.dispose()


app = FastAPI(
    title="File Analysis Service",
    lifespan=lifespan,
)

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static",
)

app.include_router(download_router)
app.include_router(files_router)
app.include_router(web_router)
