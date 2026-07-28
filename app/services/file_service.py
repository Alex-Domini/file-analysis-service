import logging

from app.repositories.downloaded_file_repository import DownloadedFileRepository
from app.services.file_storage_service import FileStorageService
from app.clients.file_api_client import ExternalAPIClient

from app.services.download_state import DownloadState

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.INFO)


class FileService:
    def __init__(
        self,
        client: ExternalAPIClient,
        storage: FileStorageService,
        repository: DownloadedFileRepository,
    ) -> None:
        self.client = client
        self.storage = storage
        self.repository = repository

    async def download_batch(self, state: DownloadState) -> int:
        logger.info("Requesting next batch of files")
        names = await self.client.get_files_names()

        if not names:
            logger.info("No files left to download")
            return 0

        state.current_batch_total = len(names)
        state.current_batch_downloaded = 0

        names_to_download = names[:3]
        logger.info(
            "Downloading %s file(s): %s",
            len(names_to_download),
            names_to_download,
        )

        zip_bytes = await self.client.download_files_zip(names_to_download)

        saved_files = await self.storage.save_files_from_zip(zip_bytes)
        state.current_batch_downloaded = len(saved_files)

        logger.info(
            "Saved %s file(s) to disk",
            len(saved_files),
        )

        await self.repository.create_many(saved_files)
        logger.info("Metadata saved to database")

        await self.client.mark_as_downloaded(names_to_download)
        logger.info("Files marked as downloaded")

        return len(saved_files)

    async def download_all(self, state: DownloadState) -> int:
        total_downloaded = 0

        logger.info("Starting full download")

        while True:
            if state.stop_requested:
                break

            downloaded = await self.download_batch(state)

            if downloaded == 0:
                break
            total_downloaded += downloaded
            state.downloaded_count = total_downloaded

            logger.info("Total downloaded: %s", total_downloaded)

        logger.info(
            "Download finished. Total files: %s",
            total_downloaded,
        )

        return total_downloaded
