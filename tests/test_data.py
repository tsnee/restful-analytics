def test_get_empty_collection(client):
    empty_response = client.get('/data')
    assert empty_response.status_code == 200
    assert 'json' in empty_response.content_type
    assert empty_response.is_json
    assert empty_response.json['href'].startswith('http')
    assert empty_response.json['href'].endswith('/data')
    assert not empty_response.json['collection']

def test_put_to_collection(client):
    put_response = client.put('/data',
            data={'python': '1'},
    )
    assert put_response.status_code == 201
    assert 'json' in put_response.content_type
    assert put_response.is_json
    assert put_response.location == put_response.json['href']
    assert put_response.json['href'].startswith('http')
    assert '/data/' in put_response.json['href']

def test_get_collection(client):
    response = client.get('/data')
    assert response.status_code == 200
    assert 'json' in response.content_type
    assert response.is_json
    assert response.json['href'].startswith('http')
    assert response.json['href'].endswith('/data')
    assert response.json['collection']
