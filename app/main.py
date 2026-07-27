import httpx

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends

from app.core.base import Base
from app.core.database import engine

from app.api.dependencies import get_file_service
from app.api.dependencies import get_external_api_client


from app.clients.file_api_client import ExternalAPIClient
from app.services.file_service import FileService
from app.models.file import DownloadedFile  # noqa: F401

from app.core.config import settings

from app.api.routers.download import router as download_router
from app.api.routers.files_router import router as files_router


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


app.include_router(download_router)
app.include_router(files_router)


@app.get("/health")
async def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/test-api")
async def test_api(
    client: ExternalAPIClient = Depends(get_external_api_client),
) -> dict[str, list[str]]:
    files = await client.get_files_names()
    return {"fetched_names": files}


@app.post("/test/download")
async def download_files(service: FileService = Depends(get_file_service)):
    downloaded = await service.download_all()
    return {"downloaded": downloaded}
