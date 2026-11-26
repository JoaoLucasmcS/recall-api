from http import HTTPStatus


def test_listar_campeoes_deve_retornar_resumo_com_url_da_imagem(client):
    response = client.get('/campeoes/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == [
        {
            'id': 'Ahri',
            'name': 'Ahri',
            'title': 'a Raposa de Nove Caudas',
            'tags': ['Mage', 'Assassin'],
            'imagem_url': 'https://ddragon.leagueoflegends.com/cdn/img/champion/loading/Ahri_0.jpg',
        }
    ]


def test_listar_campeoes_deve_usar_versao_atual_do_data_dragon(client, data_dragon):
    client.get('/campeoes/')

    assert '/cdn/16.23.1/data/pt_BR/champion.json' in data_dragon.urls_pedidas


def test_buscar_campeao_deve_retornar_detalhe_com_habilidades_e_urls(client):
    response = client.get('/campeoes/Ahri')
    campeao = response.json()

    assert response.status_code == HTTPStatus.OK
    assert campeao['splash_url'] == 'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/Ahri_0.jpg'
    assert campeao['passive']['imagem_url'].endswith('/cdn/16.23.1/img/passive/Ahri_P.png')
    assert [spell['id'] for spell in campeao['spells']] == ['AhriQ', 'AhriW', 'AhriE', 'AhriR']
    assert campeao['spells'][0]['imagem_url'].endswith('/cdn/16.23.1/img/spell/AhriQ.png')


def test_buscar_campeao_deve_remover_chromas_das_skins(client):
    response = client.get('/campeoes/Ahri')

    assert [skin['num'] for skin in response.json()['skins']] == [0, 1]


def test_buscar_campeao_inexistente_deve_retornar_404(client):
    response = client.get('/campeoes/ahri')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Campeão não encontrado'}


def test_listar_campeoes_com_data_dragon_fora_do_ar_deve_retornar_503(client, data_dragon):
    data_dragon.fora_do_ar = True

    response = client.get('/campeoes/')

    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
    assert response.json() == {'detail': 'Data Dragon indisponível no momento'}


def test_buscar_campeao_com_data_dragon_fora_do_ar_deve_retornar_503(client, data_dragon):
    data_dragon.fora_do_ar = True

    response = client.get('/campeoes/Ahri')

    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
