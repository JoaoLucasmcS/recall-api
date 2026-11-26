from recall_api.app import app

DUAS_VEZES = 2


def test_versao_deve_ser_buscada_uma_vez_dentro_do_prazo(client, data_dragon):
    client.get('/campeoes/')
    client.get('/campeoes/')
    client.get('/patch/')

    assert data_dragon.quantas_vezes('versions.json') == 1


def test_versao_deve_ser_buscada_de_novo_depois_do_prazo(client, data_dragon):
    client.get('/patch/')
    # simula que as 6h passaram: o horário da última busca fica muito no passado
    app.state.cache_versao._buscado_em -= 7 * 60 * 60
    data_dragon.versoes = ['16.24.1']

    response = client.get('/patch/')

    assert data_dragon.quantas_vezes('versions.json') == DUAS_VEZES
    assert response.json() == {'versao': '16.24.1'}


def test_campeoes_devem_ser_baixados_uma_vez_por_patch(client, data_dragon):
    for _ in range(3):
        client.get('/campeoes/')
        client.get('/campeoes/Ahri')

    assert data_dragon.quantas_vezes('/champion.json') == 1
    assert data_dragon.quantas_vezes('/champion/Ahri.json') == 1


def test_campeoes_devem_ser_baixados_de_novo_quando_sai_patch_novo(client, data_dragon):
    client.get('/campeoes/')
    app.state.cache_versao._buscado_em -= 7 * 60 * 60
    data_dragon.versoes = ['16.24.1']

    client.get('/campeoes/')

    assert data_dragon.quantas_vezes('/cdn/16.23.1/data/pt_BR/champion.json') == 1
    assert data_dragon.quantas_vezes('/cdn/16.24.1/data/pt_BR/champion.json') == 1


def test_erro_nao_deve_ficar_guardado_no_cache(client, data_dragon):
    client.get('/campeoes/ahri')
    client.get('/campeoes/ahri')

    assert data_dragon.quantas_vezes('/champion/ahri.json') == DUAS_VEZES
