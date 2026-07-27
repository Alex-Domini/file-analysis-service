import asyncio
import logging
import httpx


from typing import Any
from app.core.config import settings

logger = logging.getLogger("uvicorn.error")


class ExternalAPIClient:
    def __init__(
        self,
        client: httpx.AsyncClient,
        base_api_url: str = settings.BASE_API_URL,
        request_delay: int = 2,
    ) -> None:
        self.client = client
        self.base_api_url = base_api_url
        self.request_delay = request_delay

    async def fetch_with_retry(
        self,
        method: str,
        endpoint: str,
        max_attempts: int = 5,
        **kwargs: Any,
    ) -> httpx.Response:
        url = f"{self.base_api_url}/{endpoint.lstrip('/')}"

        for attempt in range(1, max_attempts + 1):
            logger.info("Sending %s request to %s", method, endpoint)

            response = await self.client.request(
                method=method,
                url=url,
                **kwargs,
            )

            if response.status_code not in (429, 403):
                response.raise_for_status()

                logger.info(
                    "%s %s completed successfully",
                    method,
                    endpoint,
                )

                await asyncio.sleep(self.request_delay)

                return response

            if attempt == max_attempts:
                logger.error(
                    "%s %s failed after %s attempts",
                    method,
                    endpoint,
                    max_attempts,
                )
                response.raise_for_status()

            retry_after = response.headers.get("Retry-After")

            if retry_after:
                try:
                    wait_time = int(retry_after)
                except ValueError:
                    wait_time = 5
            else:
                wait_time = 10

            logger.warning(
                "Received %s. Waiting %s seconds. Attempt %s/%s.",
                response.status_code,
                wait_time,
                attempt,
                max_attempts,
            )

            await asyncio.sleep(wait_time)

        return response

    async def get_files_names(self) -> list[str]:
        response = await self.fetch_with_retry(
            method="GET",
            endpoint="/api/files/names",
        )
        data = response.json()
        return data.get("file_names", [])

    async def download_files_zip(self, filenames: list[str]) -> bytes:
        if not filenames:
            return b""

        if len(filenames) > 3:
            raise ValueError("API не позволяет скачивать более 3 файлов за один запрос")

        response = await self.fetch_with_retry(
            method="POST",
            endpoint="/api/files/download",
            json={"file_names": filenames},
        )

        return response.content

    async def mark_as_downloaded(self, filenames: list[str]) -> dict:
        if not filenames:
            return {}
        payload = {"file_names": filenames}
        response = await self.fetch_with_retry(
            method="POST",
            endpoint="/api/files/downloaded",
            json=payload,
        )
        return response.json()
