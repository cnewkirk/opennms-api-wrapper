"""Users REST API – /rest/users."""
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
        """
        params = {"hashPassword": "true"} if hash_password else None
        return self._post("users", json_data=user, params=params)

    def update_user(self, username: str, user: User):
        """Update user properties.

        Args:
            username: Username of the user to update.
            user: Dict of user fields to change. Pass only the fields to update.
        """
        return self._put(f"users/{username}", json_data=user)

    def delete_user(self, username: str):
        """Delete a user."""
        return self._delete(f"users/{username}")

    def assign_role_to_user(self, username: str, role_name: str):
        """Assign *role_name* to *username*."""
        return self._put(f"users/{username}/roles/{role_name}")

    def revoke_role_from_user(self, username: str, role_name: str):
        """Revoke *role_name* from *username*."""
        return self._delete(f"users/{username}/roles/{role_name}")
