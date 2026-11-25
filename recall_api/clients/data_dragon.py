from http import HTTPStatus

import httpx

from recall_api.core.exceptions import (
    CampeaoNaoEncontradoError,
    DataDragonIndisponivelError,
)


class DataDragonClient:
    def __init__(self, base_url: str, http_client: httpx.AsyncClient) -> None:
        self.base_url = base_url
        self.http_client = http_client

    async def _get(self, url: str) -> httpx.Response:
        try:
            resposta = await self.http_client.get(url)

        except httpx.RequestError:
            raise DataDragonIndisponivelError('Data Dragon indisponível')

        if resposta.is_server_error:
            raise DataDragonIndisponivelError('Data Dragon respondeu com erro')

        return resposta

    async def get_versoes(self):
        url_versoes = f'{self.base_url}/api/versions.json'

        versoes = await self._get(url_versoes)

        return versoes.json()

    async def get_idiomas(self):
        url_idiomas = f'{self.base_url}/cdn/languages.json'

        idiomas = await self._get(url_idiomas)

        return idiomas.json()

    async def get_campeoes(self, versao: str, idioma: str):
        url_campeoes = f'{self.base_url}/cdn/{versao}/data/{idioma}/champion.json'

        campeoes = await self._get(url_campeoes)

        return campeoes.json()

    async def get_campeao_detalhe_por_id(self, versao: str, idioma: str, campeao_id: str):
        url_campeao = f'{self.base_url}/cdn/{versao}/data/{idioma}/champion/{campeao_id}.json'

        campeao_detalhado = await self._get(url_campeao)

        if campeao_detalhado.status_code in {HTTPStatus.FORBIDDEN, HTTPStatus.NOT_FOUND}:
            raise CampeaoNaoEncontradoError(f'Campeão {campeao_id} não encontrado')

        return campeao_detalhado.json()

    def montar_url_imagem_campeao_loading(self, campeao_id: str) -> str:
        url_img = f'{self.base_url}/cdn/img/champion/loading/{campeao_id}_0.jpg'

        return url_img
