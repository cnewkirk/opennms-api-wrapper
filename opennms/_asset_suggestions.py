"""Asset Suggestions REST API – /rest/assets/suggestions."""


class AssetSuggestionsMixin:
    def get_asset_suggestions(self):
        """Get asset field suggestions based on existing inventory data."""
        return self._get("assets/suggestions")
