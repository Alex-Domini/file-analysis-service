from dataclasses import dataclass
from datetime import datetime


@dataclass
class DownloadState:
    status: str = "idle"
    downloaded_count: int = 0

    current_batch_total: int = 0
    current_batch_downloaded: int = 0

    started_at: datetime | None = None
    stop_requested: bool = False
    error: str | None = None
