from collections.abc import AsyncIterator
from typing import Annotated

import httpx
from fastapi import Depends

from recall_api.clients.data_dragon import DataDragonClient
from recall_api.core.settings import get_settings
from recall_api.services.campeoes_service import CampeoesService


async def get_data_dragon_client() -> AsyncIterator[DataDragonClient]:
    settings = get_settings()

    async with httpx.AsyncClient(timeout=10.0) as http_client:
        yield DataDragonClient(
            base_url=settings.url_dDragon_campeoes,
            http_client=http_client,
        )


def get_campeoes_service(
    client: Annotated[DataDragonClient, Depends(get_data_dragon_client)],
) -> CampeoesService:
    return CampeoesService(client_data_dragon=client)
