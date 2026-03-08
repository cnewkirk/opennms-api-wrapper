"""Exception hierarchy for opennms-api-wrapper."""


class OpenNMSError(Exception):
    """Base class for all opennms-api-wrapper exceptions."""


class OpenNMSHTTPError(OpenNMSError):
    """Raised when the OpenNMS server returns an HTTP error response.

    Attributes:
        status_code: The HTTP status code returned by the server.
        response: The original ``requests.Response`` object, providing
            access to headers, URL, and raw body.
    """

    def __init__(self, message: str, response=None):
        super().__init__(message)
        self.response = response
        self.status_code = response.status_code if response is not None else None


class BadRequestError(OpenNMSHTTPError):
    """400 Bad Request — the request body or parameters were invalid."""


class AuthenticationError(OpenNMSHTTPError):
    """401 Unauthorized — credentials are missing or incorrect."""


class ForbiddenError(OpenNMSHTTPError):
    """403 Forbidden — the authenticated user lacks permission."""


class NotFoundError(OpenNMSHTTPError):
    """404 Not Found — the requested resource does not exist."""


class ConflictError(OpenNMSHTTPError):
    """409 Conflict — the resource already exists or a state conflict occurred."""


class ServerError(OpenNMSHTTPError):
    """5xx Server Error — the OpenNMS server encountered an internal error."""
