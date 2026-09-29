import httpx


class DataDragonClient:
    def __init__(self, base_url: str, http_client: httpx.AsyncClient) -> None:
        self.base_url = base_url
        self.http_client = http_client

    async def get_campeoes(self):

        lista_campeoes = await self.http_client.get(self.base_url)

        return lista_campeoes.json()
