"""Tests for UsersMixin – /rest/users."""
import responses
from .conftest import V1, qs
from .fixtures import USER, USER_LIST

NEW_USER = {
    "user-id": "newuser",
    "full-name": "New User",
    "password": "s3cret",
    "email": "newuser@example.com",
}


@responses.activate
def test_get_users(client):
    responses.add(responses.GET, f"{V1}/users", json=USER_LIST)
    result = client.get_users()
    assert result["user"][0]["user-id"] == "jsmith"


@responses.activate
def test_get_user(client):
    responses.add(responses.GET, f"{V1}/users/jsmith", json=USER)
    result = client.get_user("jsmith")
    assert result["user-id"] == "jsmith"
    assert result["full-name"] == "Jane Smith"


@responses.activate
def test_create_user(client):
    responses.add(responses.POST, f"{V1}/users", json=USER, status=201)
    client.create_user(NEW_USER)
    request = responses.calls[0].request
    assert request.headers["Content-Type"] == "application/xml"
    assert request.body == (
        "<user><user-id>newuser</user-id>"
        "<full-name>New User</full-name>"
        "<email>newuser@example.com</email>"
        "<password>s3cret</password></user>")


@responses.activate
def test_create_user_hash_password(client):
    responses.add(responses.POST, f"{V1}/users", json=USER, status=201)
    client.create_user(NEW_USER, hash_password=True)
    assert qs(responses.calls[0].request.url)["hashPassword"] == ["true"]


@responses.activate
def test_create_user_roles_and_salt(client):
    responses.add(responses.POST, f"{V1}/users", status=201)
    client.create_user({
        "user-id": "oncall",
        "password": "hashed",
        "passwordSalt": True,
        "role": ["ROLE_ADMIN"],
    })
    assert responses.calls[0].request.body == (
        "<user><user-id>oncall</user-id>"
        "<password>hashed</password>"
        "<passwordSalt>true</passwordSalt>"
        "<role>ROLE_ADMIN</role></user>")


@responses.activate
def test_update_user(client):
    responses.add(responses.PUT, f"{V1}/users/jsmith", status=204)
    client.update_user("jsmith", {"fullName": "Jane A. Smith"})
    request = responses.calls[0].request
    assert request.headers["Content-Type"] == (
        "application/x-www-form-urlencoded")
    assert request.body == "fullName=Jane+A.+Smith"


@responses.activate
def test_delete_user(client):
    responses.add(responses.DELETE, f"{V1}/users/jsmith", status=202)
    result = client.delete_user("jsmith")
    assert result is None


@responses.activate
def test_assign_role_to_user(client):
    responses.add(responses.PUT, f"{V1}/users/jsmith/roles/ROLE_ADMIN",
                  status=204)
    result = client.assign_role_to_user("jsmith", "ROLE_ADMIN")
    assert result is None
    assert "/users/jsmith/roles/ROLE_ADMIN" in responses.calls[0].request.url


@responses.activate
def test_revoke_role_from_user(client):
    responses.add(responses.DELETE, f"{V1}/users/jsmith/roles/ROLE_ADMIN",
                  status=204)
    result = client.revoke_role_from_user("jsmith", "ROLE_ADMIN")
    assert result is None
