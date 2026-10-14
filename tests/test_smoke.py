import pytest

from link_vaulter.app import create_app

@pytest.fixture()
def client():
    return create_app(testing=True).test_client()


@pytest.mark.smoke
def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"LinkVaulter" in response.data


@pytest.mark.smoke
def test_health_endpoint(client):
    assert client.get("/health").get_json() == {"status": "ok"}


@pytest.mark.smoke
def test_json_api_data(client):
    data = client.get("/api/links").get_json()
    assert len(data) == 3
    assert data[0]["title"] == "Python Documentation"

