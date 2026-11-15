import pytest
from jsonschema import validate

pytestmark = pytest.mark.api

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "username", "email", "address", "company"],
    "properties": {
        "id": {"type": "integer"},
        "name": {"type": "string"},
        "username": {"type": "string"},
        "email": {"type": "string", "pattern": "^[^@]+@[^@]+$"},
        "address": {
            "type": "object",
            "required": ["street", "city", "zipcode"],
        },
        "company": {"type": "object", "required": ["name"]},
    },
}


@pytest.mark.smoke
def test_get_user(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/users/2")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 2
    assert data["name"] == "Ervin Howell"


def test_user_matches_schema(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/users/1")

    assert response.status_code == 200
    validate(instance=response.json(), schema=USER_SCHEMA)


def test_user_not_found(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/users/999")

    assert response.status_code == 404


def test_create_user(api_session, api_base_url):
    payload = {"name": "Nimesha", "job": "QA Engineer"}
    response = api_session.post(f"{api_base_url}/users", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["job"] == payload["job"]
    assert "id" in data


def test_get_all_users(api_session, api_base_url):
    response = api_session.get(f"{api_base_url}/users")

    assert response.status_code == 200
    users = response.json()
    assert len(users) == 10
    for user in users:
        validate(instance=user, schema=USER_SCHEMA)
