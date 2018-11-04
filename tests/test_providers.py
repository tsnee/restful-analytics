def test_get_collection(client):
    response = client.get('/providers')
    assert response.status_code == 200
    assert 'json' in response.content_type
    assert response.is_json
    assert response.json['href'].startswith('http')
    assert response.json['href'].endswith('/providers')
    assert response.json['collection']

def test_get_instance(client):
    collection_response = client.get('/providers')
    for provider in collection_response.json['collection']:
        instance_response = client.get(provider['href'])
        assert instance_response.status_code == 200
        assert 'json' in instance_response.content_type
        assert instance_response.is_json
        assert instance_response.json['href'].startswith('http')
        assert '/providers/' in instance_response.json['href']
