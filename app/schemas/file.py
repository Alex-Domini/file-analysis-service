from datetime import datetime
from pydantic import BaseModel, ConfigDict


class DownloadedFileResponse(BaseModel):
    id: int
    filename: str
    downloaded_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PaginatedFilesResponse(BaseModel):
    items: list[DownloadedFileResponse]
    page: int
    page_size: int
    total: int
    total_pages: int
