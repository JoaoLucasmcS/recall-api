from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends

from recall_api.core.dependencies import get_assistente_service
from recall_api.schemas.assistente_schemas import PerguntaAssistente, RespostaAssistente
from recall_api.services.assistente_service import AssistenteService

router = APIRouter(prefix='/assistente', tags=['assistente'])

Service = Annotated[AssistenteService, Depends(get_assistente_service)]


@router.post('/', status_code=HTTPStatus.OK, response_model=RespostaAssistente)
async def perguntar_ao_assistente(pergunta_e_historico: PerguntaAssistente, service: Service):

    resposta = await service.responder(pergunta_e_historico.mensagens)

    return {'resposta': resposta}
