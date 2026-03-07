"""Tests for ProvisiondMixin – /api/v2/provisiond."""
import responses
from .conftest import V2
from .fixtures import PROVISIOND_STATUS, PROVISIOND_JOB_STATUS


@responses.activate
def test_get_provisiond_status(client):
    responses.add(responses.GET, f"{V2}/provisiond/status",
                  json=PROVISIOND_STATUS)
    result = client.get_provisiond_status()
    assert result["status"] == "RUNNING"


@responses.activate
def test_get_provisiond_job_status(client):
    responses.add(responses.GET, f"{V2}/provisiond/status/job-123",
                  json=PROVISIOND_JOB_STATUS)
    result = client.get_provisiond_job_status("job-123")
    assert result["id"] == "job-123"
    assert result["status"] == "COMPLETED"
