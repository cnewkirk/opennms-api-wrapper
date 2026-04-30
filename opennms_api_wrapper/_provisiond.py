"""Provisiond REST API v2 – /api/v2/provisiond."""
from ._base import _OpenNMSBase


class ProvisiondMixin(_OpenNMSBase):
    def get_provisiond_status(self):
        """Get the current status of the Provisiond daemon."""
        return self._get("provisiond/status", v2=True)

    def get_provisiond_job_status(self, job_id: str):
        """Get the status of a specific provisioning job.

        Args:
            job_id: Provisioning job ID.
        """
        return self._get(f"provisiond/status/{job_id}", v2=True)
