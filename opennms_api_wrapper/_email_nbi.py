"""Email NBI Configuration REST API – /rest/config/email-nbi."""


class EmailNbiMixin:
    _EMAIL_NBI = "config/email-nbi"

    def get_email_nbi_config(self):
        """Get the full email NBI configuration."""
        return self._get(self._EMAIL_NBI)

    def get_email_nbi_status(self):
        """Get the email NBI forwarding status."""
        return self._get(f"{self._EMAIL_NBI}/status")

    def set_email_nbi_status(self, enabled: bool):
        """Enable or disable email NBI forwarding.

        Args:
            enabled: ``True`` to enable, ``False`` to disable.
        """
        return self._put(f"{self._EMAIL_NBI}/status",
                         form_data={"enabled": str(enabled).lower()})

    def get_email_nbi_destinations(self):
        """List all email NBI destinations."""
        return self._get(f"{self._EMAIL_NBI}/destinations")

    def get_email_nbi_destination(self, name: str):
        """Get a specific email destination by *name*."""
        return self._get(f"{self._EMAIL_NBI}/destinations/{name}")

    def create_email_nbi_destination(self, data: dict):
        """Create a new email NBI destination.

        Args:
            data: Destination definition dict with keys such as ``name``,
                ``firstOccurrenceOnly``, ``filters``.
        """
        return self._post(f"{self._EMAIL_NBI}/destinations",
                          json_data=data)

    def update_email_nbi_destination(self, name: str, data: dict):
        """Update an email NBI destination.

        Args:
            name: Name of the destination to update.
            data: Form-encoded key/value pairs to update.
        """
        return self._put(f"{self._EMAIL_NBI}/destinations/{name}",
                         form_data=data)

    def delete_email_nbi_destination(self, name: str):
        """Delete an email NBI destination."""
        return self._delete(f"{self._EMAIL_NBI}/destinations/{name}")

    def update_email_nbi_config(self, data: dict):
        """Update the email NBI configuration.

        Args:
            data: Updated configuration data dict.
        """
        return self._post(self._EMAIL_NBI, json_data=data)
