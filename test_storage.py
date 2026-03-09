import pytest
from storage import format_date


def test_format_date_valid_iso():
    """Test that a valid ISO timestamp formats correctly."""
    # This is a fixed date: March 9, 2026 at 12:30 PM
    iso_string = "2026-03-09T12:30:00"

    # Call our function
    result = format_date(iso_string)

    # Assert (check) that the result matches what we expect
    assert result == "Mar 09, 2026 at 12:30 PM"


def test_format_date_empty_or_na():
    """Test that empty strings or 'N/A' return the default 'Never studied' message."""
    assert format_date(None) == "Never studied"
    assert format_date("N/A") == "Never studied"


def test_format_date_invalid_string():
    """Test that an invalid date string just returns the string itself."""
    # If the database accidentally got corrupted with bad data,
    # the function should safely return the bad data instead of crashing.
    bad_data = "Not a real date"
    assert format_date(bad_data) == "Not a real date"
