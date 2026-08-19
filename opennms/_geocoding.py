"""Geocoding REST API v2 – /api/v2/geocoding."""
from ._base import _OpenNMSBase


class GeocodingMixin(_OpenNMSBase):
    def get_geocoding_config(self):
        """Get the geocoder service manager configuration.

        Returns:
            Dict with the ``activeGeocoderId`` key (``None`` when no
            geocoder is active).
        """
        return self._get("geocoding/config", v2=True)

    def get_geocoders(self):
        """Get all registered geocoder services.

        Returns:
            List of geocoder definitions with their configuration, or
            ``None`` when none are registered (204 No Content).
        """
        return self._get("geocoding/geocoders", v2=True)

    def set_active_geocoder(self, geocoder_id: str):
        """Activate the geocoder service with *geocoder_id*.

        Args:
            geocoder_id: Identifier of the geocoder to activate,
                e.g. ``"nominatim"`` or ``"google"``.
        """
        return self._post("geocoding/config",
                          json_data={"activeGeocoderId": geocoder_id},
                          v2=True)

    def configure_geocoder(self, geocoder_id: str, config: dict):
        """Update the configuration of a geocoder service.

        Args:
            geocoder_id: Identifier of the geocoder to configure.
            config: Provider-specific settings as string key/value
                pairs, e.g. ``{"apiKey": "..."}``.
        """
        return self._post(f"geocoding/geocoders/{geocoder_id}",
                          json_data={"config": config}, v2=True)

    def reset_geocoding_config(self):
        """Reset the geocoder service manager to its defaults."""
        return self._delete("geocoding/config", v2=True)
