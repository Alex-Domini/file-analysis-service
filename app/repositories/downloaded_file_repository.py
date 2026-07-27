from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, func

from app.models.file import DownloadedFile


class DownloadedFileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, filename: str, stored_path: Path) -> DownloadedFile:
        downloaded_file = DownloadedFile(
            filename=filename,
            stored_path=str(stored_path),
        )

        self.session.add(downloaded_file)
        await self.session.commit()
        await self.session.refresh(downloaded_file)

        return downloaded_file

    async def create_many(
        self,
        saved_files: list[tuple[str, Path]],
    ) -> None:
        if not saved_files:
            return

        values = [
            {
                "filename": filename,
                "stored_path": str(file_path),
            }
            for filename, file_path in saved_files
        ]

        statement = insert(DownloadedFile).values(values)

        await self.session.execute(statement)
        await self.session.commit()

    async def get_all(self) -> list[DownloadedFile]:
        result = await self.session.execute(
            select(DownloadedFile).order_by(DownloadedFile.downloaded_at.desc())
        )

        return list(result.scalars().all())

    async def get_by_filename(
        self,
        filename: str,
    ) -> DownloadedFile | None:
        result = await self.session.execute(
            select(DownloadedFile).where(DownloadedFile.filename == filename)
        )

        return result.scalar_one_or_none()

    async def get_paginated(
        self,
        page: int,
        page_size: int,
    ) -> tuple[list[DownloadedFile], int]:
        offset = (page - 1) * page_size

        files_query = (
            select(DownloadedFile)
            .order_by(DownloadedFile.downloaded_at.desc())
            .offset(offset)
            .limit(page_size)
        )

        files_result = await self.session.execute(files_query)
        files = list(files_result.scalars().all())

        count_query = select(func.count(DownloadedFile.id))
        count_result = await self.session.execute(count_query)
        total = count_result.scalar_one()

        return files, total

    async def get_by_ids(
        self,
        file_ids: list[int],
    ) -> list[DownloadedFile]:
        query = (
            select(DownloadedFile)
            .where(DownloadedFile.id.in_(file_ids))
            .order_by(DownloadedFile.downloaded_at.desc())
        )

        result = await self.session.execute(query)

        return list(result.scalars().all())
