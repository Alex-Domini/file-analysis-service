from dataclasses import dataclass


@dataclass
class DownloadState:
    status: str = "idle"
    downloaded_count: int = 0
    error: str | None = None
