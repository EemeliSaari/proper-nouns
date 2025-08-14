import pytest


def test_parse_valid_url(test_client, test_url):
    res = test_client.post('/pos/count_propn', json={'url': test_url})
    assert res.status_code == 200
    assert len(res.json()['values']) > 0


@pytest.mark.parametrize('url', ['not-url', 42, {'nested': 'structure'}])
def test_parse_invalid_url(url, test_client):
    res = test_client.post('/pos/count_propn', json={'url': url})
    assert res.status_code == 422


def test_page_not_loading(test_client):
    res = test_client.post('/pos/count_propn', json={'url': 'https://absolotely-false.url'})
    assert res.status_code == 400


def test_healthcheck(test_client):
    res = test_client.get('/healthcheck')
    assert res.status_code == 200
    assert res.json() == {'status': 'alive'}
