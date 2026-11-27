import httpx

from recall_api.core.exceptions import LLMIndisponivelError


class LLMClient:
    def __init__(self, url_base: str, modelo: str, api_key: str, http_client: httpx.AsyncClient) -> None:
        self.url_base = url_base
        self.modelo = modelo
        self.api_key = api_key
        self.http_client = http_client

    async def conversar(self, mensagens: list[dict]) -> str:

        url_conversa = f'{self.url_base}/chat/completions'

        try:
            resposta = await self.http_client.post(
                url_conversa,
                json={
                    'model': self.modelo,
                    'messages': mensagens,
                },
                headers={'Authorization': f'Bearer {self.api_key}'},
            )

        except httpx.RequestError:
            raise LLMIndisponivelError('LLM indisponível')

        if not resposta.is_success:
            raise LLMIndisponivelError('LLM respondeu com erro')

        return resposta.json()['choices'][0]['message']['content']
