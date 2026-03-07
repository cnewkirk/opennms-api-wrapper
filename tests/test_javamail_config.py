"""Tests for JavamailConfigMixin – /rest/config/javamail."""
import json
import responses
from .conftest import V1
from .fixtures import (
    JAVAMAIL_DEFAULT_CONFIG,
    JAVAMAIL_READMAIL, JAVAMAIL_READMAIL_LIST,
    JAVAMAIL_SENDMAIL, JAVAMAIL_SENDMAIL_LIST,
    JAVAMAIL_END2END, JAVAMAIL_END2END_LIST,
)


@responses.activate
def test_get_javamail_default_config(client):
    responses.add(responses.GET, f"{V1}/config/javamail",
                  json=JAVAMAIL_DEFAULT_CONFIG)
    result = client.get_javamail_default_config()
    assert result["defaultReadConfigName"] == "localhost"


@responses.activate
def test_set_javamail_default_config(client):
    responses.add(responses.POST, f"{V1}/config/javamail", status=204)
    result = client.set_javamail_default_config(
        {"defaultReadConfigName": "remote"})
    assert result is None


# -- readmails --

@responses.activate
def test_get_javamail_readmails(client):
    responses.add(responses.GET, f"{V1}/config/javamail/readmails",
                  json=JAVAMAIL_READMAIL_LIST)
    result = client.get_javamail_readmails()
    assert result["readmail"][0]["name"] == "localhost"


@responses.activate
def test_get_javamail_readmail(client):
    responses.add(responses.GET,
                  f"{V1}/config/javamail/readmails/localhost",
                  json=JAVAMAIL_READMAIL)
    result = client.get_javamail_readmail("localhost")
    assert result["protocol"] == "imaps"


@responses.activate
def test_create_javamail_readmail(client):
    responses.add(responses.POST, f"{V1}/config/javamail/readmails",
                  status=201)
    client.create_javamail_readmail(JAVAMAIL_READMAIL)
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "localhost"


@responses.activate
def test_update_javamail_readmail(client):
    responses.add(responses.PUT,
                  f"{V1}/config/javamail/readmails/localhost",
                  status=204)
    result = client.update_javamail_readmail("localhost",
                                             {"port": "995"})
    assert result is None
    assert "port=995" in responses.calls[0].request.body


@responses.activate
def test_delete_javamail_readmail(client):
    responses.add(responses.DELETE,
                  f"{V1}/config/javamail/readmails/localhost",
                  status=204)
    result = client.delete_javamail_readmail("localhost")
    assert result is None


# -- sendmails --

@responses.activate
def test_get_javamail_sendmails(client):
    responses.add(responses.GET, f"{V1}/config/javamail/sendmails",
                  json=JAVAMAIL_SENDMAIL_LIST)
    result = client.get_javamail_sendmails()
    assert result["sendmail"][0]["name"] == "localhost"


@responses.activate
def test_get_javamail_sendmail(client):
    responses.add(responses.GET,
                  f"{V1}/config/javamail/sendmails/localhost",
                  json=JAVAMAIL_SENDMAIL)
    result = client.get_javamail_sendmail("localhost")
    assert result["protocol"] == "smtp"


@responses.activate
def test_create_javamail_sendmail(client):
    responses.add(responses.POST, f"{V1}/config/javamail/sendmails",
                  status=201)
    client.create_javamail_sendmail(JAVAMAIL_SENDMAIL)
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "localhost"


@responses.activate
def test_update_javamail_sendmail(client):
    responses.add(responses.PUT,
                  f"{V1}/config/javamail/sendmails/localhost",
                  status=204)
    result = client.update_javamail_sendmail("localhost",
                                             {"port": "587"})
    assert result is None


@responses.activate
def test_delete_javamail_sendmail(client):
    responses.add(responses.DELETE,
                  f"{V1}/config/javamail/sendmails/localhost",
                  status=204)
    result = client.delete_javamail_sendmail("localhost")
    assert result is None


# -- end2ends --

@responses.activate
def test_get_javamail_end2ends(client):
    responses.add(responses.GET, f"{V1}/config/javamail/end2ends",
                  json=JAVAMAIL_END2END_LIST)
    result = client.get_javamail_end2ends()
    assert result["end2end"][0]["name"] == "localhost"


@responses.activate
def test_get_javamail_end2end(client):
    responses.add(responses.GET,
                  f"{V1}/config/javamail/end2ends/localhost",
                  json=JAVAMAIL_END2END)
    result = client.get_javamail_end2end("localhost")
    assert result["readMailConfigName"] == "localhost"


@responses.activate
def test_create_javamail_end2end(client):
    responses.add(responses.POST, f"{V1}/config/javamail/end2ends",
                  status=201)
    client.create_javamail_end2end(JAVAMAIL_END2END)
    body = json.loads(responses.calls[0].request.body)
    assert body["name"] == "localhost"


@responses.activate
def test_update_javamail_end2end(client):
    responses.add(responses.PUT,
                  f"{V1}/config/javamail/end2ends/localhost",
                  status=204)
    result = client.update_javamail_end2end("localhost",
                                            {"readMailConfigName": "remote"})
    assert result is None


@responses.activate
def test_delete_javamail_end2end(client):
    responses.add(responses.DELETE,
                  f"{V1}/config/javamail/end2ends/localhost",
                  status=204)
    result = client.delete_javamail_end2end("localhost")
    assert result is None
