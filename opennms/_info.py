"""Server Info REST API – /rest/info."""


class InfoMixin:
    def get_info(self):
        """Return OpenNMS server version, package info, and running services.

        Example response keys: ``displayVersion``, ``version``,
        ``packageName``, ``packageDescription``, ``ticketerConfig``,
        ``datetimeformatConfig``, ``services``.
        """
        return self._get("info")
