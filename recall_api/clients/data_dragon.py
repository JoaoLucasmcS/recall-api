import httpx


class DataDragonClient:
    def __init__(self, base_url: str, http_client: httpx.AsyncClient) -> None:
        self.base_url = base_url
        self.http_client = http_client

    async def get_versoes(self):

        url_versoes = f"{self.base_url}/api/versions.json"

        versoes = await self.http_client.get(url_versoes)

        return versoes.json()

    async def get_idiomas(self):

        url_idiomas = f"{self.base_url}/cdn/languages.json"

        idiomas = await self.http_client.get(url_idiomas)

        return idiomas.json()

    async def get_campeoes(self, versao: str, idioma: str):

        url_campeoes = f"{self.base_url}/cdn/{versao}/data/{idioma}/champion.json"

        campeoes = await self.http_client.get(url_campeoes)

        return campeoes.json()

    async def get_campeao_detalhe(self, versao: str, idioma: str, champion_id: str):

        url_campeao = f"{self.base_url}/cdn/{versao}/data/{idioma}/champion/{champion_id}.json"

        campeao_detalhado = await self.http_client.get(url_campeao)

        return campeao_detalhado.json()
