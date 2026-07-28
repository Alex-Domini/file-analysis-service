from math import ceil
from pathlib import Path

from fastapi import APIRouter, Depends, Query, HTTPException
from starlette import status

from app.api.dependencies import get_file_service
from app.services.file_service import FileService


from app.schemas.file_statistics import FileStatisticsRequest
from app.services.file_statistics_service import FileStatisticsService
from app.repositories.downloaded_file_repository import (
    DownloadedFileRepository,
)
from app.api.dependencies import get_file_repository, get_file_statistics_service


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


@router.post("/statistics")
async def calculate_statistics(
    data: FileStatisticsRequest,
    repository: DownloadedFileRepository = Depends(get_file_repository),
    statistics_service: FileStatisticsService = Depends(get_file_statistics_service),
) -> dict:
    files = await repository.get_by_ids(data.file_ids)

    if not files:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Files not found",
        )

    found_ids = {file.id for file in files}
    missing_ids = set(data.file_ids) - found_ids

    if missing_ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": "Some files were not found",
                "missing_ids": sorted(missing_ids),
            },
        )

    files_to_calculate = [
        (
            file.filename,
            Path(file.stored_path),
        )
        for file in files
    ]

    try:
        return statistics_service.calculate(files_to_calculate)
    except FileNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error),
        ) from error
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(error),
        ) from error


@router.get("/ids")
async def get_all_file_ids(
    service: FileService = Depends(get_file_service),
):
    ids = await service.get_all_ids()

    return {
        "ids": ids,
    }
