from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

from recall_api.core.dependencies import get_versao_atual
from recall_api.schemas.patch_schemas import Patch

router = APIRouter(prefix='/patch', tags=['patch'])


@router.get('/', status_code=HTTPStatus.OK, response_model=Patch)
async def buscar_patch_atual(versao: Annotated[str, Depends(get_versao_atual)]):
    return {'versao': versao}
