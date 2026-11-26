from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from recall_api.core.dependencies import get_campeoes_service
from recall_api.core.exceptions import CampeaoNaoEncontradoError
from recall_api.schemas.campeoes_schemas import CampeaoDetalhe, CampeaoResumo
from recall_api.services.campeoes_service import CampeoesService

router = APIRouter(prefix='/campeoes', tags=['campeoes'])

Service = Annotated[CampeoesService, Depends(get_campeoes_service)]


@router.get('/', status_code=HTTPStatus.OK, response_model=list[CampeaoResumo])
async def listar_campeoes(service: Service):
    return await service.listar_campeoes_resumo()


@router.get('/{campeao_id}', status_code=HTTPStatus.OK, response_model=CampeaoDetalhe)
async def buscar_campeao_detalhado_por_id(campeao_id: str, service: Service):
    try:
        return await service.buscar_campeao_detalhado(campeao_id=campeao_id)

    except CampeaoNaoEncontradoError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Campeão não encontrado',
        )
