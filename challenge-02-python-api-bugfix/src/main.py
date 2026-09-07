from src.api_client import fetch_user


BASE_URL = "https://jsonplaceholder.typicode.com"


def get_user(user_id: int) -> dict:
    return fetch_user(BASE_URL, user_id)


def main() -> None:
    try:
        user = get_user(1)
        print(f"User: {user['name']} ({user['email']})")
    except Exception as exc:
        print(f"Request failed: {exc}")


if __name__ == "__main__":
    main()
