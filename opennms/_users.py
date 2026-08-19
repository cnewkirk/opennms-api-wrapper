"""Users REST API – /rest/users."""
from xml.sax.saxutils import escape

from ._base import _OpenNMSBase
from .types import User


class UsersMixin(_OpenNMSBase):
    def get_users(self):
        """List all users."""
        return self._get("users")

    def get_user(self, username: str):
        """Get a specific user by *username*."""
        return self._get(f"users/{username}")

    def create_user(self, user: User, hash_password: bool = False):
        """Create a new user.

        Args:
            user: User attribute dict. Required key: ``user-id``. Optional
                keys: ``full-name``, ``user-comments``, ``password``,
                ``email``, ``duty-schedule`` (list of schedule strings).
                Example::

                    {
                        "user-id": "jsmith",
                        "full-name": "Jane Smith",
                        "password": "secret",
                        "email": "jsmith@example.com",
                    }

            hash_password: When ``True`` OpenNMS hashes the plain-text password.

        The body is sent as XML — ``POST /rest/users`` does not
        accept JSON on any OpenNMS version.
        """
        parts = []
        for key in ("user-id", "full-name", "user-comments", "email",
                    "password", "passwordSalt"):
            if key in user:
                value = user[key]
                if isinstance(value, bool):
                    value = str(value).lower()
                parts.append(f"<{key}>{escape(str(value))}</{key}>")
        for schedule in user.get("duty-schedule", []):
            parts.append(
                f"<duty-schedule>{escape(str(schedule))}</duty-schedule>")
        for role in user.get("role", []):
            parts.append(f"<role>{escape(str(role))}</role>")
        xml = f"<user>{''.join(parts)}</user>"
        params = {"hashPassword": "true"} if hash_password else None
        return self._post_text("users", xml, "application/xml",
                               params=params)

    def update_user(self, username: str, user: dict):
        """Update user properties.

        The body is sent form-encoded — ``PUT /rest/users/{name}``
        does not accept JSON on any OpenNMS version. Keys are bean
        property names, e.g. ``fullName``, ``email``, ``password``.

        Args:
            username: Username of the user to update.
            user: Dict of user fields to change. Pass only the fields to update.
        """
        return self._put(f"users/{username}", form_data=user)

    def delete_user(self, username: str):
        """Delete a user."""
        return self._delete(f"users/{username}")

    def assign_role_to_user(self, username: str, role_name: str):
        """Assign *role_name* to *username*."""
        return self._put(f"users/{username}/roles/{role_name}")

    def revoke_role_from_user(self, username: str, role_name: str):
        """Revoke *role_name* from *username*."""
        return self._delete(f"users/{username}/roles/{role_name}")
