import requests

REQUIRED_USER_FIELDS = ("name", "email")


class APIError(Exception):
    """Base class for all API client errors."""


class APINetworkError(APIError):
    """Network-level problem: timeout, connection failure, request error."""


class APIHTTPError(APIError):
    """API responded with an HTTP 4xx/5xx status."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class APIInvalidDataError(APIError):
    """API responded, but the payload is not valid JSON or has an unexpected shape."""


def fetch_user(base_url: str, user_id: int) -> dict:
    try:
        response = requests.get(f"{base_url}/users/{user_id}", timeout=5)
        response.raise_for_status()
    except requests.exceptions.HTTPError as exc:
        status_code = exc.response.status_code if exc.response is not None else None
        raise APIHTTPError(
            f"API returned HTTP error {status_code}", status_code=status_code
        ) from exc
    except requests.exceptions.Timeout as exc:
        raise APINetworkError("API request timed out") from exc
    except requests.exceptions.ConnectionError as exc:
        raise APINetworkError("API connection failed") from exc
    except requests.exceptions.RequestException as exc:
        raise APINetworkError(f"API request failed: {exc}") from exc

    try:
        payload = response.json()
    except ValueError as exc:
        raise APIInvalidDataError("API response is not valid JSON") from exc

    if not isinstance(payload, dict):
        raise APIInvalidDataError("API response is not a JSON object")

    if "data" in payload:
        user = payload["data"]
    elif all(field in payload for field in REQUIRED_USER_FIELDS):
        # Some APIs (e.g. jsonplaceholder) return the user object without a 'data' wrapper.
        user = payload
    else:
        raise APIInvalidDataError("API response is missing the 'data' field")

    if not isinstance(user, dict):
        raise APIInvalidDataError("'data' is not a JSON object")

    for field in REQUIRED_USER_FIELDS:
        if field not in user:
            raise APIInvalidDataError(
                f"API response is missing required field '{field}'"
            )

    return user
