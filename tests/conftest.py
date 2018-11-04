import pytest
import restful_analytics

@pytest.fixture(scope='function')
def app():
    return restful_analytics.create_app({'TESTING': True})

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()
