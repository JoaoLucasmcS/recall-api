import httpx
import pytest
from fastapi.testclient import TestClient

from recall_api.app import app

AHRI = {
    'id': 'Ahri',
    'name': 'Ahri',
    'title': 'a Raposa de Nove Caudas',
    'tags': ['Mage', 'Assassin'],
    'image': {'full': 'Ahri.png'},
    'info': {'attack': 3, 'defense': 4, 'magic': 8, 'difficulty': 5},
    'lore': 'Lore completa',
    'blurb': 'Resumo',
    'allytips': ['Dica com'],
    'enemytips': ['Dica contra'],
    'partype': 'Mana',
    'stats': {},
    'passive': {'name': 'Furto de Essência', 'description': 'Descrição', 'image': {'full': 'Ahri_P.png'}},
    'spells': [
        {
            'id': f'Ahri{tecla}',
            'name': tecla,
            'description': 'Descrição',
            'cooldownBurn': '7',
            'costBurn': '55',
            'image': {'full': f'Ahri{tecla}.png'},
        }
        for tecla in 'QWER'
    ],
    'skins': [
        {'id': '103000', 'num': 0, 'name': 'default', 'chromas': False},
        {'id': '103001', 'num': 1, 'name': 'Ahri da Dinastia', 'chromas': True},
        {'id': '103008', 'num': 8, 'name': 'Ahri da Dinastia (Ametista)', 'chromas': False, 'parentSkin': 1},
    ],
}


class DataDragonFalso:
    """Simula o Data Dragon: responde como a CDN real e registra cada URL pedida."""

    def __init__(self):
        self.versoes = ['16.23.1', '16.22.1']
        self.fora_do_ar = False
        self.urls_pedidas: list[str] = []

    def responder(self, requisicao: httpx.Request) -> httpx.Response:
        caminho = requisicao.url.path
        self.urls_pedidas.append(caminho)

        if self.fora_do_ar:
            raise httpx.ConnectError('Data Dragon fora do ar', request=requisicao)

        if caminho == '/api/versions.json':
            return httpx.Response(200, json=self.versoes)
        if caminho.endswith('/champion.json'):
            return httpx.Response(200, json={'data': {'Ahri': AHRI}})
        if caminho.endswith('/champion/Ahri.json'):
            return httpx.Response(200, json={'data': {'Ahri': AHRI}})
        # a CDN real responde 403 para arquivos que não existem
        return httpx.Response(403, text='<Error>AccessDenied</Error>')

    def quantas_vezes(self, trecho: str) -> int:
        return sum(trecho in url for url in self.urls_pedidas)


@pytest.fixture
def data_dragon():
    return DataDragonFalso()


@pytest.fixture
def client(data_dragon):
    # o "with" roda o lifespan: cria caches novos (vazios) para cada teste
    with TestClient(app) as client:
        # troca o client HTTP real por um que responde com o Data Dragon falso
        app.state.http_client = httpx.AsyncClient(
            base_url='https://ddragon.leagueoflegends.com',
            transport=httpx.MockTransport(data_dragon.responder),
        )
        yield client
