from unittest.mock import Mock, patch

import pytest
import requests

from src.api_client import (
    APIError,
    APIHTTPError,
    APIInvalidDataError,
    APINetworkError,
    fetch_user,
)
from src.main import main


@patch("src.api_client.requests.get")
def test_success_response(mock_get):
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "data": {"id": 1, "name": "Alice", "email": "alice@example.com"}
    }
    mock_get.return_value = response

    result = fetch_user("https://example.test", 1)

    assert result == {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com",
    }
    mock_get.assert_called_once_with("https://example.test/users/1", timeout=5)


@patch("src.api_client.requests.get")
def test_http_404_raises_api_http_error(mock_get):
    response = Mock()
    response.status_code = 404
    response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "404 Client Error", response=response
    )
    mock_get.return_value = response

    with pytest.raises(APIHTTPError) as exc_info:
        fetch_user("https://example.test", 1)

    assert exc_info.value.status_code == 404


@patch("src.api_client.requests.get")
def test_server_error_is_handled(mock_get):
    response = Mock()
    response.status_code = 500
    response.raise_for_status.side_effect = requests.exceptions.HTTPError(
        "500 Server Error", response=response
    )
    mock_get.return_value = response

    with pytest.raises(APIHTTPError) as exc_info:
        fetch_user("https://example.test", 1)

    assert exc_info.value.status_code == 500


@patch("src.api_client.requests.get")
def test_timeout_raises_api_network_error(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout("timed out")

    with pytest.raises(APINetworkError):
        fetch_user("https://example.test", 1)


@patch("src.api_client.requests.get")
def test_connection_error_raises_api_network_error(mock_get):
    mock_get.side_effect = requests.exceptions.ConnectionError("refused")

    with pytest.raises(APINetworkError):
        fetch_user("https://example.test", 1)


@patch("src.api_client.requests.get")
def test_invalid_json_is_handled(mock_get):
    response = Mock()
    response.status_code = 200
    response.json.side_effect = ValueError("invalid json")
    mock_get.return_value = response

    with pytest.raises(APIInvalidDataError):
        fetch_user("https://example.test", 1)


@patch("src.api_client.requests.get")
def test_missing_data_key_raises_api_invalid_data_error(mock_get):
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"error": "not found"}
    mock_get.return_value = response

    with pytest.raises(APIInvalidDataError, match="data"):
        fetch_user("https://example.test", 1)


@patch("src.api_client.requests.get")
def test_missing_required_field_raises_api_invalid_data_error(mock_get):
    response = Mock()
    response.status_code = 200
    response.json.return_value = {"data": {"id": 1}}
    mock_get.return_value = response

    with pytest.raises(APIInvalidDataError, match="name"):
        fetch_user("https://example.test", 1)


def test_error_types_are_distinguishable():
    assert issubclass(APIError, Exception)
    assert issubclass(APINetworkError, APIError)
    assert issubclass(APIHTTPError, APIError)
    assert issubclass(APIInvalidDataError, APIError)
    assert not issubclass(APIInvalidDataError, APINetworkError)
    assert not issubclass(APINetworkError, APIInvalidDataError)
    assert not issubclass(APIHTTPError, APINetworkError)


@patch("src.main.fetch_user")
def test_main_reports_network_and_data_errors_differently(mock_fetch, capsys):
    mock_fetch.side_effect = APINetworkError("boom")
    main()
    network_output = capsys.readouterr().out

    mock_fetch.side_effect = APIInvalidDataError("bad payload")
    main()
    data_output = capsys.readouterr().out

    assert network_output != data_output
    assert "Network problem" in network_output
    assert "Invalid data from API" in data_output


@patch("src.main.fetch_user")
def test_main_prints_user_on_success(mock_fetch, capsys):
    mock_fetch.return_value = {"name": "Alice", "email": "alice@example.com"}

    main()

    captured = capsys.readouterr().out
    assert "User: Alice (alice@example.com)" in captured