from dataclasses import dataclass
from datetime import datetime


@dataclass
class DownloadState:
    status: str = "idle"
    downloaded_count: int = 0
    error: str | None = None
    started_at: datetime | None = None
    stop_requested: bool = False
