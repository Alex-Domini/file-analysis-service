import httpx

from dataclasses import asdict

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request
from starlette import status

from app.clients.file_api_client import ExternalAPIClient
from app.core.database import AsyncSessionLocal
from app.api.dependencies import get_download_state
from app.repositories.downloaded_file_repository import DownloadedFileRepository
from app.services.download_state import DownloadState
from app.services.download_task_service import DownloadTaskService
from app.services.file_service import FileService
from app.services.file_storage_service import FileStorageService

from app.schemas.download_status import DownloadStatusResponse


router = APIRouter(
    prefix="/download",
    tags=["download"],
)


async def run_download_in_background(
    http_client: httpx.AsyncClient,
    state: DownloadState,
) -> None:
    async with AsyncSessionLocal() as session:
        external_api_client = ExternalAPIClient(client=http_client)
        storage = FileStorageService()
        repository = DownloadedFileRepository(session)

        file_service = FileService(
            client=external_api_client,
            storage=storage,
            repository=repository,
        )

        task_service = DownloadTaskService(
            file_service=file_service,
            state=state,
        )

        await task_service.run()


@router.post("", status_code=status.HTTP_202_ACCEPTED)
async def start_download(
    background_tasks: BackgroundTasks,
    request: Request,
    state: DownloadState = Depends(get_download_state),
) -> dict[str, str]:
    if state.status == "running":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Download is already running",
        )

    state.status = "running"
    state.downloaded_count = 0

    state.current_batch_total = 0
    state.current_batch_downloaded = 0

    state.error = None
    state.stop_requested = False

    background_tasks.add_task(
        run_download_in_background,
        request.app.state.http_client,
        state,
    )

    return {"status": "started"}


@router.get(
    "/status",
    response_model=DownloadStatusResponse,
)
async def get_download_status(
    state: DownloadState = Depends(get_download_state),
) -> DownloadStatusResponse:
    return DownloadStatusResponse(**asdict(state))


@router.post("/stop")
async def stop_download(
    state: DownloadState = Depends(get_download_state),
) -> dict[str, str]:
    if state.status != "running":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Download is not running",
        )

    state.stop_requested = True

    return {"status": "stop_requested"}
