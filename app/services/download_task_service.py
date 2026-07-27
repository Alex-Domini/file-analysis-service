import logging

from datetime import datetime
from zoneinfo import ZoneInfo

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
        self.state.stop_requested = False
        self.state.started_at = datetime.now(ZoneInfo("Asia/Novosibirsk"))

        try:
            downloaded_count = await self.file_service.download_all(self.state)

            self.state.downloaded_count = downloaded_count

            if self.state.stop_requested:
                self.state.status = "stopped"
            else:
                self.state.status = "completed"

        except Exception as error:
            self.state.status = "failed"
            self.state.error = str(error)

            logger.exception("Download failed: %s", error)
            logger.exception("Background download failed")
