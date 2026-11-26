from recall_api.clients.data_dragon import DataDragonClient
from recall_api.core.cache import CacheCampeoes
from recall_api.schemas.campeoes_schemas import CampeaoDetalhe, CampeaoResumo


class CampeoesService:
    def __init__(
        self, client_data_dragon: DataDragonClient, cache: CacheCampeoes, versao: str, idioma: str
    ) -> None:
        self._client_data_dragon = client_data_dragon
        self._cache = cache
        self._versao = versao
        self._idioma = idioma

    def _adicionar_url_da_imagem(self, campeao: dict) -> dict:

        url_imagem = self._client_data_dragon.montar_url_imagem_campeao_loading(campeao['id'])

        campeao_com_url_img = {**campeao, 'imagem_url': url_imagem}

        return campeao_com_url_img

    async def listar_campeoes_resumo(self) -> list[CampeaoResumo]:

        dados = await self._cache.obter(
            self._versao,
            f'lista:{self._idioma}',
            lambda: self._client_data_dragon.get_campeoes(self._versao, self._idioma),
        )

        campeoes = dados['data'].values()

        return [CampeaoResumo.model_validate(self._adicionar_url_da_imagem(campeao)) for campeao in campeoes]

    def _montar_passiva(self, passiva: dict) -> dict:

        url_imagem = self._client_data_dragon.montar_url_imagem_passiva(
            self._versao, passiva['image']['full']
        )

        return {**passiva, 'imagem_url': url_imagem}

    def _montar_habilidades(self, habilidades: list[dict]) -> list[dict]:

        return [
            {
                **habilidade,
                'imagem_url': self._client_data_dragon.montar_url_imagem_habilidade(
                    self._versao, habilidade['image']['full']
                ),
            }
            for habilidade in habilidades
        ]

    def _montar_skins(self, campeao_id: str, skins: list[dict]) -> list[dict]:

        # chromas vêm na mesma lista, marcados com 'parentSkin', e não têm splash art própria
        return [
            {**skin, 'splash_url': self._client_data_dragon.montar_url_splash(campeao_id, skin['num'])}
            for skin in skins
            if 'parentSkin' not in skin
        ]

    async def buscar_campeao_detalhado(self, campeao_id: str) -> CampeaoDetalhe:

        dados = await self._cache.obter(
            self._versao,
            f'detalhe:{self._idioma}:{campeao_id}',
            lambda: self._client_data_dragon.get_campeao_detalhe_por_id(
                self._versao, self._idioma, campeao_id
            ),
        )

        campeao_detalhado = dados['data'][campeao_id]

        campeao_completo = {
            **self._adicionar_url_da_imagem(campeao_detalhado),
            'splash_url': self._client_data_dragon.montar_url_splash(campeao_id),
            'passive': self._montar_passiva(campeao_detalhado['passive']),
            'spells': self._montar_habilidades(campeao_detalhado['spells']),
            'skins': self._montar_skins(campeao_id, campeao_detalhado['skins']),
        }

        return CampeaoDetalhe.model_validate(campeao_completo)
