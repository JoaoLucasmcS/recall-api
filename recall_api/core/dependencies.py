from typing import Annotated

from fastapi import Depends, Request

from recall_api.clients.data_dragon import DataDragonClient
from recall_api.clients.llm import LLMClient
from recall_api.core.settings import Settings, get_settings
from recall_api.services.assistente_service import AssistenteService
from recall_api.services.campeoes_service import CampeoesService


def get_data_dragon_client(request: Request) -> DataDragonClient:
    settings = get_settings()

    return DataDragonClient(
        base_url=settings.url_base,
        http_client=request.app.state.http_client,
    )


async def get_versao_atual(
    request: Request,
    client: Annotated[DataDragonClient, Depends(get_data_dragon_client)],
) -> str:
    return await request.app.state.cache_versao.obter(client)


def get_campeoes_service(
    request: Request,
    client: Annotated[DataDragonClient, Depends(get_data_dragon_client)],
    settings: Annotated[Settings, Depends(get_settings)],
    versao: Annotated[str, Depends(get_versao_atual)],
) -> CampeoesService:
    return CampeoesService(
        client_data_dragon=client,
        cache=request.app.state.cache_campeoes,
        versao=versao,
        idioma=settings.idioma,
    )


async def get_llm_client(request: Request) -> LLMClient:
    settings = get_settings()

    return LLMClient(
        url_base=settings.llm_url_base,
        modelo=settings.llm_modelo,
        api_key=settings.llm_api_key,
        http_client=request.app.state.http_client_llm,
    )


def get_assistente_service(client: Annotated[LLMClient, Depends(get_llm_client)]) -> AssistenteService:

    return AssistenteService(client)
