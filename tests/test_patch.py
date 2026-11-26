from http import HTTPStatus


def test_patch_deve_retornar_versao_mais_recente(client):
    response = client.get('/patch/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'versao': '16.23.1'}


def test_patch_com_data_dragon_fora_do_ar_deve_retornar_503(client, data_dragon):
    data_dragon.fora_do_ar = True

    response = client.get('/patch/')

    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE
