import httpx
from fastapi import Depends, Request

from app.clients.file_api_client import ExternalAPIClient


async def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client


async def get_external_api_client(
    client: httpx.AsyncClient = Depends(get_http_client),
) -> ExternalAPIClient:
    http_client = ExternalAPIClient(
        client=client,
    )

    return http_client
