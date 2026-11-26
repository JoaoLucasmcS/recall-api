from typing import Annotated

from fastapi import Depends, Request

from recall_api.clients.data_dragon import DataDragonClient
from recall_api.core.settings import Settings, get_settings
from recall_api.services.campeoes_service import CampeoesService


def get_data_dragon_client(request: Request) -> DataDragonClient:
    settings = get_settings()

    return DataDragonClient(
        base_url=settings.url_base,
        http_client=request.app.state.http_client,
    )


def get_campeoes_service(
    client: Annotated[DataDragonClient, Depends(get_data_dragon_client)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> CampeoesService:
    return CampeoesService(client_data_dragon=client, versao=settings.versao, idioma=settings.idioma)
