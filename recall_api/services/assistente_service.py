from recall_api.clients.llm import LLMClient
from recall_api.schemas.assistente_schemas import Mensagem

PROMPT_SISTEMA = (
    'Você é o assistente do Recall, uma biblioteca de campeões do League of Legends. '
    'Responda sempre em português, de forma curta e direta. '
    'Se não tiver certeza de uma informação, diga que não sabe em vez de inventar.'
)

MAX_MENSAGENS = 10


class AssistenteService:
    def __init__(self, llm_client: LLMClient):
        self._llm = llm_client

    async def responder(self, mensagens: list[Mensagem]) -> str:

        historico = [mensagem.model_dump() for mensagem in mensagens[-MAX_MENSAGENS:]]

        conversa = [
            {
                'role': 'system',
                'content': PROMPT_SISTEMA,
            },
            *historico,
        ]

        return await self._llm.conversar(conversa)
