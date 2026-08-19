"""Applications REST API v2 – /api/v2/applications."""
from ._base import _OpenNMSBase
from .types import Application


class ApplicationsMixin(_OpenNMSBase):
    def get_applications(self, limit: int = 10, offset: int = 0):
        """List all applications.

        Args:
            limit: Maximum number of results.
            offset: Number of results to skip.
        """
        params = {"limit": limit, "offset": offset}
        return self._get("applications", params=params, v2=True)

    def get_application(self, app_id: int):
        """Get a specific application by *app_id*."""
        return self._get(f"applications/{app_id}", v2=True)

    def create_application(self, app: Application):
        """Create a new application.

        Args:
            app: Application definition dict with keys such as ``name``
                and ``monitoredServices``.
        """
        return self._post("applications", json_data=app, v2=True)

    def delete_application(self, app_id: int):
        """Delete an application."""
        return self._delete(f"applications/{app_id}", v2=True)
