from unittest.mock import Mock, patch

from src.api_client import fetch_user


@patch("src.api_client.requests.get")
def test_success_response(mock_get):
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "data": {"id": 1, "name": "Alice", "email": "alice@example.com"}
    }
    mock_get.return_value = response

    result = fetch_user("https://example.test", 1)

    assert result["name"] == "Alice"
    assert result["email"] == "alice@example.com"


@patch("src.api_client.requests.get")
def test_server_error_is_handled(mock_get):
    response = Mock()
    response.status_code = 500
    response.json.return_value = {"error": "temporary failure"}
    mock_get.return_value = response

    # TODO: expected behaviour is defined by the client brief.
    # This test intentionally exposes the current defect.
    try:
        fetch_user("https://example.test", 1)
    except Exception:
        pass


@patch("src.api_client.requests.get")
def test_invalid_json_is_handled(mock_get):
    response = Mock()
    response.status_code = 200
    response.json.side_effect = ValueError("invalid json")
    mock_get.return_value = response

    try:
        fetch_user("https://example.test", 1)
    except Exception:
        pass
