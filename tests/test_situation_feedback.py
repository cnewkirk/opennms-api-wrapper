"""Tests for SituationFeedbackMixin – /rest/situation-feedback."""
import json
import responses
from .conftest import V1, qs
from .fixtures import SITUATION_FEEDBACK_TAGS, SITUATION_FEEDBACK


@responses.activate
def test_get_situation_feedback_tags(client):
    responses.add(responses.GET, f"{V1}/situation-feedback/tags",
                  json=SITUATION_FEEDBACK_TAGS)
    result = client.get_situation_feedback_tags()
    assert result[0]["name"] == "correct"


@responses.activate
def test_get_situation_feedback_tags_with_prefix(client):
    responses.add(responses.GET, f"{V1}/situation-feedback/tags",
                  json=SITUATION_FEEDBACK_TAGS)
    client.get_situation_feedback_tags(prefix="cor")
    params = qs(responses.calls[0].request.url)
    assert params["prefix"] == ["cor"]


@responses.activate
def test_get_situation_feedback(client):
    responses.add(responses.GET, f"{V1}/situation-feedback/99",
                  json=SITUATION_FEEDBACK)
    result = client.get_situation_feedback(99)
    assert result[0]["feedbackType"] == "CORRECT"


@responses.activate
def test_submit_situation_feedback(client):
    responses.add(responses.POST, f"{V1}/situation-feedback/99",
                  status=204)
    result = client.submit_situation_feedback(99, SITUATION_FEEDBACK)
    assert result is None
    body = json.loads(responses.calls[0].request.body)
    assert body[0]["feedbackType"] == "CORRECT"
