"""Filesystem REST API – /rest/filesystem.

Read and write configuration files in the OpenNMS ``etc`` directory.
All calls require the ``FILESYSTEM EDITOR`` role.
"""
from ._base import _OpenNMSBase


class FilesystemMixin(_OpenNMSBase):
    def get_filesystem_files(self, changed_only: bool = False):
        """Get the configuration files accessible via the API.

        Args:
            changed_only: Only list files that differ from the
                shipped defaults.

        Returns:
            List of file names.
        """
        params = {"changedFilesOnly": "true"} if changed_only else None
        return self._get("filesystem", params=params)

    def get_filesystem_extensions(self):
        """Get the file extensions supported by the filesystem API."""
        return self._get("filesystem/extensions")

    def get_filesystem_help(self, filename: str) -> str:
        """Get the Markdown help text for a configuration file.

        Args:
            filename: Name of the configuration file.
        """
        return self._get_text("filesystem/help",
                              params={"f": filename})

    def get_filesystem_contents(self, filename: str) -> str:
        """Get the contents of a configuration file.

        Args:
            filename: Name of the configuration file, e.g.
                ``"discovery-configuration.xml"``.
        """
        return self._get_text("filesystem/contents",
                              params={"f": filename})

    def upload_filesystem_contents(self, filename: str, content):
        """Create or overwrite a configuration file.

        Args:
            filename: Name of the configuration file.
            content: New file contents as ``str`` or ``bytes``.
        """
        if isinstance(content, str):
            content = content.encode()
        files = {"upload": (filename, content)}
        return self._post_files("filesystem/contents", files=files,
                                params={"f": filename})

    def delete_filesystem_file(self, filename: str):
        """Delete a configuration file.

        Args:
            filename: Name of the configuration file.
        """
        return self._delete("filesystem/contents",
                            params={"f": filename})
