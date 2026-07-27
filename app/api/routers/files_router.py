from math import ceil

from fastapi import APIRouter, Depends, Query

from app.api.dependencies import get_file_repository
from app.repositories.downloaded_file_repository import (
    DownloadedFileRepository,
)


router = APIRouter(
    prefix="/files",
    tags=["files"],
)


@router.get("")
async def get_files(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=100),
    repository: DownloadedFileRepository = Depends(get_file_repository),
) -> dict:
    files, total = await repository.get_paginated(
        page=page,
        page_size=page_size,
    )

    return {
        "items": [
            {
                "id": file.id,
                "filename": file.filename,
                "downloaded_at": file.downloaded_at,
            }
            for file in files
        ],
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": ceil(total / page_size) if total else 0,
        },
    }
