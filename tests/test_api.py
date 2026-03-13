import pytest
import requests

from unittest.mock import patch
from word_stack.api import get_word_info


# The @patch decorator intercepts 'requests.get' inside our api.py file
@patch("word_stack.api.requests.get")
def test_get_word_info_success(mock_get):
    """Test fetching a word successfully using a fake API response."""

    # 1. Setup the fake response (This is what the API would normally return)
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{
        "phonetic": "/tɛst/",
        "meanings": [{
            "definitions": [{
                "definition": "A procedure intended to establish the quality of something.",
                "example": "Both tests were successful."
            }]
        }]
    }]

    # 2. Call function. It thinks it's hitting the internet, but it gets fake data!
    result = get_word_info("test")

    # 3. Assert it parsed fake JSON correctly
    assert result is not None
    assert result["phonetic"] == "/tɛst/"
    assert result["definition"] == "A procedure intended to establish the quality of something."
    assert result["example"] == "Both tests were successful."


@patch("word_stack.api.requests.get")
def test_get_word_info_not_found(mock_get):
    """Test how the app handles a 404 Not Found error."""

    # Simulate the API returning a 404 error
    mock_get.return_value.status_code = 404

    # Tell pytest that we EXPECT a ValueError to be raised here
    with pytest.raises(ValueError, match="not_found"):
        get_word_info("notarealword123")


@patch("word_stack.api.requests.get")
def test_get_word_info_connection_error(mock_get):
    """Test how the app handles a complete network failure."""

    # .side_effect is used in mocks to simulate an exception being thrown
    mock_get.side_effect = requests.exceptions.ConnectionError("No internet")

    with pytest.raises(ConnectionError):
        get_word_info("wifi_is_down_word")
