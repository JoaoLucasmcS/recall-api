import time

from recall_api.clients.data_dragon import DataDragonClient


class CacheVersao:
    def __init__(self, ttl_segundos: int):
        self._ttl_segundos = ttl_segundos
        self._versao: str | None = None
        self._buscado_em: float = 0

    async def obter(self, client: DataDragonClient) -> str:

        expirou = time.monotonic() - self._buscado_em > self._ttl_segundos

        if self._versao is None or expirou:
            versoes = await client.get_versoes()
            self._versao = versoes[0]
            self._buscado_em = time.monotonic()
        return self._versao
