import httpx

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends

from app.core.base import Base
from app.core.database import engine

from app.models.file import DownloadedFile  # noqa: F401

from app.clients.file_api_client import ExternalAPIClient
from app.clients.dependencies import get_external_api_client

from app.core.config import settings

from app.services.file_storage_service import FileStorageService
from app.repositories.downloaded_file_repository import DownloadedFileRepository
from app.core.database import AsyncSession, get_db


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


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/test-api")
async def test_api(
    client: ExternalAPIClient = Depends(get_external_api_client),
) -> dict[str, list[str]]:
    files = await client.get_files_names()
    return {"fetched_names": files}
