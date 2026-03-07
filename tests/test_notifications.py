"""Tests for NotificationsMixin – /rest/notifications."""
import responses
from .conftest import V1, qs
from .fixtures import NOTIFICATION, NOTIFICATION_LIST


@responses.activate
def test_get_notifications_default(client):
    responses.add(responses.GET, f"{V1}/notifications", json=NOTIFICATION_LIST)
    result = client.get_notifications()
    assert result["notification"][0]["notifyId"] == 601
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["10"]
    assert params["offset"] == ["0"]


@responses.activate
def test_get_notifications_with_filters(client):
    responses.add(responses.GET, f"{V1}/notifications", json=NOTIFICATION_LIST)
    client.get_notifications(limit=50, order_by="pageTime", order="descending",
                             answered="false")
    params = qs(responses.calls[0].request.url)
    assert params["limit"] == ["50"]
    assert params["answered"] == ["false"]


@responses.activate
def test_get_notification(client):
    responses.add(responses.GET, f"{V1}/notifications/601", json=NOTIFICATION)
    result = client.get_notification(601)
    assert result["notifyId"] == 601
    assert result["answeredBy"] == "admin"


@responses.activate
def test_get_notification_count(client):
    responses.add(responses.GET, f"{V1}/notifications/count",
                  body="8", content_type="text/plain")
    assert client.get_notification_count() == 8


@responses.activate
def test_trigger_destination_path(client):
    responses.add(responses.POST,
                  f"{V1}/notifications/destination-paths/Email/trigger",
                  status=200)
    result = client.trigger_destination_path("Email")
    assert result is None
    assert responses.calls[0].request.method == "POST"
    assert "Email/trigger" in responses.calls[0].request.url
