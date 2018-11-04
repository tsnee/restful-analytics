def test_get_empty_collection(client):
    empty_response = client.get('/computations')
    assert empty_response.status_code == 200
    assert 'json' in empty_response.content_type
    assert empty_response.is_json
    assert empty_response.json['href'].endswith('/computations')
    assert not empty_response.json['collection']

def test_post_to_collection(client):
    post_response = client.post('/computations',
            content_type='application/x-www-form-urlencoded',
            data='provider=numpy&analytic=roll&operand=[1,2,3]&operand=1',
    )
    assert post_response.status_code == 201
    assert 'json' in post_response.content_type
    assert post_response.is_json
    assert post_response.location == post_response.json['href']
    assert post_response.json['href'].startswith('http')
    assert '/computations/' in post_response.json['href']

def test_get_collection(client):
    response = client.get('/computations')
    assert response.status_code == 200
    assert 'json' in response.content_type
    assert response.is_json
    assert response.json['href'].endswith('/computations')
    assert response.json['collection']
