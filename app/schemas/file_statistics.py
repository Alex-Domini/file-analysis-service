from pydantic import BaseModel, Field


class FileStatisticsRequest(BaseModel):
    file_ids: list[int] = Field(min_length=1)
