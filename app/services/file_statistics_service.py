from pathlib import Path


class FileStatisticsService:
    def calculate(
        self,
        files: list[tuple[str, Path]],
    ) -> dict:
        total_counts = {str(digit): 0 for digit in range(10)}
        files_statistics = []

        for filename, file_path in files:
            file_counts = {str(digit): 0 for digit in range(10)}

            content = file_path.read_text(encoding="utf-8").strip()

            if len(content) != 500:
                raise ValueError(f"File {filename} must contain exactly 500 characters")

            if not content.isdigit():
                raise ValueError(f"File {filename} contains non-digit characters")

            for character in content:
                file_counts[character] += 1
                total_counts[character] += 1

            files_statistics.append(
                {
                    "filename": filename,
                    "digits": file_counts,
                }
            )

        return {
            "total": total_counts,
            "files": files_statistics,
        }
