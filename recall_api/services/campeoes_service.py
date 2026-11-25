from recall_api.clients.data_dragon import DataDragonClient
from recall_api.schemas.campeoes_schemas import CampeaoDetalhe, CampeaoResumo


class CampeoesService:
    def __init__(self, client_data_dragon: DataDragonClient, versao: str, idioma: str) -> None:
        self._client_data_dragon = client_data_dragon
        self._versao = versao
        self._idioma = idioma

    def _adicionar_url_da_imagem(self, campeao: dict) -> dict:

        url_imagem = self._client_data_dragon.montar_url_imagem_campeao_loading(campeao['id'])

        campeao_com_url_img = {**campeao, 'imagem_url': url_imagem}

        return campeao_com_url_img

    async def listar_campeoes_resumo(self) -> list[CampeaoResumo]:

        dados = await self._client_data_dragon.get_campeoes(self._versao, self._idioma)

        campeoes = dados['data'].values()

        return [CampeaoResumo.model_validate(self._adicionar_url_da_imagem(campeao)) for campeao in campeoes]

    async def buscar_campeao_detalhado(self, campeao_id: str) -> CampeaoDetalhe:

        dados = await self._client_data_dragon.get_campeao_detalhe_por_id(
            self._versao, self._idioma, campeao_id
        )

        campeao_detalhado = dados['data'][campeao_id]

        return CampeaoDetalhe.model_validate(self._adicionar_url_da_imagem(campeao_detalhado))
