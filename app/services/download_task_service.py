import logging
from app.services.file_service import FileService
from app.services.download_state import DownloadState

logger = logging.getLogger(__name__)


class DownloadTaskService:
    def __init__(self, file_service: FileService, state: DownloadState) -> None:
        self.file_service = file_service
        self.state = state

    async def run(self) -> None:
        self.state.status = "running"
        self.state.downloaded_count = 0
        self.state.error = None

        try:
            downloaded_count = await self.file_service.download_all()

            self.state.downloaded_count = downloaded_count
            self.state.status = "completed"

        except Exception as error:
            logger.exception("Download failed: %s", error)

            self.state.status = "failed"
            self.state.error = str(error)
