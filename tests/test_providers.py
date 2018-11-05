def test_get_provider_collection(client):
    response = client.get('/providers')
    assert response.status_code == 200
    assert 'json' in response.content_type
    assert response.is_json
    assert response.json['href'].startswith('http')
    assert response.json['href'].endswith('/providers')
    assert response.json['collection']

def test_get_provider_instance(client):
    collection_response = client.get('/providers')
    for provider in collection_response.json['collection']:
        instance_response = client.get(provider['href'])
        assert instance_response.status_code == 200
        assert 'json' in instance_response.content_type
        assert instance_response.is_json
        assert instance_response.json['href'].startswith('http')
        assert '/providers/' in instance_response.json['href']

def test_get_provider_doc(client):
    collection_response = client.get('/providers')
    for provider in collection_response.json['collection']:
        doc_response = client.get(provider['documentation'])
        assert 'text/html' in doc_response.content_type
        assert not doc_response.is_json

def test_get_analytic_instance(client):
    provider_collection_response = client.get('/providers')
    for provider in provider_collection_response.json['collection']:
        provider_instance_response = client.get(provider['href'])
        analytics = provider_instance_response.json['analytics']
        for analytic in analytics[:5]:
            analytic_response = client.get(analytic['href'])
            assert analytic_response.status_code == 200
            assert 'json' in analytic_response.content_type
            assert analytic_response.is_json
            assert analytic_response.json['href'].startswith('http')
            assert analytic_response.json['href'].endswith('/providers/{}/{}'.format(provider['name'],
                analytic_response.json['name']))

def test_get_analytic_doc(client):
    provider_collection_response = client.get('/providers')
    for provider in provider_collection_response.json['collection']:
        provider_instance_response = client.get(provider['href'])
        analytics = provider_instance_response.json['analytics']
        for analytic in analytics[:5]:
            analytic_response = client.get(analytic['href'])
            doc_response = client.get(analytic_response.json['documentation'])
            assert doc_response.status_code == 200
            assert 'text/html' in doc_response.content_type
            assert not doc_response.is_json
