from typing import Annotated

from fastapi import APIRouter, Depends

from recall_api.core.dependencies import get_campeoes_service
from recall_api.schemas.campeoes_schemas import CampeaoResumo, CampeaoDetalhe
from recall_api.services.campeoes_service import CampeoesService

router = APIRouter(prefix="/campeoes", tags=["campeoes"])


@router.get("/", response_model=list[CampeaoResumo])
async def listar_campeoes(
    service: Annotated[CampeoesService, Depends(get_campeoes_service)],
):
    return await service.listar_campeoes_resumo()

@router.get("/{campeao_id}", response_model=CampeaoDetalhe)
async def buscar_campeao_detalhado(
        service: Annotated[CampeoesService, Depends(get_campeoes_service)],
        campeao_id: str
):
    return await service.listar_campeao_detalhado(campeao_id=campeao_id)