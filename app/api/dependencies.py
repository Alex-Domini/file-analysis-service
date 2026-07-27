import httpx
from fastapi import Depends, Request

from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.file_api_client import ExternalAPIClient

from app.services.download_state import DownloadState
from app.services.download_task_service import DownloadTaskService
from app.services.file_service import FileService
from app.services.file_storage_service import FileStorageService
from app.repositories.downloaded_file_repository import DownloadedFileRepository

from app.core.database import get_db

download_state = DownloadState()


async def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client


async def get_external_api_client(
    client: httpx.AsyncClient = Depends(get_http_client),
) -> ExternalAPIClient:
    return ExternalAPIClient(client=client)


async def get_file_service(
    client: httpx.AsyncClient = Depends(get_http_client),
    session: AsyncSession = Depends(get_db),
) -> FileService:
    external_api_client = ExternalAPIClient(client)
    storage = FileStorageService()
    repository = DownloadedFileRepository(session)

    service = FileService(external_api_client, storage, repository)
    return service


def get_download_state() -> DownloadState:
    return download_state


async def get_download_task_service(
    file_service: FileService = Depends(get_file_service),
    state: DownloadState = Depends(get_download_state),
) -> DownloadTaskService:
    return DownloadTaskService(
        file_service=file_service,
        state=state,
    )
