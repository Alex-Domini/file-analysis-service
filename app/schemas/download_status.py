from datetime import datetime

from pydantic import BaseModel


class DownloadStatusResponse(BaseModel):
    status: str
    downloaded_count: int
    error: str | None
    started_at: datetime | None
    stop_requested: bool
