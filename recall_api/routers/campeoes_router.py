from typing import Annotated

from fastapi import APIRouter, Depends

from recall_api.core.dependencies import get_campeoes_service
from recall_api.schemas.campeoes_schemas import CampeaoResumo
from recall_api.services.campeoes_service import CampeoesService

router = APIRouter(prefix="/campeoes", tags=["campeoes"])


@router.get("/", response_model=list[CampeaoResumo])
async def listar_campeoes(
    service: Annotated[CampeoesService, Depends(get_campeoes_service)],
):
    return await service.listar_campeoes_resumo()
