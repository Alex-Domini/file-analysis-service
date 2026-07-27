import io
import zipfile
from pathlib import Path
from app.core.paths import FILES_DIR


class FileStorageService:
    def __init__(self, files_dir: Path = FILES_DIR) -> None:
        self.files_dir = files_dir
        self.files_dir.mkdir(parents=True, exist_ok=True)

    async def save_files_from_zip(self, archive_content: bytes) -> list:
        saved_files = []

        with zipfile.ZipFile(io.BytesIO(archive_content)) as archive:
            for archive_name in archive.namelist():
                if archive_name.endswith("/"):
                    continue

                filename = Path(archive_name).name
                file_path = self.files_dir / filename

                with archive.open(archive_name) as source:
                    file_path.write_bytes(source.read())

                saved_files.append((archive_name, file_path))

        return saved_files
