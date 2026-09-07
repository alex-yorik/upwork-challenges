from src.api_client import (
    APIError,
    APIHTTPError,
    APIInvalidDataError,
    APINetworkError,
    fetch_user,
)

BASE_URL = "https://jsonplaceholder.typicode.com"


def get_user(user_id: int) -> dict:
    return fetch_user(BASE_URL, user_id)


def main() -> None:
    try:
        user = get_user(1)
    except APIHTTPError as exc:
        print(f"API error: {exc}")
    except APINetworkError as exc:
        print(f"Network problem: {exc}")
    except APIInvalidDataError as exc:
        print(f"Invalid data from API: {exc}")
    except APIError as exc:
        print(f"API request failed: {exc}")
    except Exception as exc:
        print(f"Unexpected error: {exc}")
    else:
        print(f"User: {user['name']} ({user['email']})")


if __name__ == "__main__":
    main()
