import requests


class APIError(Exception):
    pass


def fetch_user(base_url: str, user_id: int) -> dict:
    response = requests.get(f"{base_url}/users/{user_id}", timeout=5)
    data = response.json()
    return data["data"]
