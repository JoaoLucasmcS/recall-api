from recall_api.clients.data_dragon import DataDragonClient
from recall_api.schemas.campeoes_schemas import CampeaoResumo


class CampeoesService:
    def __init__(self, client_data_dragon: DataDragonClient) -> None:
        self._client_data_dragon = client_data_dragon

    async def listar_campeoes_resumo(self) -> list[CampeaoResumo]:

        dados = await self._client_data_dragon.get_campeoes()

        campeoes = dados["data"].values()

        return [CampeaoResumo.model_validate(campeao) for campeao in campeoes]
