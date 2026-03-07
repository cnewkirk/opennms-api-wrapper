"""Javamail Configuration REST API – /rest/config/javamail."""
from .types import JavamailDefaultConfig, JavamailReadmail, JavamailSendmail, JavamailEnd2End


class JavamailConfigMixin:
    _JM = "config/javamail"

    # ------------------------------------------------------------------
    # Default configuration
    # ------------------------------------------------------------------

    def get_javamail_default_config(self):
        """Get the default Javamail configuration."""
        return self._get(self._JM)

    def set_javamail_default_config(self, data: JavamailDefaultConfig):
        """Update the default Javamail configuration.

        Args:
            data: Configuration data dict.
        """
        return self._post(self._JM, json_data=data)

    # ------------------------------------------------------------------
    # Read-mail configs
    # ------------------------------------------------------------------

    def get_javamail_readmails(self):
        """List all read-mail configurations."""
        return self._get(f"{self._JM}/readmails")

    def get_javamail_readmail(self, name: str):
        """Get a specific read-mail configuration by *name*."""
        return self._get(f"{self._JM}/readmails/{name}")

    def create_javamail_readmail(self, data: JavamailReadmail):
        """Create a new read-mail configuration.

        Args:
            data: Read-mail configuration dict.
        """
        return self._post(f"{self._JM}/readmails", json_data=data)

    def update_javamail_readmail(self, name: str, data: JavamailReadmail):
        """Update a read-mail configuration.

        Args:
            name: Name of the read-mail configuration.
            data: Form-encoded key/value pairs to update.
        """
        return self._put(f"{self._JM}/readmails/{name}",
                         form_data=data)

    def delete_javamail_readmail(self, name: str):
        """Delete a read-mail configuration."""
        return self._delete(f"{self._JM}/readmails/{name}")

    # ------------------------------------------------------------------
    # Send-mail configs
    # ------------------------------------------------------------------

    def get_javamail_sendmails(self):
        """List all send-mail configurations."""
        return self._get(f"{self._JM}/sendmails")

    def get_javamail_sendmail(self, name: str):
        """Get a specific send-mail configuration by *name*."""
        return self._get(f"{self._JM}/sendmails/{name}")

    def create_javamail_sendmail(self, data: JavamailSendmail):
        """Create a new send-mail configuration.

        Args:
            data: Send-mail configuration dict.
        """
        return self._post(f"{self._JM}/sendmails", json_data=data)

    def update_javamail_sendmail(self, name: str, data: JavamailSendmail):
        """Update a send-mail configuration.

        Args:
            name: Name of the send-mail configuration.
            data: Form-encoded key/value pairs to update.
        """
        return self._put(f"{self._JM}/sendmails/{name}",
                         form_data=data)

    def delete_javamail_sendmail(self, name: str):
        """Delete a send-mail configuration."""
        return self._delete(f"{self._JM}/sendmails/{name}")

    # ------------------------------------------------------------------
    # End-to-end configs
    # ------------------------------------------------------------------

    def get_javamail_end2ends(self):
        """List all end-to-end mail test configurations."""
        return self._get(f"{self._JM}/end2ends")

    def get_javamail_end2end(self, name: str):
        """Get a specific end-to-end mail test configuration by *name*."""
        return self._get(f"{self._JM}/end2ends/{name}")

    def create_javamail_end2end(self, data: JavamailEnd2End):
        """Create a new end-to-end mail test configuration.

        Args:
            data: End-to-end configuration dict.
        """
        return self._post(f"{self._JM}/end2ends", json_data=data)

    def update_javamail_end2end(self, name: str, data: JavamailEnd2End):
        """Update an end-to-end mail test configuration.

        Args:
            name: Name of the end-to-end configuration.
            data: Form-encoded key/value pairs to update.
        """
        return self._put(f"{self._JM}/end2ends/{name}",
                         form_data=data)

    def delete_javamail_end2end(self, name: str):
        """Delete an end-to-end mail test configuration."""
        return self._delete(f"{self._JM}/end2ends/{name}")
