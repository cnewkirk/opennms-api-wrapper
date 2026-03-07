"""Tests for AssetSuggestionsMixin – /rest/assets/suggestions."""
import responses
from .conftest import V1
from .fixtures import ASSET_SUGGESTIONS


@responses.activate
def test_get_asset_suggestions(client):
    responses.add(responses.GET, f"{V1}/assets/suggestions",
                  json=ASSET_SUGGESTIONS)
    result = client.get_asset_suggestions()
    assert result["assetSuggestion"][0]["column"] == "manufacturer"
    assert "Cisco" in result["assetSuggestion"][0]["values"]
